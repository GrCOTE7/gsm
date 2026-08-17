import os

from env_config import load_env
from cli_spawner import spawn_cli_if_needed, place_cli_window
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


def _spawn_app_detached(app: str, env: dict, mode: str):
    """Lance une app dans son PROPRE process (mode multi-apps sans CLI dédiée).

    `run_flet` est bloquant (l'app reste liée au cycle de vie de la CLI) : il
    ne peut donc y avoir qu'UN run_flet par process. On relance ce pipeline en
    mode interne "_<app>_nocli" : l'enfant hérite de la console courante (logs
    visibles) et sa fermeture (CTRL+C / croix) fermera l'app via run_flet.
    """
    import subprocess
    import sys

    subprocess.Popen([sys.executable, str(MAIN_PY), child_arg(app, mode, "nocli")])


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
            # Parent : ouvre la console dédiée — créée à proximité de la bonne
            # position par cli_spawner. C'est elle qui relance ce pipeline en
            # mode interne (_gsm_child) et lance Flet.
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
