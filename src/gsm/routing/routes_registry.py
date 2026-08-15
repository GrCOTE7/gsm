# src/gsm/routing/routes_registry.py

"""
Registre central des pages de l'application.

C'est la SEULE source de vérité pour "quelles pages existent, à quelle
URL, et sous quel nom dans la navigation". `AppRouter` et `NavBar` ne
font plus que *lire* cette liste, chacun n'y prenant que ce qui le
concerne — ils ne la redéclarent jamais.

Pour ajouter une page :
    1. Créez sa classe dans `gsm/views/pages/`.
    2. Ajoutez une entrée `PageRoute(...)` dans `PAGES` ci-dessous.
   Rien d'autre à modifier — ni dans le routeur, ni dans la NavBar.
"""

from dataclasses import dataclass
from typing import Callable
import flet as ft

from gsm.config.app_config import config  # 💡 On importe la configuration

from gsm.views.pages.home import HomePage
from gsm.views.pages.about import AboutPage
from gsm.views.pages.counter import CounterPage
from gsm.views.pages.test import TestPage

@dataclass(frozen=True)
class PageRoute:
    """Décrit une page navigable : où elle vit, ce qu'elle affiche."""

    component: Callable[[], ft.Control]
    path: str  # chemin absolu, ex. "/" ou "/about"
    label: str | None = None  # None => n'apparaît pas dans la NavBar

    @property
    def is_index(self) -> bool:
        return self.path == config.home_path

    @property
    def segment(self) -> str:
        """Segment relatif attendu par `ft.Route(path=...)`."""
        return self.path.lstrip("/")


# Ordre = ordre d'apparition dans la NavBar.
# (Le 404 n'est volontairement pas ici : ce n'est pas une page
# "navigable", elle est câblée à part comme route catch-all.)
PAGES: list[PageRoute] = [
    PageRoute(component=HomePage.view, path="/", label="Accueil"),
    PageRoute(component=AboutPage.view, path="/about", label="About"),
    PageRoute(component=CounterPage.view, path="/counter", label="Compteur"),
    PageRoute(component=TestPage.view, path="/test", label="Test"),
]
