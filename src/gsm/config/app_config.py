# src/gsm/config/app_config.py

# * clés API
# * constantes métier
# * options de services
# * paramètres de scraping
# * chemins personnalisés
# * règles internes

import os
from dataclasses import dataclass, field

import flet as ft

from gsm.config.window_config import WindowConfig


@dataclass
class AppConfig:
    window: WindowConfig = field(default_factory=WindowConfig)
    home_path = "/"
    # Même chose que window, en bien meilleur techniquement : Avec WindowConfig = WindowConfig(), l'instance de WindowConfig est créée une seule fois au moment où Python lit le fichier. Si vous créez plusieurs instances de AppConfig (par exemple pour des tests unitaires), elles partageront toutes exactement la même instance de fenêtre en mémoire. C'est ce qu'on appelle un "effet de bord".

    # On peut forcer la home_path définie ici
    # à chaque REFRESH dans app_bootstrap
    # ----------------------------------------
    home_path: str = "/counter"
    home_path: str = "/about"
    # ----------------------------------------

    # Thème global de l'app. Par défaut on force un thème stable pour éviter que
    # Flet hérite du thème système de la machine (Windows sombre, Linux clair).
    theme_mode: ft.ThemeMode = ft.ThemeMode.DARK

    def get_theme_mode(self) -> ft.ThemeMode:
        raw = os.getenv("GSM_THEME_MODE", "").strip().upper()
        if raw == "LIGHT":
            return ft.ThemeMode.LIGHT
        if raw == "DARK":
            return ft.ThemeMode.DARK
        return self.theme_mode

    # Vos futurs paramètres ici (theme, etc...)


# On crée l'instance unique (Singleton) directement ici
config = AppConfig()

if __name__ == "__main__":

    def main(page: ft.Page):
        config.window.apply(page)

    # import subprocess
    # subprocess.run(["flet", "run", "src/gsm/helpers/uuu.py"])
