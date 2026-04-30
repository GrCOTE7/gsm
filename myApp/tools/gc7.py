from datetime import datetime as dt

import flet as ft
import tools.screen_utils as screen_utils

THEME_MODE = ft.ThemeMode.DARK


def curr_time():
    now = dt.now()
    return f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"


def themed_border_color(dark: bool) -> ft.Colors:
    return ft.Colors(141, 145, 153) if dark else ft.Colors(115, 119, 127)


def btn(label, action=None, btnWidth=None):
    return ft.OutlinedButton(
        label,
        on_click=action,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=7),
            padding=ft.padding.symmetric(horizontal=10, vertical=7),
            color="cyan",
        ),
        width=btnWidth or 100,
        height=40,
    )


def theTime(page=None):
    now = dt.now()
    theTime = f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"
    # print(theTime, page.route)
    return theTime


def nf(f, dec=2):
    "Number Format 123456789 → 123 456,79"
    try:
        f = float(f)
        # Keep formatting deterministic on all platforms (desktop/mobile/web)
        # by avoiding OS locale dependencies.
        s = f"{f:,.{dec}f}"
        # U+00A0 is better supported on Android fonts than U+202F.
        return s.replace(",", "\u00a0").replace(".", ",")
    except (TypeError, ValueError):
        print(f"nf(): unsupported value type ({type(f).__name__}) -> {f}")
        return str(f)


def toggleTheme(page: ft.Page, on_change=None) -> ft.IconButton:
    """
    Retourne un bouton animé qui change le thème clair/sombre
    et affiche un SnackBar flottant avec l'info.
    """
    # Déclaration du bouton AVANT la fonction pour qu'on puisse le modifier depuis toggle()
    theme_btn = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE,
        icon_color="gold",
        icon_size=32,
        tooltip="Changer le thème",
        on_click=None,
    )
    # print(currentTime, "-", page.route, "-", page.theme_mode, ">")
    # page.update()

    def toggle(e):
        is_light = page.theme_mode == ft.ThemeMode.LIGHT
        page.theme_mode = ft.ThemeMode.DARK if is_light else ft.ThemeMode.LIGHT
        page.bgcolor = screen_utils.get_colors_theme(page)["bg"]

        # Met à jour l'icône du bouton
        theme_btn.icon = ft.Icons.LIGHT_MODE if is_light else ft.Icons.DARK_MODE
        # theme_btn.icon_color = "gold" if is_light else "lightblue"

        # Affiche une SnackBar
        snackbar = ft.SnackBar(
            content=ft.Text(
                f"{'🌙' if is_light else '🌞'} Thème {'sombre' if is_light else 'clair'} activé",
                color="cyan",
            ),
            bgcolor="black" if not is_light else "white",
            behavior=ft.SnackBarBehavior.FLOATING,
            duration=2000,
        )
        page.overlay.append(snackbar)
        snackbar.open = True
        if on_change:
            on_change()
        page.update()

    theme_btn.on_click = toggle

    return theme_btn


import os, shutil, subprocess


def reset_venv(requirements_file="requirements.txt"):
    """
    Supprime et recrée venv, puis installe les dépendances.
    """
    print("🔧 [gc7] Réinitialisation de l'environnement virtuel...")

    if os.path.isdir("venv"):
        shutil.rmtree("venv")
        print("🗑️ venv supprimé.")
    else:
        print("💡 Aucun venv existant.")

    os.system("python -m venv .venv")
    print("✅ Nouveau venv créé.")

    pip_path = os.path.join("venv", "Scripts", "pip.exe")

    if os.path.isfile(requirements_file):
        subprocess.run([pip_path, "install", "-r", requirements_file])
        print(f"📦 Dépendances installées depuis {requirements_file}.")
    else:
        subprocess.run([pip_path, "install", "flet"])
        print("📦 Flet installé par défaut.")

    print("🚀 Environnement prêt !")


def simpleTest():
    f = 1234567.89
    # f = float(f)
    dec = 2
    return nf(f, dec)
