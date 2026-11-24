"""Ouverture et positionnement des fenêtres CLI dédiées (sous chaque app)."""

import os
import platform
import shutil
import subprocess
import time
from pathlib import Path

from common import ROOT, GO_PS1, CLI_WIDTH, CLI_HEIGHT, CLI_TOP, SUFFIX_CLI, child_arg
from env_config import wants_cli, window_left

if platform.system() == "Windows":
    import win32gui
    import win32process

# Hôtes de terminal Windows, par ordre de préférence : le CADRE visible
# (WindowsTerminal.exe) d'abord, puis le miroir OpenConsole (conhost.exe).
TERMINAL_HOSTS = (
    ("windowsterminal.exe", "wt.exe"),
    ("openconsole.exe", "conhost.exe"),
)


def spawn_cli_if_needed(app: str, env: dict, mode: str) -> bool:
    """Ouvre une console dédiée sous la fenêtre Flet.

    Retourne True si une CLI dédiée a bien été lancée, False sinon.
    - Windows → Windows Terminal (wt.exe) ;
    - Linux → gnome-terminal / xterm.
    """
    if not wants_cli(app, env):
        print(f"[CLI] Pas de console dédiée pour {app}.")
        return False

    if platform.system() == "Windows":
        return _spawn_cli_windows(app, env, mode)
    return _spawn_cli_linux(app)


def _visible_origin(
    left: int, top: int, width: int = CLI_WIDTH, height: int = CLI_HEIGHT
) -> tuple[int, int]:
    """Ramène (left, top) dans un écran visible si la cible tombe hors bureau.

    `.env` peut viser le 2e écran (GSM_WINDOW_LEFT=1913). Avec un seul écran
    branché, la console naissait à 1913 px sur une dalle de 1920 : 7 px visibles,
    et `./go` semblait ne rien faire.
    """
    try:
        import win32api

        monitors = [rect for _, _, rect in win32api.EnumDisplayMonitors()]
    except Exception:
        return left, top

    if not monitors:
        return left, top

    # Fenêtre déjà majoritairement visible (même à cheval sur 2 écrans) : on ne
    # touche à rien, c'est la disposition voulue dans .env.
    visible = max(
        (min(left + width, r) - max(left, l) for l, _t, r, _b in monitors),
        default=0,
    )
    if visible >= width * 0.6:
        return left, top

    l, t, r, b = next((m for m in monitors if m[0] <= left < m[2]), monitors[0])
    return max(l, min(left, r - width)), max(t, min(top, b - height))


def _window_by_title(marker: str) -> int | None:
    """Fenêtre visible dont le titre contient `marker`, ou None."""
    found: list[int] = []

    def _cb(hwnd, _arg):
        try:
            if win32gui.IsWindowVisible(hwnd) and marker in win32gui.GetWindowText(
                hwnd
            ):
                found.append(hwnd)
        except Exception:
            pass
        return True

    try:
        win32gui.EnumWindows(_cb, None)
    except Exception:
        return None
    return found[0] if found else None


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
    user32 = ctypes.windll.user32
    clamp_left, clamp_top = _visible_origin(left, top)

    def _move(hwnd) -> bool:
        # pywin32 : MoveWindow ne renvoie rien (None) ; le déplacement est
        # vérifié par la fenêtre elle-même (GetWindowRect après coup).
        win32gui.MoveWindow(hwnd, clamp_left, clamp_top, width, height, True)
        # Remonter la fenêtre : lancée depuis VS Code (ou avec l'app au
        # premier plan), la CLI naissait derrière et semblait ne pas s'ouvrir.
        user32.ShowWindow(hwnd, 9)  # SW_RESTORE
        user32.BringWindowToTop(hwnd)
        user32.SetForegroundWindow(hwnd)
        print(
            f"[CLI] Terminal repositionné : ({clamp_left}, {clamp_top}) {width}x{height} px"
        )
        return True

    # 0) Notre propre fenêtre, identifiée par le titre unique posé par go.ps1
    #    ("GSM-CLI::<pid>"). C'est la seule méthode fiable quand plusieurs CLI
    #    cohabitent : sinon on déplaçait/redimensionnait la fenêtre d'une CLI
    #    précédente, et la nouvelle restait à la taille par défaut.
    marker = os.environ.get("GSM_CLI_WINDOW_TITLE", "")
    if marker:
        deadline = time.time() + 5.0
        while time.time() < deadline:
            hwnd = _window_by_title(marker)
            if hwnd:
                return _move(hwnd)
            time.sleep(0.15)

    # 1) Fenêtre VISIBLE du terminal hôte (Windows Terminal ou conhost).
    #    On passe par la chaîne des processus AVANT GetConsoleWindow() : sous
    #    Windows Terminal (y compris via la redirection « terminal par défaut »
    #    de Windows 11), GetConsoleWindow() renvoie le miroir OpenConsole, dont
    #    le déplacement ne bouge pas la fenêtre visible — d'où une CLI qui
    #    s'ouvrait à la mauvaise place et à la mauvaise taille.
    deadline = time.time() + 5.0
    while time.time() < deadline:
        procs = _snapshot_processes()
        chain = _process_chain(procs, os.getpid())
        for group in TERMINAL_HOSTS:
            for pid in chain:
                info = procs.get(pid)
                if info and info[1].lower() in group:
                    hwnd = _nearest_window(pid, left, top)
                    if hwnd:
                        return _move(hwnd)
        # La fenêtre peut aussi être une console classique : on tente le
        # handle direct à chaque tour avant de réessayer.
        hwnd = kernel32.GetConsoleWindow()
        if hwnd and win32gui.IsWindowVisible(hwnd):
            return _move(hwnd)
        time.sleep(0.15)

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
        "-Filter \"Name='pwsh.exe' OR Name='powershell.exe'\" | "
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


def _spawn_cli_windows(app: str, env: dict, mode: str) -> bool:
    print(f"[CLI] Ouverture d'une console PowerShell pour {app}...")

    left = window_left(app, env)
    # Position/size imposées DÈS la création par Windows Terminal (wt.exe ne
    # dimensionne qu'en caractères : 60x12 ≈ CLI_WIDTH x CLI_HEIGHT px). Le
    # positionnement a posteriori reste fait par l'enfant, mais il ne peut pas
    # corriger une fenêtre créée au hasard.
    cli_top = max(0, _monitor_height_at(left) - CLI_HEIGHT)

    wt_exe = _find_wt_exe()
    pwsh_exe = _find_pwsh_exe()

    # go.ps1 est relancé en mode interne "_<app>_child[_<mode>]" : ce mode est
    # géré par mode_resolver/app_launcher pour relancer Flet SANS rouvrir une
    # nouvelle CLI (évite la récursion) ; la console reste ouverte (-NoExit).
    child_arg_ = child_arg(app, mode, SUFFIX_CLI)
    wt_cmd = (
        "wt.exe -w new "
        f"--pos {left},{cli_top} "
        "--size 60,12 "
        f'-d "{ROOT}" '
        f'"{pwsh_exe}" -NoExit -File "{GO_PS1}" {child_arg_}'
    )

    ps_exe = _find_powershell_exe()
    # valid_cli_pid purge un .pid périmé : nécessaire pour que la nouvelle
    # console soit bien détectée comme « différente » de l'ancienne.
    previous_pid = valid_cli_pid(app)
    try:
        subprocess.Popen(
            [
                ps_exe,
                "-NoProfile",
                "-Command",
                f"Start-Process -FilePath \"{wt_exe}\" -ArgumentList '{wt_cmd}'",
            ]
        )
    except OSError:
        print(f"[CLI][ERROR] Impossible d'ouvrir la console Windows pour {app}.")
        return False

    # Popen ne prouve rien : Start-Process peut échouer silencieusement. Les
    # preuves de vie sont le .pid réécrit par go.ps1 et le process enfant.
    if not _wait_for_child_cli(app, previous_pid):
        # Dernier contrôle : une console qui a démarré juste après le délai ne
        # doit pas provoquer un second lancement de l'app en double.
        live = _live_child_cli_pids(app)
        if live and (live - ({previous_pid} if previous_pid is not None else set())):
            return True
        print(
            f"[CLI][WARN] La console dédiée pour {app} n'a pas démarré "
            "(aucune CLI enfant détectée)."
        )
        return False
    return True


def _cli_pid_file(app: str) -> Path:
    """Fichier .pid de la CLI dédiée, écrit par go.ps1 au démarrage enfant."""
    temp = os.environ.get("TEMP", os.environ.get("TMP", ""))
    return Path(temp) / f"gsm_cli_{app.lower()}.pid"


def _read_cli_pid(app: str) -> int | None:
    """PID enregistré dans le .pid de la CLI dédiée de `app`, ou None.

    Lecture BRUTE du fichier : ne dit rien sur la vivacité du process (cf.
    `valid_cli_pid`). Utilisée dans les boucles d'attente, où un appel WMI
    toutes les 200 ms serait ruineux.
    """
    try:
        return int(_cli_pid_file(app).read_text(encoding="ascii").strip())
    except (OSError, ValueError):
        return None


def _live_child_cli_pids(app: str) -> set[int] | None:
    """PID des CLI dédiées VIVANTES de `app`, ou None si la requête échoue.

    Un .pid laissé par une CLI fermée devient un piège : Windows recycle les
    PID, et le lanceur croit alors qu'une CLI dédiée existe encore (il réutilise
    la console courante au lieu d'en ouvrir une). On vérifie donc que le
    process existe bel et bien avec la ligne de commande attendue.
    """
    ps = _find_powershell_exe()
    # -notlike 'Start-Process' : le PowerShell INTERMÉDIAIRE qui lance wt.exe
    # porte dans sa ligne de commande le texte complet (« ... -File go.ps1
    # _gsm_child ») et serait compté comme une CLI vivante. La vraie CLI enfant
    # est « pwsh -NoExit -File <go.ps1> _<app>_child », sans Start-Process.
    script = (
        "Get-CimInstance Win32_Process "
        "-Filter \"Name='pwsh.exe' OR Name='powershell.exe'\" | "
        f"Where-Object {{ $_.CommandLine -like '*go.ps1*_{app}_child*' "
        "-and $_.CommandLine -notlike '*Start-Process*' }} | "
        "ForEach-Object { $_.ProcessId }"
    )
    try:
        result = subprocess.run(
            [ps, "-NoProfile", "-NonInteractive", "-Command", script],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    pids: set[int] = set()
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.isdigit():
            pids.add(int(line))
    return pids


def valid_cli_pid(app: str) -> int | None:
    """PID de la CLI dédiée de `app` s'il est VIVANT, sinon nettoie et None."""
    pid = _read_cli_pid(app)
    if pid is None:
        return None

    live = _live_child_cli_pids(app)
    if live is None:
        # Requête impossible : on ne casse rien, on fait confiance au fichier.
        return pid

    if pid in live:
        return pid

    _cli_pid_file(app).unlink(missing_ok=True)
    return None


def _wait_for_child_cli(app: str, previous: int | None, timeout: float = 30.0) -> bool:
    """Attend que la CLI enfant soit réellement là (30 s par défaut).

    Deux preuves acceptées : le .pid réécrit par go.ps1, ou un process
    'go.ps1 _<app>_child' vivant autre que `previous`. Le délai est large à
    dessein : au premier lancement après un démarrage de Windows, Terminal +
    PowerShell 7 peuvent dépasser la dizaine de secondes — l'ancien délai de
    10 s faisait alors conclure à l'échec, et `./go` basculait sur la console
    courante alors que la CLI finissait par s'ouvrir.
    """
    deadline = time.time() + timeout
    live_interval = 3.0
    next_live_check = time.time() + live_interval
    announced = False
    previous_set = {previous} if previous is not None else set()

    while time.time() < deadline:
        pid = _read_cli_pid(app)
        if pid is not None and pid != previous:
            return True

        now = time.time()
        if now >= next_live_check:
            next_live_check = now + live_interval
            live = _live_child_cli_pids(app)
            if live and (live - previous_set):
                return True

        if not announced and now > deadline - timeout + 6.0:
            announced = True
            print(
                "[CLI] Démarrage de la console (premier lancement : quelques secondes)..."
            )

        time.sleep(0.3)

    return False


# ---------------------------------------------------------------------------
# LINUX IMPLEMENTATION
# ---------------------------------------------------------------------------


def _spawn_cli_linux(app: str) -> bool:
    """Ouvre une console Linux sous la fenêtre Flet (gnome-terminal puis xterm).

    Retourne True si une console a pu être démarrée, False sinon.
    On contourne les PATH entries qui existent mais ne sont pas exécutable
    (PermissionError / OSError) : ce cas est fréquent sur certains systèmes
    Linux où un binaire résolu dans le PATH n'a pas les bons droits.
    """
    print(f"[CLI] Ouverture d'une console Linux pour {app}...")

    for terminal in ("gnome-terminal", "xterm"):
        terminal_path = shutil.which(terminal)
        if not terminal_path or not os.access(terminal_path, os.X_OK):
            continue

        try:
            subprocess.Popen([terminal_path])
            print(f"[CLI] {terminal} lancé.")
            return True
        except (FileNotFoundError, PermissionError, OSError):
            continue

    print("[CLI][ERROR] Aucun terminal disponible (gnome-terminal, xterm).")
    return False
