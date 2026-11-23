#!/usr/bin/env python3
"""
Client minimal pour l'API RPC du DeepSeek Harness (DSH) local.

Le serveur DSH (http://127.0.0.1:3080) n'expose PAS d'endpoint OpenAI
(/api/chat n'existe pas). Il expose un protocole RPC maison :

    POST /api/<method>
    body: {"type": "client-request", "rpcId": "<uuid>", "method": "<method>", "payload": {...}}
    ->   {"type": "server-response", "rpcId": "<même uuid>",
          "result": {"ok": true, "value": {...}} | {"ok": false, "error": {...}}}

Ce script :
  1. réutilise une session existante (ou en crée une),
  2. envoie un message via session.prompt (mode queue),
  3. attend la réponse de l'assistant en interrogeant session.history,
  4. affiche la réponse.

Usage :
    python req_api.py [--new] [message...]
    --new force une nouvelle session (par défaut, la conversation la plus
          récente non occupée est réutilisée).
    Exemple : python req_api.py --new "Bonjour, qui es-tu ?"
"""

import sys
import time
import uuid

import requests

BASE_URL = "http://127.0.0.1:3080"
POLL_INTERVAL = 0.5   # secondes entre deux lectures de l'historique
MAX_WAIT = 600.0      # délai maximum d'attente de la réponse (s)
# deepseek-v4-flash

def rpc(method, payload, timeout=60.0):
    """Appelle une méthode RPC du harness et renvoie le champ `value`."""
    body = {
        "type": "client-request",
        "rpcId": str(uuid.uuid4()),
        "method": method,
        "payload": payload,
    }
    response = requests.post(f"{BASE_URL}/api/{method}", json=body, timeout=timeout)
    response.raise_for_status()
    envelope = response.json()
    result = envelope.get("result")
    if result is None:
        raise RuntimeError(f"réponse inattendue pour {method} : {envelope}")
    if not result.get("ok"):
        error = result.get("error", {})
        raise RuntimeError(f"erreur RPC {method} : [{error.get('code')}] {error.get('message')}")
    return result.get("value")


def find_or_create_session(fresh=False):
    """Renvoie une session existante libre, sinon en crée une nouvelle."""
    if not fresh:
        items = (rpc("session.list", {}) or {}).get("items", [])
        # On réutilise la conversation la plus récente si elle est libre ;
        # une session "blank" (créée mais jamais utilisée) est aussi réutilisable.
        for summary in items:
            if not summary.get("running"):
                return summary["sessionId"]
    created = rpc("session.create", {})
    return created["sessionId"]


def message_text(entry):
    """Texte des blocs 'text' d'un événement user/message ou assistant/message."""
    event = entry["event"]
    data = event.get("data", {})
    if event["type"] == "assistant/message":
        message = data.get("message", {})
    elif event["type"] == "user/message":
        message = data
    else:
        return None
    parts = []
    for block in message.get("content", []):
        if isinstance(block, dict) and block.get("type") == "text":
            parts.append(block.get("text", ""))
    return "\n".join(parts)


def send_and_wait(session_id, text):
    """Envoie `text` puis attend la réponse de l'assistant (texte final)."""
    # Séquence de fin du journal AVANT l'envoi : le tour déclenché par notre
    # prompt ne peut contenir que des événements plus récents que cette borne.
    tail = rpc("session.history", {"sessionId": session_id, "maxMessages": 1})
    tail_events = tail.get("events", [])
    tail_seq = tail_events[-1]["event"]["seq"] if tail_events else -1

    prompt_value = rpc("session.prompt", {
        "sessionId": session_id,
        "mode": "queue",
        "content": [{"type": "text", "text": text}],
    })
    # Une commande slash est exécutée par l'hôte : pas de réponse modèle.
    if prompt_value and prompt_value.get("command"):
        return prompt_value["command"].get("text") or "(commande exécutée)"

    deadline = time.monotonic() + MAX_WAIT
    started = deadline - MAX_WAIT
    last_progress = started
    while time.monotonic() < deadline:
        history = rpc("session.history", {"sessionId": session_id, "maxMessages": 100})
        events = [entry["event"] for entry in history.get("events", [])]

        # Notre prompt = premier message utilisateur après la borne, de
        # préférence celui dont le contenu correspond exactement au texte envoyé
        # (le harnais peut injecter des messages système entre-temps).
        prompt_seq = None
        for event in events:
            if event["type"] != "user/message" or event["seq"] <= tail_seq:
                continue
            if prompt_seq is None:
                prompt_seq = event["seq"]
            if message_text({"event": event}) == text:
                prompt_seq = event["seq"]
                break

        if prompt_seq is not None:
            # Fin du tour = premier turn/end après notre prompt.
            end_seq = None
            end_reason = None
            for event in events:
                if event["type"] == "turn/end" and event["seq"] > prompt_seq:
                    end_seq = event["seq"]
                    end_reason = event.get("data", {}).get("reason", {})
                    break

            if end_seq is not None:
                parts = []
                for event in events:
                    if event["type"] != "assistant/message":
                        continue
                    if not (prompt_seq < event["seq"] <= end_seq):
                        continue
                    data = event.get("data", {})
                    if data.get("interrupted"):
                        continue
                    for block in data.get("message", {}).get("content", []):
                        if isinstance(block, dict) and block.get("type") == "text":
                            parts.append(block.get("text", ""))

                reason_kind = end_reason.get("kind") if isinstance(end_reason, dict) else None
                if parts:
                    answer = "\n\n".join(parts)
                    if reason_kind in ("error", "aborted"):
                        answer += f"\n\n[fin du tour : {reason_kind}]"
                    return answer
                # Tour terminé sans texte visible (interruption, erreur…).
                return f"[réponse sans texte visible ; fin du tour : {reason_kind or '?'}]"

        # Indicateur de progression discret (toutes les 5 s).
        now = time.monotonic()
        if now - last_progress >= 5.0:
            print(f"... attente de la reponse ({int(now - started)}s)", file=sys.stderr)
            last_progress = now
        time.sleep(POLL_INTERVAL)

    raise TimeoutError(f"pas de réponse de l'assistant après {int(MAX_WAIT)} s")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    fresh = "--new" in sys.argv
    args = [arg for arg in sys.argv[1:] if arg != "--new"]

    message = "Bonjour, qui es-tu ?"
    if args:
        message = " ".join(args)

    try:
        session_id = find_or_create_session(fresh=fresh)
        print(f"[dsh] session : {session_id}", file=sys.stderr)
        print(f"[moi] {message}")
        answer = send_and_wait(session_id, message)
        print(f"[assistant] {answer}")
    except KeyboardInterrupt:
        print("\ninterrompu.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
    # print("Simulation de la conversation : → Voir code source.")
    """ Simulation de la conversation sans exécuter le main()

    [moi] Bonjour, qui es-tu ?
    [assistant] Bonjour ! 👋

    → Je suis un agent IA propulsé par le modèle **deepseek-v4-flash**, fonctionnant dans le **DeepSeek Harness** — une plateforme d'agents basée sur des plugins (construite sur Cordis).

    En bref, je peux :
    - 🛠️ **Travailler sur le dépôt** `C:\\ai\\dsh` (écrire du code, lancer des tests, des builds, etc.)
    - 🌐 **Rechercher sur le web** pour des informations actuelles
    - 📂 **Manipuler des fichiers** (lire, écrire, éditer)
    - 🤖 **Déléguer des tâches** à des sous-agents en arrière-plan
    - ✅ **Gérer des objectifs** à long terme

    OU :

    → Je suis un **agent IA** fonctionnant dans le **DeepSeek Harness**, propulsé par le modèle **deepseek-v4-flash**.

    Je peux vous aider avec :
    - **Le développement** dans ce dépôt (`C:\ai\dsh`) — code, tests, builds
    - **La recherche web** pour des infos à jour
    - **La manipulation de fichiers** — lecture, écriture, édition
    - **La délégation** de tâches à des sous-agents
    - **Des objectifs à long terme** suivis sur plusieurs étapes

Comment puis-je vous aider ?
    Si vous avez besoin d'aide pour développer, déboguer, documenter ou analyser quelque chose dans ce projet, je suis là ! Que puis-je faire pour vous ?
    """

