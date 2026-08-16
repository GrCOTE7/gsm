import sys
from datetime import datetime

from mode_resolver import resolve_mode
from app_launcher import launch_app

# Lancer avec : uv run flet run scripts/app_window/main.py -r

# Les consoles Windows (cp1252) peuvent faire planter les print contenant des
# caractères non-ASCII (→, …) : on force UTF-8 avec remplacement sûr.
for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
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
    launch_app(action)


if __name__ == "__main__":
    main()
    print(f"{datetime.now().strftime('%H:%M:%S')} > ", end="")
