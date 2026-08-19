import os
import time
from pathlib import Path

from env_config import load_env
from cli_spawner import spawn_cli_if_needed, place_cli_window, _close_stale_cli
from flet_runner import run_flet, _build_flet_command, _resolve_main_file
from common import MAIN_PY, CLI_TOP, CLI_WIDTH, CLI_HEIGHT, child_arg


def debug_dump(action, env):
    print("=== MODE DEBUG ===")
    print("[ACTION] Apps :", action["apps"], "-", "[ACTION] Mode :", action["mode"])
    print()

    print("[ENV] Variables chargées (Concernant les fenêtres):")
    for k, v in env.items():
        # if 'WINDOW' in k:
        print(f"\t{k} = {v}")
    print()

    print("[WINDOW] Fenêtres qui seraient préparées :")
    for app in action["apps"]:
        print(f"    - {app}")
    print()

    print("[CLI] CLI dédiée :")
    for app in action["apps"]:
        cli_flag = env.get(f"{app.upper()}_WINDOW_CLI", 0)
        print(f"    - {app} : {'OUI' if cli_flag == 1 else 'NON'}")
    print()

    print("[FLET] Commandes qui seraient exécutées :")
    for app in action["apps"]:
        cmd = _build_flet_command(_resolve_main_file(app), action["mode"])
        print(f"    - {' '.join(cmd)}")
    print()

    print("=== FIN DEBUG ===")


def _spawn_app_detached(app: str, env: dict, mode: str, suffix: str = "nocli"):
    """Lance une app dans son PROPRE process (non bloquant pour le parent).

    `run_flet` est bloquant (l'app reste liée au cycle de vie de la CLI) : il
    ne peut donc y avoir qu'UN run_flet par process. On relance ce pipeline en
    mode interne "_<app>_<suffix>_" :
    - suffix "nocli" : enfant détaché en mode multi-apps SANS CLI dédiée
      (./go gu sans *_WINDOW_CLI) — n'hérite que de la console, ne la
      repositionne pas ;
    - suffix "child" : enfant d'une CLI dédiée RÉUTILISÉE (./go gu relancé
      depuis une CLI dédiée) — hérite de la console courante, la repositionne
      (place_cli_window) puis lance Flet.
    """
    import subprocess
    import sys

    subprocess.Popen([sys.executable, str(MAIN_PY), child_arg(app, mode, suffix)])


def _reuse_current_cli(app: str, action: dict) -> bool:
    """Vrai si la CLI dédiée COURANTE doit être réutilisée pour `app`.

    Marqueur posé par cli_spawner (GSM_DEDICATED_CLI) quand il ouvre une CLI
    dédiée : on est alors dans la console de cette CLI (relance de ./go).
    - mono-app → la CLI courante est toujours réutilisée ;
    - multi-app (./go gu) → seule l'app que la CLI courante héberge déjà
      (GSM_DEDICATED_CLI_APP) est réutilisée — l'autre est spawnée.
    """
    if os.environ.get("GSM_DEDICATED_CLI") != "1":
        return False
    if len(action["apps"]) == 1:
        return True
    return os.environ.get("GSM_DEDICATED_CLI_APP", "") == app


def _should_close_stale_cli(app: str) -> bool:
    """Vrai s'il faut remplacer une ancienne CLI dédiée de `app` avant d'en ouvrir
    une nouvelle.

    On est dans une CLI dédiée (relance de ./go depuis cette console) et l'app
    cible n'est pas la CLI courante. L'existence réelle d'une CLI de `app` est
    vérifiée par _close_stale_cli (filtre Get-CimInstance sur 'go.ps1 _<app>_child') :
    inutile de dépendre de marqueurs hérités (absents sur les CLI créées avant).
    """
    if os.environ.get("GSM_DEDICATED_CLI") != "1":
        return False
    return os.environ.get("GSM_DEDICATED_CLI_APP", "") != app


# ---------------------------------------------------------------------------
# Lien entre les CLI dédiées (./go gu) : fichiers .pid + flag de remplacement.
# ---------------------------------------------------------------------------

def _cli_pid_file(app: str) -> Path:
    """Fichier .pid écrit par go.ps1 pour une CLI dédiée (mode _<app>_child)."""
    tmp = os.environ.get("TEMP", os.environ.get("TMP", ""))
    return Path(tmp) / f"gsm_cli_{app.lower()}.pid"


def _read_pid(app: str) -> int | None:
    f = _cli_pid_file(app)
    if not f.exists():
        return None
    try:
        return int(f.read_text(encoding="ascii").strip())
    except ValueError:
        return None


def _set_replacing_flag(on: bool) -> None:
    """Flag partagé : un remplacement de CLI dédiée est en cours. Le watcher de
    liaison (cli_watcher.ps1) ne doit PAS interpréter la mort de l'ancienne CLI
    comme une fermeture de l'autre CLI."""
    flag = Path(os.environ.get("TEMP", os.environ.get("TMP", ""))) / "gsm_cli_replacing"
    if on:
        flag.write_text("1", encoding="ascii")
    else:
        flag.unlink(missing_ok=True)


def _wait_for_new_cli_pid(app: str, old_pid: int | None, timeout: float = 12.0) -> None:
    """Attend que la NOUVELLE CLI de `app` ait écrit son .pid (≠ ancien PID)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        cur = _read_pid(app)
        if cur is not None and cur != old_pid:
            return
        time.sleep(0.3)


def _apply_upu_alone(env: dict) -> None:
    """./go u (UPU SEULE) : UPU prend la place de GSM.

    En mode normal (./go gu), UPU s'ouvre à UPU_WINDOW_LEFT (à côté de GSM).
    Quand UPU est seule, il n'y a pas de GSM à côté : inutile de laisser vide
    la place de GSM — UPU s'ouvre donc à GSM_WINDOW_LEFT (ex: 1913), avec ou
    sans CLI dédiée.

    Implémentation : le parent pose UPU_ALONE=1 (hérité par la CLI dédiée et
    l'app), puis on force UPU_WINDOW_LEFT := GSM_WINDOW_LEFT dans env +
    os.environ. L'enfant CLI relit le .env (UPU_WINDOW_LEFT=2445) dans son
    propre launch_app : le flag hérité réapplique alors le même forçage
    (idempotent).
    """
    if os.environ.get("UPU_ALONE") == "1":
        gsm_left = int(
            env.get("GSM_WINDOW_LEFT", os.environ.get("GSM_WINDOW_LEFT", "1913"))
        )
        env["UPU_WINDOW_LEFT"] = gsm_left
        os.environ["UPU_WINDOW_LEFT"] = str(gsm_left)


def launch_app(action: dict):
    env = load_env()

    if action["mode"] == "debug":
        debug_dump(action, env)
        return

    # UPU seule (./go u) : flag posé par le parent, puis appliqué partout
    # (parent, enfant CLI, app) de façon idempotente.
    if action["apps"] == ["upu"] and not action.get("internal_child"):
        os.environ["UPU_ALONE"] = "1"
    _apply_upu_alone(env)

    for app in action["apps"]:
        cli_key = f"{app.upper()}_WINDOW_CLI"
        cli_flag = int(env.get(cli_key, 0))

        if cli_flag == 1 and not action.get("internal_child"):
            # CLI dédiée courante réutilisée (relance depuis une CLI dédiée) :
            # mono-app → en place (positionnement + Flet bloquant) ;
            # multi-app → enfant détaché (_<app>_child) pour ne pas bloquer la
            # boucle qui doit encore spawner l'autre app.
            if _reuse_current_cli(app, action):
                print(
                    f"[CLI] CLI dédiée courante réutilisée pour {app} "
                    "(relance depuis la CLI) — aucune nouvelle fenêtre."
                )
                if len(action["apps"]) == 1:
                    # L'app demandée avait déjà une CLI dédiée ailleurs ?
                    # (ex: ./go u relancé depuis la CLI GSM alors qu'une CLI
                    # UPU existe encore) → on la ferme avant de la remplacer
                    # par la CLI courante, en rompant d'abord le lien de la
                    # CLI courante (elle change d'app).
                    if _should_close_stale_cli(app):
                        _set_replacing_flag(True)
                        try:
                            current = os.environ.get("GSM_DEDICATED_CLI_APP", "")
                            if current:
                                # Supprime le .pid de la CLI courante : son
                                # watcher de liaison sort (il verrait la mort
                                # de l'ancienne CLI comme une fermeture).
                                _cli_pid_file(current).unlink(missing_ok=True)
                            _close_stale_cli(app)
                            # Laisse le watcher constater la rupture de lien.
                            time.sleep(2.5)
                        finally:
                            _set_replacing_flag(False)
                    left = int(env.get(f"{app.upper()}_WINDOW_LEFT", 0))
                    place_cli_window(
                        left=left, top=CLI_TOP, width=CLI_WIDTH, height=CLI_HEIGHT
                    )
                    run_flet(app, env, action["mode"])
                else:
                    # Multi-app : run_flet est bloquant → on relaie à un enfant
                    # détaché qui se charge de cette CLI (positionnement +
                    # Flet), et le parent continue pour spawner l'autre app.
                    _spawn_app_detached(app, env, action["mode"], suffix="child")
            else:
                # Une CLI dédiée de `app` existe peut-être encore ailleurs
                # (relance de ./go gu depuis une CLI dédiée) : on la remplace
                # pour ne jamais avoir de CLI en trop.
                if _should_close_stale_cli(app):
                    # Flag pour le watcher de liaison : remplacement planifié,
                    # pas une vraie fermeture de CLI.
                    _set_replacing_flag(True)
                    try:
                        old_pid = _read_pid(app)
                        _close_stale_cli(app)
                        # Parent : ouvre la console dédiée — créée à proximité
                        # de la bonne position par cli_spawner. C'est elle qui
                        # relance ce pipeline en mode interne (_gsm_child) et
                        # lance Flet.
                        spawn_cli_if_needed(app, env, action["mode"])
                        # Attend que la nouvelle CLI écrive son .pid, puis
                        # relâche le flag (sinon le watcher croirait à une
                        # fermeture).
                        _wait_for_new_cli_pid(app, old_pid)
                    finally:
                        _set_replacing_flag(False)
                else:
                    spawn_cli_if_needed(app, env, action["mode"])
        elif action.get("internal_child"):
            # Enfant : repositionne la fenêtre du terminal sous l'app (pixels
            # exacts, comme go_ori.ps1) SAUF si c'est un enfant détaché sans
            # CLI dédiée (_gsm_nocli), puis lance Flet (bloquant).
            if not action.get("skip_cli_placement"):
                left = int(env.get(f"{app.upper()}_WINDOW_LEFT", 0))
                place_cli_window(
                    left=left, top=CLI_TOP, width=CLI_WIDTH, height=CLI_HEIGHT
                )
            run_flet(app, env, action["mode"])
        else:
            # Mode sans CLI : Flet se lance et se positionne tout seul
            # (window_config de l'app). run_flet est bloquant (lié à la CLI) :
            # en mode multi-apps, chaque app doit donc tourner dans son PROPRE
            # process, sinon la 1ère bloquerait et les suivantes ne seraient
            # jamais lancées.
            if len(action["apps"]) > 1:
                _spawn_app_detached(app, env, action["mode"])
            else:
                run_flet(app, env, action["mode"])
