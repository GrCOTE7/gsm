import platform
import time

# Import Windows-only modules safely
if platform.system() == "Windows":
    import win32gui
    import win32con
    import win32api


def prepare_window(app: str, env: dict):
    """
    Prépare la fenêtre de l'app (GSM ou UPU).
    - Sous Windows : déplace, restaure, met au premier plan.
    - Sous Linux : no-op.
    """

    left_key = f"{app.upper()}_WINDOW_LEFT"
    cli_key = f"{app.upper()}_WINDOW_CLI"

    left = env.get(left_key)
    cli_flag = env.get(cli_key, 0)

    if left is None:
        print(f"[WARN] {left_key} manquant dans .env")
        return

    if platform.system() != "Windows":
        print(f"[INFO] Linux : pas de déplacement de fenêtre pour {app}")
        return

    _move_window_windows(app, left, cli_flag)


# ---------------------------------------------------------------------------
# WINDOWS IMPLEMENTATION
# ---------------------------------------------------------------------------


def _move_window_windows(app: str, left: int, cli_flag: int):
    """
    Déplace la fenêtre Flet sous Windows.
    Utilise FindWindow + SetWindowPos + MoveWindow + ShowWindow + SetForegroundWindow.
    Gère multi-écrans + hauteur dynamique selon CLI.
    """

    window_title = f"{app.upper()} - Flet"
    print(f"[WINDOW] Recherche de la fenêtre : '{window_title}'...")

    hwnd = _wait_for_window(window_title)
    if not hwnd:
        print(f"[ERROR] Impossible de trouver la fenêtre '{window_title}'.")
        return

    print(f"[WINDOW] Fenêtre trouvée : hwnd={hwnd}")

    # Récupération de la résolution de l'écran cible
    screen = _get_screen_for_left(left)
    screen_width, screen_height = screen["width"], screen["height"]

    print(f"[WINDOW] Écran détecté : {screen_width}x{screen_height}")

    # Hauteur dynamique selon CLI
    # Si CLI=1 → on laisse 300px en bas
    cli_offset = 300 if cli_flag == 1 else 0
    window_height = screen_height - cli_offset

    # Déplacement + redimensionnement
    win32gui.MoveWindow(hwnd, left, 0, screen_width, window_height, True)
    print(f"[WINDOW] MoveWindow → X={left}, Y=0, W={screen_width}, H={window_height}")

    # Restaure si minimisée
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    print("[WINDOW] ShowWindow(SW_RESTORE)")

    # Met au premier plan
    try:
        win32gui.SetForegroundWindow(hwnd)
        print("[WINDOW] SetForegroundWindow OK")
    except Exception as e:
        print(f"[WARN] SetForegroundWindow a échoué : {e}")

    # Déplacement final sans changer la taille
    win32gui.SetWindowPos(
        hwnd, None, left, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER
    )
    print(f"[WINDOW] SetWindowPos → X={left}, Y=0")


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------


def _wait_for_window(title: str, timeout: float = 2.0):
    """Attend que la fenêtre Flet soit créée."""
    hwnd = None
    for _ in range(int(timeout * 20)):  # 20 checks/sec
        hwnd = win32gui.FindWindow(None, title)
        if hwnd:
            return hwnd
        time.sleep(0.05)
    return None


def _get_screen_for_left(left: int):
    """
    Détecte l'écran correspondant à la position X donnée.
    Multi-écrans : utilise EnumDisplayMonitors.
    Retourne {left, top, width, height}.
    """

    monitors = []

    def _callback(hMonitor, hdcMonitor, rect, data):
        left, top, right, bottom = rect
        monitors.append(
            {
                "left": left,
                "top": top,
                "width": right - left,
                "height": bottom - top,
            }
        )
        return True

    win32api.EnumDisplayMonitors(None, None, _callback, None)

    # Trouver l'écran dont la zone couvre la coordonnée X
    for m in monitors:
        if m["left"] <= left < m["left"] + m["width"]:
            return m

    # Fallback : écran principal
    return (
        monitors[0]
        if monitors
        else {
            "left": 0,
            "top": 0,
            "width": win32api.GetSystemMetrics(0),
            "height": win32api.GetSystemMetrics(1),
        }
    )
