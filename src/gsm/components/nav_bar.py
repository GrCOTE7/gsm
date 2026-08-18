# src/gsm/components/nav_bar.py

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
    ) -> ft.AppBar:

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
                ft.Text(
                    "GSM",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    title,
                    size=18,
                ),
            ],
        )

        return appbar

    # ========================================================
    # DRAWER
    # ========================================================

    @staticmethod
    @ft.component
    def drawer(
        on_change: ft.ControlEventHandler[ft.NavigationDrawer] | None,
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
            on_change=on_change,
        )

    # ========================================================
    # DESTINATION
    # ========================================================

    @staticmethod
    def _destination(page) -> ft.NavigationDrawerDestination:

        return ft.NavigationDrawerDestination(
            label=page.label,
            icon=NavBar._icon_for(page.path),
        )

    # ========================================================
    # ICONES
    # ========================================================

    @staticmethod
    def _icon_for(path: str):

        icons = {
            "/": ft.Icons.HOME_OUTLINED,
            "/about": ft.Icons.INFO_OUTLINED,
            "/counter": ft.Icons.EXPOSURE_PLUS_1,
            "/test": ft.Icons.BUG_REPORT_OUTLINED,
        }

        return icons.get(
            path,
            ft.Icons.CIRCLE_OUTLINED,
        )

    @staticmethod
    def path_for_selected_index(selected_index: int | None) -> str | None:

        destinations = [page for page in PAGES if page.label is not None]

        if selected_index is None:
            return None

        if selected_index < 0 or selected_index >= len(destinations):
            return None

        return destinations[selected_index].path
