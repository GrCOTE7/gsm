# src/gsm/views/partials/nav_bar.py

import flet as ft

from gsm.routing.routes_registry import PAGES


class NavBar:

    # ========================================================
    # APP BAR
    # ========================================================

    @staticmethod
    @ft.component
    def app_bar(
        title: str,
        on_menu_click: ft.ControlEventHandler[ft.IconButton] | None,
        brand_is_link: bool = False,
    ) -> ft.AppBar:
        """AppBar de l'application.

        `brand_is_link` vient de `MainLayout` (qui évalue déjà la route active) :
        la marque ne doit jamais lire `ft.context.page` elle-même pendant le
        rendu, sous peine de casser le re-rendu déclenché par la navigation
        (les destinations du menu ne changeaient alors plus rien).
        """

        appbar = ft.AppBar()
        appbar.leading = ft.IconButton(
            icon=ft.Icons.MENU,
            tooltip="Menu",
            on_click=on_menu_click,
        )
        appbar.leading_width = 48
        appbar.title = ft.Row(
            spacing=12,
            controls=[
                NavBar._brand(brand_is_link),
                ft.Text(
                    title,
                    size=18,
                ),
            ],
        )

        return appbar

    # ========================================================
    # MARQUE "GSM"
    # ========================================================

    @staticmethod
    def _brand(is_link: bool) -> ft.Control:
        """Libellé "GSM" : cliquable vers l'accueil, ou simple texte.

        Aucun accès au contexte ici — c'est l'appelant qui décide, ce qui évite
        toute lecture de `ft.context.page` au moment du rendu. Le handler, lui,
        s'exécute dans un contexte d'événement où `ft.context.page` est valide.
        """
        brand = ft.Text(
            "GSM",
            size=20,
            weight=ft.FontWeight.BOLD,
        )

        if not is_link:
            return brand

        return ft.Container(
            content=brand,
            on_click=lambda _e: ft.context.page.navigate("/"),
            ink=True,
            tooltip="Aller à l'accueil",
            padding=ft.Padding.symmetric(horizontal=6, vertical=2),
            border_radius=6,
        )

    # ========================================================
    # DRAWER
    # ========================================================

    @staticmethod
    @ft.component
    def drawer(
        on_change: ft.ControlEventHandler[ft.NavigationDrawer] | None,
        selected_index: int = 0,
    ) -> ft.NavigationDrawer:

        return ft.NavigationDrawer(
            controls=[
                ft.Container(
                    padding=ft.Padding.only(
                        left=20,
                        top=20,
                        bottom=20,
                    ),
                    content=ft.Text(
                        "GSM",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                    ),
                ),
                *[
                    NavBar._destination(page)
                    for page in PAGES
                    if page.label is not None
                ],
            ],
            selected_index=selected_index,
            on_change=on_change,
        )

    # ========================================================
    # DESTINATION
    # ========================================================

    @staticmethod
    def _destination(page) -> ft.NavigationDrawerDestination:

        return ft.NavigationDrawerDestination(
            label=page.label,
            icon=page.icon or ft.Icons.CIRCLE_OUTLINED,
            selected_icon=page.selected_icon or page.icon or ft.Icons.CIRCLE_OUTLINED,
        )

    # ========================================================
    # INDEX
    # ========================================================

    @staticmethod
    def index_for_path(path: str | None) -> int:
        """
        Index du destination NavBar correspondant à la route courante.

        - Retourne `-1` pour une route hors registre (ex. 404) : dans ce cas
          aucune destination n'est sélectionnée (comportement Flet).
        """

        destinations = [page for page in PAGES if page.label is not None]

        if not destinations:
            return -1

        route = (path or "/").split("?", 1)[0].split("#", 1)[0]

        for index, page in enumerate(destinations):
            if page.path == route:
                return index

        return -1

    @staticmethod
    def path_for_selected_index(selected_index: int | None) -> str | None:

        destinations = [page for page in PAGES if page.label is not None]

        if selected_index is None:
            return None

        if selected_index < 0 or selected_index >= len(destinations):
            return None

        return destinations[selected_index].path
