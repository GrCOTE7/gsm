# src/gsm/bootstrap/app_bootstrap.py
import flet as ft

from gsm.config.app_config import config
from gsm.app import App


class AppBootstrap:
    """
    Point d'amorçage de la session Flet.

    `ft.run(AppBootstrap)` fonctionne car une classe est un *callable* en Python :
    `AppBootstrap(page)` est équivalent à `AppBootstrap.__init__(instance, page)`,
    ce qui respecte exactement le contrat attendu par `ft.run`.

    Toute la configuration impérative (fenêtre, thème...) se fait ici, une
    seule fois par session ; le reste de l'app est 100% déclaratif.
    """

    def __init__(self, page: ft.Page) -> None:
        # Configuration impérative de la fenêtre (titre L_ si local, etc.)
        config.window.apply(page)
        self.page = page
        
        # 🎯 FORCE LA REDIRECTION INITIALE et À CHAQUE REFRESH VERS VOTRE ACCUEIL DE CONFIG
        # page.go(config.home_path or '/')
            
        # Rendu déclaratif de l'arbre de composants. `App.view` est passé
        # par référence. Flet se charge de l'invoquer à chaque changement d'état.
        page.render(App.view)
