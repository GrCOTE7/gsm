# src/gsm/components/nav_bar.py

import flet as ft

from gsm.routing.routes_registry import PAGES


class NavBar:
    """
    Barre de navigation, générée depuis le registre `PAGES` — les pages
    sans `label` (ex. une page volontairement masquée) sont simplement
    ignorées ici, sans rien à modifier dans le registre lui-même.

    `ft.is_route_active()` et `ft.context.page.navigate()` exigent d'être
    appelés depuis un composant rendu à l'intérieur de l'arbre du Router
    — c'est le cas ici, NavBar n'étant utilisé que depuis MainLayout, qui
    est lui-même une route.
    """

    @staticmethod
    @ft.component
    def view() -> ft.Control:
        return ft.Row(
            controls=[
                NavBar._link(page.label, page.path)
                for page in PAGES
                if page.label is not None
            ],
        )

    @staticmethod
    def _link(label: str, path: str) -> ft.Control:
        active = ft.is_route_active(path, exact=(path == "/"))
        return ft.TextButton(
            label,
            style=ft.ButtonStyle(
                color=ft.Colors.PRIMARY if active else ft.Colors.ON_SURFACE,
            ),
            on_click=lambda _: ft.context.page.navigate(path),
        )
