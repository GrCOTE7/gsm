import sys
from datetime import datetime

from mode_resolver import resolve_mode
from app_launcher import launch_app

# Lancer avec : uv run flet run scripts/app_window/main.py -r

# Les consoles Windows (cp1252) peuvent faire planter les print contenant des
# caractères non-ASCII (→, …) : on force UTF-8 avec remplacement sûr.
for stream in (sys.stdout, sys.stderr):
    try:
        # `reconfigure` n'existe que sur io.TextIOWrapper (pas sur TextIO,
        # d'où le getattr pour rester compatible et satisfaire Pylance).
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# sys.argv.append("u")  # Simulation ""./go essai"


def get_mode():
    """Retourne le mode demandé : '', 'w', 'u', 'gu'."""
    args = sys.argv[1:]
    return args[0].lower() if args else ""


def main():
    mode = get_mode()
    action = resolve_mode(mode)
    try:
        launch_app(action)
    except KeyboardInterrupt:
        # CTRL+C tombant après la fermeture de l'app : sortie propre, sans traceback.
        print()
        print("[GSM] Fermeture demandée.")
        return 1
    return 0


if __name__ == "__main__":
    rc = main()
    print(f"{datetime.now().strftime('%H:%M:%S')} > ", end="")
    sys.exit(rc)
