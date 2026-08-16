"""Démo interactive : les 10 combinaisons distinctes de lancement (./go).

Pour chaque combinaison :
  1. ajuste temporairement GSM_WINDOW_CLI / UPU_WINDOW_CLI dans le .env
  2. lance l'app (ou les apps) via scripts/app_window/main.py
  3. affiche la config en CLI
  4. attend qu'une touche soit pressée avant la config suivante
  5. nettoie les process de l'app ET ferme les CLI dédiées (fenêtres wt)

Le focus est systématiquement ramené sur la console de la démo avant chaque
prompt (les fenêtres des apps volent le focus à l'ouverture).
À la fin (ou sur Ctrl+C / 'q') le .env d'origine est restauré.

Usage :
  python scripts/app_window/demo_configs.py
"""

import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT / ".env"
MAIN_PY = ROOT / "scripts" / "app_window" / "main.py"
PYTHON = sys.executable

# Les 10 combinaisons réellement distinctes : (mode, gsm_cli, upu_cli, description)
CONFIGS = [
    ("",   0, 0, "GSM app — sans CLI dédiée"),
    ("",   1, 0, "GSM app — CLI dédiée"),
    ("w",  0, 0, "GSM web — sans CLI dédiée"),
    ("w",  1, 0, "GSM web — CLI dédiée"),
    ("u",  0, 0, "UPU app — sans CLI dédiée"),
    ("u",  0, 1, "UPU app — CLI dédiée"),
    ("gu", 0, 0, "GSM + UPU app — sans CLI"),
    ("gu", 0, 1, "GSM + UPU app — CLI UPU seule"),
    ("gu", 1, 0, "GSM + UPU app — CLI GSM seule"),
    ("gu", 1, 1, "GSM + UPU app — CLI GSM + UPU"),
]

# Fenêtres présentes AVANT la démo : on ne fermera que les fenêtres CLI
# dédiées créées PENDANT la démo (pas les terminaux de l'utilisateur).
_BASELINE_HWNDS: set = set()


# ---------------------------------------------------------------------------
# .env
# ---------------------------------------------------------------------------

def _set_cli_values(gsm_cli: int, upu_cli: int) -> None:
    """Remplace les valeurs de GSM_WINDOW_CLI / UPU_WINDOW_CLI dans le .env,
    en conservant les commentaires et la mise en forme."""
    text = ENV_PATH.read_text(encoding="utf-8")
    text = re.sub(r"^(GSM_WINDOW_CLI\s*=\s*)\d+", rf"\g<1>{gsm_cli}", text, flags=re.M)
    text = re.sub(r"^(UPU_WINDOW_CLI\s*=\s*)\d+", rf"\g<1>{upu_cli}", text, flags=re.M)
    ENV_PATH.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# Process & fenêtres (Windows)
# ---------------------------------------------------------------------------

PYTHON_APP_PATTERNS = ("*main_gsm*", "*main_upu*", "*flet.cli*", "*app_window\\main.py*")
UV_APP_PATTERNS = ("*main_gsm*", "*main_upu*")
PWSH_CLI_PATTERNS = ("*go.ps1 _gsm_child*", "*go.ps1 _upu_child*")


def _ps(script: str) -> None:
    subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _kill_matching(image: str, patterns) -> None:
    cond = " -or ".join(f"$_.CommandLine -like '{p}'" for p in patterns)
    script = (
        f"Get-CimInstance Win32_Process -Filter \"Name='{image}'\" | "
        f"Where-Object {{ {cond} }} | "
        "ForEach-Object { taskkill /PID $_.ProcessId /T /F 2>$null | Out-Null }"
    )
    _ps(script)


def _count_app_processes() -> int:
    cond = " -or ".join(f"$_.CommandLine -like '{p}'" for p in ("*main_gsm*", "*main_upu*"))
    script = (
        f"(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
        f"Where-Object {{ {cond} }} | Measure-Object).Count"
    )
    out = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
        capture_output=True, text=True,
    ).stdout.strip()
    return int(out) if out.isdigit() else 0


def _capture_baseline() -> None:
    """Mémorise les fenêtres visibles AVANT la démo."""
    global _BASELINE_HWNDS
    _BASELINE_HWNDS = set()
    if os.name != "nt":
        return
    try:
        import win32gui

        def _cb(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                _BASELINE_HWNDS.add(hwnd)
            return True

        win32gui.EnumWindows(_cb, None)
    except Exception:
        _BASELINE_HWNDS = set()


def _close_dedicated_cli_windows() -> None:
    """Ferme (WM_CLOSE) les fenêtres CLI dédiées créées PENDANT la démo.

    Tuer le shell pwsh ne suffit pas : la fenêtre Windows Terminal (classe
    CASCADIA_HOSTING_WINDOW_CLASS) reste ouverte. On la ferme par WM_CLOSE,
    en excluant les fenêtres déjà présentes avant la démo (baseline) et la
    console de la démo elle-même.
    """
    if os.name != "nt":
        return
    try:
        import ctypes
        import win32con
        import win32gui
    except ImportError:
        return

    my_console = ctypes.windll.kernel32.GetConsoleWindow()
    console_classes = ("CASCADIA_HOSTING_WINDOW_CLASS", "ConsoleWindowClass")

    def _cb(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return True
        if hwnd in _BASELINE_HWNDS or hwnd == my_console:
            return True
        cls = win32gui.GetClassName(hwnd)
        title = win32gui.GetWindowText(hwnd)
        if cls in console_classes or "pwsh.EXE" in title:
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        return True

    win32gui.EnumWindows(_cb, None)


def _focus_cli() -> None:
    """Ramène le focus sur la console de la démo (les apps volent le focus à
    l'ouverture — on le récupère avant chaque prompt)."""
    if os.name != "nt":
        return
    try:
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        kernel32.GetConsoleWindow.restype = wintypes.HWND
        user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]

        hwnd = kernel32.GetConsoleWindow()
        if not hwnd:
            return
        user32.ShowWindow(hwnd, 9)  # SW_RESTORE

        fg = user32.GetForegroundWindow()
        attached = False
        if fg:
            tid_fg = user32.GetWindowThreadProcessId(fg, None)
            tid_cur = kernel32.GetCurrentThreadId()
            attached = bool(user32.AttachThreadInput(tid_cur, tid_fg, True))
        user32.SetForegroundWindow(hwnd)
        if attached:
            user32.AttachThreadInput(tid_cur, tid_fg, False)
    except Exception:
        pass


def cleanup_config() -> None:
    """Ferme les CLI dédiées + tue les process de la config courante."""
    if os.name != "nt":
        subprocess.run(["pkill", "-f", "main_gsm|main_upu|flet.cli|flet run"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return
    _close_dedicated_cli_windows()
    _kill_matching("python.exe", PYTHON_APP_PATTERNS)
    _kill_matching("uv.exe", UV_APP_PATTERNS)
    _kill_matching("pwsh.exe", PWSH_CLI_PATTERNS)
    _ps("taskkill /IM flet.exe /F 2>$null | Out-Null")


def wait_for_apps(timeout: float = 30.0) -> None:
    """Attend que les apps (process main_gsm / main_upu) soient démarrées."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _count_app_processes() > 0:
            time.sleep(2.0)  # laisse les fenêtres se dessiner
            return
        time.sleep(1.0)
    print("    [warn] apps non détectées après le délai — on continue quand même.")


# ---------------------------------------------------------------------------
# Boucle principale
# ---------------------------------------------------------------------------

def main() -> int:
    if not ENV_PATH.exists():
        print(f"[ERREUR] Fichier .env introuvable : {ENV_PATH}")
        return 1

    original_env = ENV_PATH.read_text(encoding="utf-8")
    log_files: list[str] = []
    _capture_baseline()

    print("Démo des 10 combinaisons distinctes de lancement.")
    print(f"{len(CONFIGS)} configs vont se succéder — appuie sur Entrée pour passer à la suivante.")
    print("Ferme les fenêtres quand tu as observé la config.")
    print()

    try:
        cleanup_config()  # état initial propre (ferme aussi les CLI orphelines)
        for idx, (mode, gsm_cli, upu_cli, desc) in enumerate(CONFIGS, start=1):
            _set_cli_values(gsm_cli, upu_cli)

            print("=" * 72)
            print(f"=== Config {idx}/{len(CONFIGS)} : {desc}")
            print(f"    ./go {mode or '(aucune option)'}  |  GSM_WINDOW_CLI={gsm_cli}  "
                  f"UPU_WINDOW_CLI={upu_cli}")
            print("=" * 72)
            print("    Lancement des fenêtres...")

            cmd = [PYTHON, str(MAIN_PY)]
            if mode:
                cmd.append(mode)

            # La sortie des apps va dans un log temporaire : la console de la
            # démo reste réservée aux instructions.
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".log", prefix=f"demo_{idx}_", delete=False, encoding="utf-8"
            ) as f:
                log_files.append(f.name)
                subprocess.Popen(cmd, cwd=str(ROOT), stdout=f, stderr=f)

            wait_for_apps()

            print("    Fenêtres ouvertes — observe la config.")
            _focus_cli()
            while True:
                answer = input(
                    "    Appuie sur Entrée pour la config suivante "
                    "('q' + Entrée pour quitter)... "
                )
                if answer.strip().lower() in ("q", "quit"):
                    cleanup_config()
                    raise KeyboardInterrupt
                break

            cleanup_config()
            time.sleep(2.0)  # laisse les fenêtres se fermer avant la suivante
            print()
    except KeyboardInterrupt:
        print("\n[INFO] Arrêt demandé.")
    finally:
        ENV_PATH.write_text(original_env, encoding="utf-8")
        for log in log_files:
            try:
                os.remove(log)
            except OSError:
                pass
        print(f"[INFO] .env restauré à sa valeur d'origine.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
