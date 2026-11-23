"""Point d'entrée du launcher : lit l'option CLI et délègue à launch_app."""

import sys

from app_launcher import launch_app
from mode_resolver import resolve_mode

# Les consoles Windows (cp1252) peuvent faire planter les print contenant des
# caractères non-ASCII (→, …) : on force UTF-8 avec remplacement sûr.
for _stream in (sys.stdout, sys.stderr):
    # `reconfigure` n'existe que sur io.TextIOWrapper (pas sur TextIO,
    # d'où le getattr pour rester compatible et satisfaire Pylance).
    _reconfigure = getattr(_stream, "reconfigure", None)
    if _reconfigure is not None:
        try:
            _reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main() -> int:
    """Lance les apps demandées par l'option CLI ('' | w | u | gu | debug)."""
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    action = resolve_mode(mode)
    try:
        launch_app(action)
    except KeyboardInterrupt:
        # CTRL+C tombant après la fermeture de l'app : sortie propre.
        print()
        print("[GSM] Fermeture demandée.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
