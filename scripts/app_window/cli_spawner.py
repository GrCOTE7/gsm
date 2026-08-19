"""Ouverture et positionnement des fenêtres CLI dédiées (sous chaque app)."""

import os
import platform
import shutil
import subprocess
import time
from pathlib import Path

from common import ROOT, GO_PS1, CLI_WIDTH, CLI_HEIGHT, CLI_TOP, SUFFIX_CLI, child_arg
from env_config import window_left, wants_cli

if platform.system() == "Windows":
    import win32gui
    import win32process

# Hôtes de terminal Windows, par ordre de préférence : le CADRE visible
# (WindowsTerminal.exe) d'abord, puis le miroir OpenConsole (conhost.exe).
TERMINAL_HOSTS = (
    ("windowsterminal.exe", "wt.exe"),
    ("openconsole.exe", "conhost.exe"),
)


def spawn_cli_if_needed(app: str, env: dict, mode: str) -> None:
    """Ouvre une console dédiée sous la fenêtre Flet (no-op si *_WINDOW_CLI=0).

    - Windows → Windows Terminal (wt.exe) ;
    - Linux → gnome-terminal / xterm.
    """
    if not wants_cli(app, env):
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
    procs = _snapshot_processes()
    chain = _process_chain(procs, os.getpid())

    # Attend que la fenêtre du terminal soit créée (jusqu'à ~5 s).
    deadline = time.time() + 5.0
    while time.time() < deadline:
        for group in TERMINAL_HOSTS:
            for pid in chain:
                info = procs.get(pid)
                if info and info[1].lower() in group:
                    hwnd = _nearest_window(pid, left, top)
                    if hwnd:
                        return _move(hwnd)
        time.sleep(0.1)

    print("[CLI][ERROR] Fenêtre du terminal introuvable pour repositionnement.")
    return False


# ---------------------------------------------------------------------------
# Snapshot des processus Windows (partagé : repositionnement + ancêtres)
# ---------------------------------------------------------------------------


def _snapshot_processes() -> dict[int, tuple[int, str]]:
    """Instantané des processus : PID -> (PID parent, nom de l'exécutable).

    Windows uniquement ; {} ailleurs.
    """
    if platform.system() != "Windows":
        return {}

    import ctypes
    from ctypes import wintypes

    kernel32 = ctypes.windll.kernel32

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
        return {}

    procs: dict[int, tuple[int, str]] = {}
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

    return procs


def _process_chain(
    procs: dict[int, tuple[int, str]], pid: int, limit: int = 32
) -> list[int]:
    """Chaîne des processus ancêtres de `pid` : [nous, parent, grand-parent...]."""
    chain = []
    seen = set()
    for _ in range(limit):
        if not pid or pid in seen:
            break
        seen.add(pid)
        chain.append(pid)
        info = procs.get(pid)
        if not info:
            break
        pid = info[0]
    return chain


def _nearest_window(target_pid: int, prefer_left: int, prefer_top: int):
    """Fenêtre visible du process donnée, la plus proche de la position cible.

    En mode multi-app (./go gu), les deux CLI dédiées (GSM + UPU) sont
    hébergées par le MÊME process WindowsTerminal : prendre la « première
    fenêtre trouvée » déplacerait la console de l'autre app. On choisit donc,
    parmi toutes les fenêtres visibles du process, celle dont le cadre est le
    plus proche de la position attendue pour CETTE CLI.
    """
    found = []

    def _cb(hwnd, _):
        # Toujours renvoyer True : arrêter tôt (False) fait lever
        # pywintypes.error(18) par win32gui.EnumWindows.
        if win32gui.IsWindowVisible(hwnd):
            _, wpid = win32process.GetWindowThreadProcessId(hwnd)
            if wpid == target_pid:
                found.append(hwnd)
        return True

    win32gui.EnumWindows(_cb, None)
    if not found:
        return None

    def _distance(hwnd) -> int:
        left, top, _, _ = win32gui.GetWindowRect(hwnd)
        return abs(left - prefer_left) + abs(top - prefer_top)

    return min(found, key=_distance)


def get_ancestor_pids(pid: int, limit: int = 10) -> list[int]:
    r"""Retourne la chaîne des PID ancêtres de `pid` (sans `pid`), du plus
    proche au plus lointain (ex: parent, grand-parent, ...). Windows only ;
    [] ailleurs.

    Utilisé par app_launcher pour identifier la CLI dédiée courante : go.ps1
    écrit le PID de la console dans %TEMP%\gsm_cli_<app>.pid, on compare donc
    les ancêtres du process courant (le pwsh de la console, éventuellement via
    uv) à ces fichiers — fiable même si l'environnement n'est pas hérité par le
    serveur Windows Terminal (wt.exe relaie à un serveur dont l'env est figé).
    """
    if platform.system() != "Windows":
        return []

    parent_of = {pid_: parent for pid_, (parent, _) in _snapshot_processes().items()}

    ancestors = []
    current = pid
    for _ in range(limit):
        parent = parent_of.get(current)
        if not parent or parent == current or parent == 0:
            break
        ancestors.append(parent)
        current = parent
    return ancestors


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
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return "pwsh"


def _find_powershell_exe() -> str:
    r"""Chemin absolu d'un PowerShell utilisable pour lancer wt.exe.

    IMPORTANT : la CLI dédiée démarre avec un PATH minimal (sans 'powershell'
    ni 'pwsh') : CreateProcess échoue (WinError 2) sur un simple nom. On force
    donc un chemin absolu — pwsh (PowerShell 7, déjà résolu en absolu par
    _find_pwsh_exe) d'abord, puis Windows PowerShell 5.1, toujours présent
    sous %SystemRoot%\System32\WindowsPowerShell\v1.0.
    """
    pwsh = _find_pwsh_exe()
    if os.path.basename(pwsh).lower() == "pwsh.exe":
        return pwsh
    system_root = os.environ.get("SystemRoot", r"C:\Windows")
    powershell_51 = os.path.join(
        system_root, "System32", "WindowsPowerShell", "v1.0", "powershell.exe"
    )
    if os.path.exists(powershell_51):
        return powershell_51
    return pwsh  # dernier recours : "powershell.exe" (PATH normal)


def _close_stale_cli(app: str) -> None:
    """Ferme l'ancienne CLI dédiée de `app` (best-effort, Windows).

    La CLI dédiée de `app` est un pwsh -NoExit au prompt, dont la ligne de
    commande contient 'go.ps1 _<app>_child' : on tue toute son arborescence
    (la fenêtre wt se ferme). À appeler avant de spawner une nouvelle CLI
    (relance de ./go gu depuis une CLI dédiée) pour ne jamais avoir de CLI
    dédiée en double.
    """
    ps = _find_powershell_exe()
    script = (
        "Get-CimInstance Win32_Process "
        '-Filter "Name=\'pwsh.exe\' OR Name=\'powershell.exe\'" | '
        f"Where-Object {{ $_.ProcessId -ne $PID -and $_.CommandLine -like '*go.ps1*_{app}_child*' }} | "
        "ForEach-Object { taskkill /PID $_.ProcessId /T /F 2>$null | Out-Null }"
    )
    subprocess.run(
        [ps, "-NoProfile", "-NonInteractive", "-Command", script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print(f"[CLI] Ancienne CLI dédiée de {app} remplacée.")


def _monitor_height_at(x: int) -> int:
    """Hauteur en pixels de l'écran contenant la coordonnée x."""
    import win32api

    for _, _, rect in win32api.EnumDisplayMonitors():
        left, top, right, bottom = rect
        if left <= x < right:
            return bottom - top
    return 1080


def _spawn_cli_windows(app: str, env: dict, mode: str) -> None:
    print(f"[CLI] Ouverture d'une console PowerShell pour {app}...")

    left = window_left(app, env)

    # La console est créée DIRECTEMENT à la bonne position (pixels) : sous la
    # fenêtre de l'app, qui réserve ~CLI_HEIGHT px en bas de l'écran cible.
    # NB : wt.exe ne dimensionne qu'en caractères (--size c,r), pas en pixels.
    cli_top = max(0, _monitor_height_at(left) - CLI_HEIGHT)

    wt_exe = _find_wt_exe()
    pwsh_exe = _find_pwsh_exe()

    # go.ps1 est relancé en mode interne "_<app>_child[_<mode>]" : ce mode est
    # géré par mode_resolver/app_launcher pour relancer Flet SANS rouvrir une
    # nouvelle CLI (évite la récursion) ; la console reste ouverte (-NoExit).
    child_arg_ = child_arg(app, mode, SUFFIX_CLI)
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

    # On demande à PowerShell de lancer wt.exe via ShellExecute. Toujours un
    # chemin ABSOLU : la CLI dédiée a un PATH minimal (sans 'powershell') et
    # CreateProcess échouerait sinon (WinError 2).
    ps_exe = _find_powershell_exe()
    subprocess.Popen(
        [
            ps_exe,
            "-NoProfile",
            "-Command",
            f"Start-Process -FilePath \"{wt_exe}\" -ArgumentList '{wt_cmd}'",
        ]
    )


# ---------------------------------------------------------------------------
# LINUX IMPLEMENTATION
# ---------------------------------------------------------------------------


def _spawn_cli_linux(app: str) -> None:
    """Ouvre une console Linux sous la fenêtre Flet (gnome-terminal puis xterm)."""
    print(f"[CLI] Ouverture d'une console Linux pour {app}...")

    for terminal in ("gnome-terminal", "xterm"):
        try:
            subprocess.Popen([terminal])
            print(f"[CLI] {terminal} lancé.")
            return
        except FileNotFoundError:
            continue

    print("[CLI][ERROR] Aucun terminal disponible (gnome-terminal, xterm).")



