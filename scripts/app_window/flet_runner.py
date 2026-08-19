"""Lancement Flet (bloquant) + cycle de vie lié à la CLI courante."""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from common import ROOT


def run_flet(app: str, env: dict, mode: str) -> None:
    """Lance Flet pour l'application GSM ou UPU, puis reste bloqué.

    Le launcher reste BLOQUÉ tant que l'application Flet tourne. Fermer la
    console CLI (CTRL+C, croix, exit...) doit fermer aussi l'application :
    - CTRL+C → KeyboardInterrupt → on tue l'arborescence Flet (taskkill /T /F) ;
    - Croix / logoff / shutdown → handler de console (Windows) qui tue l'app ;
    - Linux → SIGINT/SIGHUP atteignent naturellement tout le groupe de process.
    """
    main_file = _resolve_main_file(app)
    if not main_file.exists():
        print(f"[FLET][ERROR] Fichier introuvable : {main_file}")
        return

    print(f"[FLET] Lancement de {app.upper()} -> {mode.upper()}")
    cmd = _build_flet_command(main_file, mode)
    print(f"[FLET] Commande : {' '.join(cmd)}")

    proc = None
    try:
        # cwd = racine du dépôt : `uv run` (sans --active) doit y trouver le
        # projet (pyproject.toml / uv.lock) pour resynchroniser l'environnement.
        proc = subprocess.Popen(cmd, cwd=str(ROOT))
        print(
            "[FLET] Process lancé — l'application restera liée à cette CLI "
            "(la fermer fermera l'app)."
        )

        if platform.system() == "Windows":
            _watchdog_console_close(proc)

        proc.wait()
        print("[FLET] Process terminé.")
    except KeyboardInterrupt:
        # L'utilisateur ferme la CLI (CTRL+C) : le `finally` ci-dessous tue
        # l'arborescence Flet encore vivante.
        print()
        print("[FLET] Interruption reçue — fermeture de l'application.")
    except Exception as exc:
        print(f"[FLET][ERROR] Impossible de lancer Flet : {exc}")
    finally:
        # Garantie : l'app ne survit JAMAIS à sa CLI. Si le process tourne
        # encore à ce stade (interruption, erreur), on tue toute l'arborescence.
        if proc is not None and proc.poll() is None:
            _terminate_process_tree(proc.pid)


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------


def _watchdog_console_close(proc: subprocess.Popen) -> None:
    """Ferme l'app quand la console CLI est fermée (croix, logoff, shutdown...).

    Le CTRL+C, lui, est déjà géré par Python (KeyboardInterrupt → `finally` de run_flet). Ici on couvre les événements de console qui tueraient ce launcher SANS exécuter `finally` : on tue alors explicitement l'arborescence Flet (taskkill /T /F) avant de laisser le comportement par défaut se produire.
    """
    try:
        import win32api
        import win32con

        close_events = (
            win32con.CTRL_CLOSE_EVENT,
            win32con.CTRL_LOGOFF_EVENT,
            win32con.CTRL_SHUTDOWN_EVENT,
            win32con.CTRL_BREAK_EVENT,
        )

        def _handler(ctrl_type):
            if ctrl_type in close_events:
                _terminate_process_tree(proc.pid)
            # False : on laisse le gestionnaire par défaut terminer ce launcher.
            return False

        win32api.SetConsoleCtrlHandler(_handler, True)
    except Exception as exc:
        print(f"[FLET][WARN] Watchdog console indisponible : {exc}")


def _terminate_process_tree(pid: int) -> None:
    """Tue toute l'arborescence du process (taskkill /T /F). Best-effort."""
    try:
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
    except Exception:
        pass


def _resolve_main_file(app: str) -> Path:
    """Retourne le fichier main_gsm.py ou main_upu.py."""
    return ROOT / "src" / f"main_{app.lower()}.py"


def _build_flet_command(main_file: Path, mode: str) -> list[str]:
    """Construit la commande Flet selon le mode (APP → desktop, WEB → web)."""
    uv_exe = _find_uv_executable()
    if uv_exe:
        # Sans `--active` : `uv run` resynchronise l'environnement (pyproject +
        # uv.lock) avant d'exécuter. Indispensable en mode WEB : le paquet
        # `flet-web` doit être installé, et le fallback d'auto-installation du
        # CLI Flet échoue car les venv gérés par uv n'embarquent pas `pip`.
        cmd = [uv_exe, "run"]
        for extra in _required_extras(mode):
            cmd += ["--extra", extra]
        cmd += [
            "python",
            "-m",
            "flet.cli",
            "run",
            str(main_file),
            "-r",  # --recursive : hot reload (mode "release" de la doc flet)
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
            "-r",  # --recursive : hot reload
        ]

    if mode == "web":
        cmd.append("--web")

    return cmd


def _required_extras(mode: str) -> list[str]:
    """Extras uv à resynchroniser : toujours desktop, plus web en mode WEB."""
    extras = ["desktop"]
    if mode == "web":
        extras.append("web")
    return extras


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

