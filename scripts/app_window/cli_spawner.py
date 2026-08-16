import os
import platform
import shutil
import subprocess
import time
from pathlib import Path

if platform.system() == "Windows":
    import win32gui
    import win32process
    import win32con
    import win32api


def _find_flet_pid():
    candidates = []

    def enum_handler(hwnd, lParam):
        if not win32gui.IsWindowVisible(hwnd):
            return True

        title = win32gui.GetWindowText(hwnd)
        if not title:
            return True

        # Fenêtres Flet typiques
        if "flet" in title.lower() or "upu" in title.lower() or "gsm" in title.lower():
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            candidates.append(pid)
            return False

        return True

    win32gui.EnumWindows(enum_handler, None)

    return candidates[0] if candidates else None


def _find_flet_window_by_pid(pid):
    result = []

    def enum_handler(hwnd, lParam):
        if not win32gui.IsWindowVisible(hwnd):
            return True

        _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
        if window_pid == pid:
            result.append(hwnd)
            return False

        return True

    win32gui.EnumWindows(enum_handler, None)

    return result[0] if result else None


def spawn_cli_if_needed(app: str, env: dict, mode: str):
    """
    Ouvre une console dédiée sous la fenêtre Flet.
    - Si *_WINDOW_CLI = 0 → no-op
    - Windows → spawn PowerShell
    - Linux → spawn gnome-terminal / xterm
    """

    cli_key = f"{app.upper()}_WINDOW_CLI"
    cli_flag = int(env.get(cli_key, 0))

    if cli_flag == 0:
        print(f"[CLI] Pas de console dédiée pour {app}.")
        return

    if platform.system() == "Windows":
        _spawn_cli_windows(app, env, mode)
    else:
        _spawn_cli_linux(app)


# ---------------------------------------------------------------------------
# WINDOWS IMPLEMENTATION
# ---------------------------------------------------------------------------


def _find_wt_exe() -> str:
    """Retourne le chemin complet de wt.exe (Windows Terminal)."""
    exe = shutil.which("wt.exe")
    if exe:
        return exe
    # Fallback : alias d'exécution Windows Store
    fallback = os.path.join(
        os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WindowsApps", "wt.exe"
    )
    if os.path.exists(fallback):
        return fallback
    return "wt.exe"


def _find_pwsh_exe() -> str:
    """Retourne le chemin complet de pwsh.exe.

    IMPORTANT : wt.exe (Windows Terminal) ne résout PAS 'pwsh' via le PATH
    lorsqu'il crée le processus de l'onglet : il faut lui donner le chemin
    absolu (sinon erreur 0x80070002 « fichier introuvable » à l'ouverture).
    """
    exe = shutil.which("pwsh")
    if exe:
        return exe
    # Fallbacks : emplacements standard d'installation de PowerShell 7
    candidates = [
        os.path.join(
            os.environ.get("ProgramFiles", r"C:\Program Files"),
            "PowerShell",
            "7",
            "pwsh.exe",
        ),
        os.path.join(
            os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
            "PowerShell",
            "7",
            "pwsh.exe",
        ),
        "powershell.exe",  # dernier recours : Windows PowerShell 5.1
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return "pwsh"


def _monitor_height_at(x: int) -> int:
    """Hauteur en pixels de l'écran contenant la coordonnée x."""
    import win32api

    for _, _, rect in win32api.EnumDisplayMonitors():
        left, top, right, bottom = rect
        if left <= x < right:
            return bottom - top
    return 1080


def _spawn_cli_windows(app: str, env: dict, mode: str):
    print(f"[CLI] Ouverture d'une console PowerShell pour {app}...")

    left = int(env.get(f"{app.upper()}_WINDOW_LEFT", 0))

    # La console est créée DIRECTEMENT à la bonne position (pixels) : sous la
    # fenêtre de l'app, qui réserve ~300 px en bas de l'écran cible (need_cli).
    # NB : wt.exe ne dimensionne qu'en caractères (--size c,r), pas en pixels.
    cli_top = max(0, _monitor_height_at(left) - 300)

    # go.ps1 est à la racine du dépôt (3 niveaux au-dessus : app_window → scripts → gsm)
    root = Path(__file__).resolve().parents[2]
    go_ps1 = str(root / "go.ps1")
    wt_exe = _find_wt_exe()
    pwsh_exe = _find_pwsh_exe()

    # go.ps1 est relancé en mode interne "_<app>_child[_<mode>]" : ce mode est
    # géré par mode_resolver/app_launcher pour relancer Flet SANS rouvrir une
    # nouvelle CLI (évite la récursion) ; la console reste ouverte (-NoExit).
    child_arg = f"_{app.lower()}_child"
    if mode and mode != "app":
        child_arg += f"_{mode}"
    # Taille volontairement modeste : wt.exe ne dimensionne qu'en caractères
    # (--size c,r) ; 60 colonnes ≈ 540 px et 12 lignes tiennent dans la bande
    # de ~300 px réservée sous la fenêtre de l'app.
    wt_cmd = (
        "wt.exe -w new "
        f"--pos {left},{cli_top} "
        "--size 60,12 "
        f'-d "{root}" '
        f'"{pwsh_exe}" -NoExit -File "{go_ps1}" {child_arg}'
    )

    # On demande à PowerShell de lancer wt.exe via ShellExecute
    subprocess.Popen(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            f"Start-Process -FilePath \"{wt_exe}\" -ArgumentList '{wt_cmd}'",
        ]
    )


def _wait_for_powershell(timeout: float = 5.0):
    import time
    import win32gui

    print("[WAIT] Recherche de la console PowerShell...")

    hwnd = None
    for _ in range(int(timeout * 20)):  # 20 checks/sec
        hwnd = win32gui.FindWindow("ConsoleWindowClass", None)
        if hwnd:
            print(f"[WAIT] Console PowerShell trouvée : hwnd={hwnd}")
            return hwnd
        time.sleep(0.05)

    print("[WAIT][ERROR] Console PowerShell introuvable.")
    return None


def _wait_for_window(app: str, timeout: float = 10.0):
    import time

    print(f"[WAIT] Recherche de la fenêtre Flet pour {app}...")

    # 1) Trouver le PID Flet
    pid = None
    for _ in range(int(timeout * 10)):
        pid = _find_flet_pid()
        if pid:
            break
        time.sleep(0.1)

    if not pid:
        print("[WAIT][ERROR] PID Flet introuvable.")
        return None

    # 2) Trouver la fenêtre correspondant à ce PID
    for _ in range(int(timeout * 20)):
        hwnd = _find_flet_window_by_pid(pid)
        if hwnd:
            print(f"[WAIT] Fenêtre Flet trouvée : hwnd={hwnd}")
            return hwnd
        time.sleep(0.05)

    print(f"[WAIT][ERROR] Fenêtre Flet introuvable après {timeout} secondes.")
    return None


# ---------------------------------------------------------------------------
# LINUX IMPLEMENTATION
# ---------------------------------------------------------------------------


def _spawn_cli_linux(app: str):
    """
    Ouvre une console Linux sous la fenêtre Flet.
    - gnome-terminal si disponible
    - sinon xterm
    """

    print(f"[CLI] Ouverture d'une console Linux pour {app}...")

    # Essayer gnome-terminal
    try:
        subprocess.Popen(["gnome-terminal"])
        print("[CLI] gnome-terminal lancé.")
        return
    except FileNotFoundError:
        pass

    # Essayer xterm
    try:
        subprocess.Popen(["xterm"])
        print("[CLI] xterm lancé.")
        return
    except FileNotFoundError:
        pass

    print("[CLI][ERROR] Aucun terminal disponible (gnome-terminal, xterm).")
