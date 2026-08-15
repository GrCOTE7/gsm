from env_config import load_env
from window_manager import prepare_window
# from cli_spawner import spawn_cli_if_needed
# from flet_runner import run_flet_app


def debug_dump(action, env):
    print("=== MODE DEBUG ===")
    print("[ACTION] Apps :", action["apps"], '-',"[ACTION] Mode :", action["mode"])
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
        print(f"    - uv run python -m flet.cli run main_{app}.py -r")
    print()

    print("=== FIN DEBUG ===")


def launch_app(action: dict):
    """
    action = {
        "apps": ["gsm", "upu"],
        "mode": "app" | "web" | "debug"
    }
    """

    # 1. Charger .env
    env = load_env()

    # 2. Mode DEBUG → ne rien lancer, juste afficher
    if action["mode"] == "debug":
        debug_dump(action, env)
        return

    # 3. Pour chaque app à lancer
    for app in action["apps"]:

        # Préparer la fenêtre (Windows uniquement)
        prepare_window(app, env)

        # Spawn CLI dédiée si nécessaire
        spawn_cli_if_needed(app, env)

        # Lancer l'app Flet
        run_flet_app(app, action["mode"])
