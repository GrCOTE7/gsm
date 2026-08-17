import sys

from mode_resolver import resolve_mode
from app_launcher import launch_app

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


def get_mode():
    """Retourne le mode demandé : '', 'w', 'u', 'gu', 'debug'."""
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
    sys.exit(main())
