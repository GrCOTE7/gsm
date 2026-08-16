import os
import platform
import time

from env_config import load_env
from cli_spawner import spawn_cli_if_needed
from flet_runner import run_flet


def debug_dump(action, env):
    print("=== MODE DEBUG ===")
    print("[ACTION] Apps :", action["apps"], "-", "[ACTION] Mode :", action["mode"])
    print()

    print("[ENV] Variables chargées (Concernant les fenêtres):")
    for k, v in env.items():
        # if 'WINDOW' in k:
        print(f"\t{k} = {v}")
    print()

    print("[WINDOW] Fenêtres qui seraient préparées :")
    for app in action["apps"]:
        print(f"    - {app}")
    print()

    print("[CLI] CLI dédiée :")
    for app in action["apps"]:
        cli_flag = env.get(f"{app.upper()}_WINDOW_CLI", 0)
        print(f"    - {app} : {'OUI' if cli_flag == 1 else 'NON'}")
    print()

    print("[FLET] Commandes qui seraient exécutées :")
    for app in action["apps"]:
        print(f"    - python -m flet.cli run main_{app}.py -r")
    print()

    print("=== FIN DEBUG ===")


def place_cli_window(left: int, top: int = 779, width: int = 540, height: int = 300) -> bool:
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

    import win32gui
    import win32process

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
    kernel32.Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
    kernel32.Process32NextW.restype = wintypes.BOOL
    kernel32.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
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
                procs[entry.th32ProcessID] = (entry.th32ParentProcessID, entry.szExeFile)
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

    def _find_window(target_pid):
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
        return found[0] if found else None

    # Attend que la fenêtre du terminal soit créée (jusqu'à ~5 s).
    deadline = time.time() + 5.0
    while time.time() < deadline:
        for group in host_groups:
            for pid_ in chain:
                info = procs.get(pid_)
                if info and info[1].lower() in group:
                    hwnd = _find_window(pid_)
                    if hwnd:
                        return _move(hwnd)
        time.sleep(0.1)

    print("[CLI][ERROR] Fenêtre du terminal introuvable pour repositionnement.")
    return False


def launch_app(action: dict):
    env = load_env()

    if action["mode"] == "debug":
        debug_dump(action, env)
        return

    for app in action["apps"]:
        cli_key = f"{app.upper()}_WINDOW_CLI"
        cli_flag = int(env.get(cli_key, 0))

        if cli_flag == 1 and not action.get("internal_child"):
            # Parent : ouvre la console dédiée — créée à proximité de la bonne
            # position par cli_spawner. C'est elle qui relance ce pipeline en
            # mode interne (_gsm_child) et lance Flet.
            spawn_cli_if_needed(app, env, action["mode"])
        elif action.get("internal_child"):
            # Enfant de la CLI : repositionne la fenêtre du terminal sous l'app
            # (pixels exacts, comme go_ori.ps1), puis lance Flet.
            left = int(env.get(f"{app.upper()}_WINDOW_LEFT", 0))
            place_cli_window(left=left, top=779, width=540, height=300)
            run_flet(app, env, action["mode"])
        else:
            # Mode sans CLI : Flet se lance et se positionne tout seul
            # (window_config de l'app).
            run_flet(app, env, action["mode"])
