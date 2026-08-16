import platform
import os
import shutil
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

    uv_exe = _find_uv_executable()
    if uv_exe:
        cmd = [
            uv_exe,
            "run",
            "--active",
            "python",
            "-m",
            "flet.cli",
            "run",
            str(main_file),
            "-r",  # release mode
        ]
    else:
        print(
            "[FLET][WARN] uv introuvable: fallback vers l'interpréteur Python courant."
        )
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


def _find_uv_executable() -> str | None:
    """Retourne le chemin de uv, même si le PATH est limité (wt.exe)."""
    # 1) PATH courant
    for candidate in ("uv", "uv.exe"):
        exe = shutil.which(candidate)
        if exe:
            return exe

    # 2) Emplacements usuels Windows (alias Windows Store / install user)
    if platform.system() == "Windows":
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        user_profile = os.environ.get("USERPROFILE", "")
        candidates = [
            os.path.join(local_app_data, "Microsoft", "WindowsApps", "uv.exe"),
            os.path.join(user_profile, ".local", "bin", "uv.exe"),
        ]
        for path in candidates:
            if path and os.path.exists(path):
                return path

    return None
