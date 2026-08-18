# src/gsm/app.py
import flet as ft

from gsm.routing.router import AppRouter


class App:
    """
    Composant racine de l'application.

    Volontairement fin pour l'instant : il délègue tout au routeur. C'est
    l'endroit où brancher plus tard des providers globaux (thème,
    contexte d'authentification via `ft.create_context`, etc.) sans
    toucher au reste de l'arborescence.
    """

    # On utilise un @classmethod. Le premier argument devient 'cls' (la classe elle-même)
    # mais Flet n'en a pas conscience et l'appel App.view fonctionnera. La classe ne sert que de namespace
    @classmethod
    @ft.component
    def view(cls) -> ft.Control:
        return ft.Container(
            expand=True,
            content=AppRouter.view(),
        )
