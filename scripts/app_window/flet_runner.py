import platform
import subprocess
import sys
from pathlib import Path


def run_flet(app: str, env: dict, mode: str):
    """
    Lance Flet pour l'application GSM ou UPU.
    - app: "gsm" ou "upu"
    - mode: "web" ou "app"
    """

    main_file = _resolve_main_file(app)
    if not main_file.exists():
        print(f"[FLET][ERROR] Fichier introuvable : {main_file}")
        return

    print(f"[FLET] Lancement de {app.upper()} -> {mode.upper()}")

    # Commande Flet
    cmd = _build_flet_command(main_file, mode)

    print(f"[FLET] Commande : {' '.join(cmd)}")

    try:
        subprocess.Popen(cmd)
        print("[FLET] Process lancé.")
    except Exception as e:
        print(f"[FLET][ERROR] Impossible de lancer Flet : {e}")


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------


def _resolve_main_file(app: str) -> Path:
    """Retourne le fichier main_gsm.py ou main_upu.py."""
    base = Path(__file__).resolve().parents[2]
    return base / "src" / f"main_{app.lower()}.py"


def _build_flet_command(main_file: Path, mode: str):
    """
    Construit la commande Flet selon le mode.
    - Mode APP → desktop
    - Mode WEB → web
    """

    # 'uv' n'est pas garanti sur le PATH (fenêtre CLI dédiée wt.exe) : on passe
    # par l'interpréteur Python courant (venv du projet) qui contient déjà flet.
    cmd = [
        sys.executable,
        "-m",
        "flet.cli",
        "run",
        str(main_file),
        "-r",  # release mode
    ]

    if mode == "web":
        cmd.append("--web")

    return cmd
