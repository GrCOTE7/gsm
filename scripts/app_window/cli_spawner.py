import os
import platform
import shutil
import subprocess
import time
from pathlib import Path

from common import ROOT, GO_PS1, CLI_WIDTH, CLI_HEIGHT, CLI_TOP, child_arg

if platform.system() == "Windows":
    import win32gui
    import win32process


def spawn_cli_if_needed(app: str, env: dict, mode: str):
    """
    Ouvre une console dédiée sous la fenêtre Flet.
    - Si *_WINDOW_CLI = 0 → no-op
    - Windows → spawn Windows Terminal (wt.exe)
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


def place_cli_window(
    left: int, top: int = CLI_TOP, width: int = CLI_WIDTH, height: int = CLI_HEIGHT
) -> bool:
    """Place la fenêtre du terminal courant aux pixels exacts (sous l'app).

    Reproduit `Move-WindowsTerminalWindow` de go_ori.ps1. Sous Windows
    Terminal, GetConsoleWindow() renvoie le « miroir » OpenConsole (déplacé
    mais pas la fenêtre visible) : on cible donc le cadre WindowsTerminal en
    remontant la chaîne des processus parents.
    """
    if platform.system() != "Windows":
        return False

    import ctypes
    from ctypes import wintypes

    kernel32 = ctypes.windll.kernel32

    def _move(hwnd) -> bool:
        # pywin32 : MoveWindow ne renvoie rien (None) ; le déplacement est
        # vérifié par la fenêtre elle-même (GetWindowRect après coup).
        win32gui.MoveWindow(hwnd, left, top, width, height, True)
        print(f"[CLI] Terminal repositionné : ({left}, {top}) {width}x{height} px")
        return True

    # 1) Console classique (hors Windows Terminal) : cible directe.
    if not os.environ.get("WT_SESSION"):
        hwnd = kernel32.GetConsoleWindow()
        if hwnd and win32gui.IsWindowVisible(hwnd):
            return _move(hwnd)

    # 2) Windows Terminal : retrouver le CADRE visible (WindowsTerminal.exe)
    #    via la chaîne des processus parents.
    class PROCESSENTRY32W(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD),
            ("cntUsage", wintypes.DWORD),
            ("th32ProcessID", wintypes.DWORD),
            ("th32DefaultHeapID", ctypes.POINTER(wintypes.ULONG)),
            ("th32ModuleID", wintypes.DWORD),
            ("cntThreads", wintypes.DWORD),
            ("th32ParentProcessID", wintypes.DWORD),
            ("pcPriClassBase", ctypes.c_long),
            ("dwFlags", wintypes.DWORD),
            ("szExeFile", ctypes.c_wchar * 260),
        ]

    kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    kernel32.Process32FirstW.restype = wintypes.BOOL
    kernel32.Process32FirstW.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(PROCESSENTRY32W),
    ]
    kernel32.Process32NextW.restype = wintypes.BOOL
    kernel32.Process32NextW.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(PROCESSENTRY32W),
    ]
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]

    snapshot = kernel32.CreateToolhelp32Snapshot(0x00000002, 0)  # TH32CS_SNAPPROCESS
    if snapshot == wintypes.HANDLE(-1).value:
        print("[CLI][ERROR] Impossible d'énumérer les processus.")
        return False

    procs = {}
    try:
        entry = PROCESSENTRY32W()
        entry.dwSize = ctypes.sizeof(PROCESSENTRY32W)
        if kernel32.Process32FirstW(snapshot, ctypes.byref(entry)):
            while True:
                procs[entry.th32ProcessID] = (
                    entry.th32ParentProcessID,
                    entry.szExeFile,
                )
                if not kernel32.Process32NextW(snapshot, ctypes.byref(entry)):
                    break
    finally:
        kernel32.CloseHandle(snapshot)

    # Ordre de préférence : le cadre WindowsTerminal d'abord, puis OpenConsole.
    host_groups = [
        ("windowsterminal.exe", "wt.exe"),
        ("openconsole.exe", "conhost.exe"),
    ]

    # Chaîne de processus : [nous, parent, grand-parent, ...]
    chain = []
    pid = os.getpid()
    seen = set()
    for _ in range(32):
        if not pid or pid in seen:
            break
        seen.add(pid)
        chain.append(pid)
        info = procs.get(pid)
        if not info:
            break
        pid = info[0]

    def _find_window(target_pid, prefer_left, prefer_top):
        """Fenêtre visible du process donné, la plus proche de la position cible.

        En mode multi-app (./go gu), les deux CLI dédiées (GSM + UPU) sont
        hébergées par le MÊME process WindowsTerminal : prendre la « première
        fenêtre trouvée » déplacerait la console de l'autre app. On choisit donc,
        parmi toutes les fenêtres visibles du process, celle dont le cadre est
        le plus proche de la position attendue pour CETTE CLI.
        """
        found = []

        def _cb(hwnd_, _):
            # Toujours renvoyer True : arrêter tôt (False) fait lever
            # pywintypes.error(18) par win32gui.EnumWindows.
            if win32gui.IsWindowVisible(hwnd_):
                _, wpid = win32process.GetWindowThreadProcessId(hwnd_)
                if wpid == target_pid:
                    found.append(hwnd_)
            return True

        win32gui.EnumWindows(_cb, None)
        if not found:
            return None

        def _score(hwnd_):
            l, t, _, _ = win32gui.GetWindowRect(hwnd_)
            return abs(l - prefer_left) + abs(t - prefer_top)

        return min(found, key=_score)

    # Attend que la fenêtre du terminal soit créée (jusqu'à ~5 s).
    deadline = time.time() + 5.0
    while time.time() < deadline:
        for group in host_groups:
            for pid_ in chain:
                info = procs.get(pid_)
                if info and info[1].lower() in group:
                    hwnd = _find_window(pid_, left, top)
                    if hwnd:
                        return _move(hwnd)
        time.sleep(0.1)

    print("[CLI][ERROR] Fenêtre du terminal introuvable pour repositionnement.")
    return False

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
    # fenêtre de l'app, qui réserve ~CLI_HEIGHT px en bas de l'écran cible.
    # NB : wt.exe ne dimensionne qu'en caractères (--size c,r), pas en pixels.
    cli_top = max(0, _monitor_height_at(left) - CLI_HEIGHT)

    wt_exe = _find_wt_exe()
    pwsh_exe = _find_pwsh_exe()

    # go.ps1 est relancé en mode interne "_<app>_child[_<mode>]" : ce mode est
    # géré par mode_resolver/app_launcher pour relancer Flet SANS rouvrir une
    # nouvelle CLI (évite la récursion) ; la console reste ouverte (-NoExit).
    child_arg_ = child_arg(app, mode, "child")
    # Taille volontairement modeste : wt.exe ne dimensionne qu'en caractères
    # (--size c,r) ; 60 colonnes ≈ CLI_WIDTH px et 12 lignes tiennent dans la
    # bande de ~CLI_HEIGHT px réservée sous la fenêtre de l'app.
    wt_cmd = (
        "wt.exe -w new "
        f"--pos {left},{cli_top} "
        "--size 60,12 "
        f'-d "{ROOT}" '
        f'"{pwsh_exe}" -NoExit -File "{GO_PS1}" {child_arg_}'
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
