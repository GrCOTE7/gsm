import requests, uuid, time

BASE = "http://127.0.0.1:3080"

def rpc(method, payload):
    body = {"type": "client-request", "rpcId": str(uuid.uuid4()),
            "method": method, "payload": payload}
    r = requests.post(f"{BASE}/api/{method}", json=body, timeout=60)
    r.raise_for_status()
    result = r.json()["result"]
    if not result["ok"]:
        raise Exception(result["error"])
    return result["value"]

def ask(question):
    # 1. Créer une session
    session_id = rpc("session.create", {})["sessionId"]
    # 2. Envoyer le prompt
    rpc("session.prompt", {"sessionId": session_id, "mode": "queue",
                           "content": [{"type": "text", "text": question}]})
    # 3. Attendre la fin du tour
    while True:
        hist = rpc("session.history", {"sessionId": session_id, "maxMessages": 20})
        events = hist.get("events", [])
        # Chercher le premier turn/end
        for ev in events:
            if ev["event"]["type"] == "turn/end":
                # Récupérer le dernier message assistant avant ce turn/end
                # (simplification : on prend le dernier texte trouvé)
                answer = ""
                for prev in events:
                    if prev["event"]["seq"] < ev["event"]["seq"] and prev["event"]["type"] == "assistant/message":
                        for block in prev["event"]["data"].get("message", {}).get("content", []):
                            if block.get("type") == "text":
                                answer = block["text"]
                return answer
        time.sleep(0.5)

if __name__ == "__main__":
    print(ask("Bonjour, qui es-tu ?"))