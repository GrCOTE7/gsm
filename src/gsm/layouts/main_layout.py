# src/gsm/layouts/main_layout.py

import flet as ft

from gsm.components.nav_bar import NavBar
from gsm.config.app_window import AppWindow
from gsm.routing.routes_registry import PAGES


class MainLayout:

    @staticmethod
    def _fallback_page_label(route: str | None) -> str:
        if not route or route == "/":
            return "Accueil"

        clean_route = route.split("?", 1)[0].split("#", 1)[0].strip("/")

        if not clean_route:
            return "Accueil"

        last_segment = clean_route.split("/")[-1]

        return last_segment.replace("-", " ").replace("_", " ").title()

    @staticmethod
    @ft.component
    def view() -> ft.Control:

        current_page = next(
            (
                page_def
                for page_def in PAGES
                if ft.is_route_active(
                    page_def.path,
                    exact=(page_def.path == "/"),
                )
            ),
            None,
        )

        page_label = (
            current_page.label
            if current_page is not None and current_page.label is not None
            else MainLayout._fallback_page_label(ft.context.page.route)
        )

        ft.context.page.title = AppWindow.build_title(page_label)

        outlet = ft.use_route_outlet()
        pagelet_ref = ft.Ref[ft.Pagelet]()

        async def handle_menu_click(_: ft.Event[ft.IconButton]) -> None:
            if pagelet_ref.current is not None:
                await pagelet_ref.current.show_drawer()

        async def handle_drawer_change(e: ft.Event[ft.NavigationDrawer]) -> None:
            target = NavBar.path_for_selected_index(e.control.selected_index)

            if target is None:
                return

            if pagelet_ref.current is not None:
                await pagelet_ref.current.close_drawer()

            ft.context.page.navigate(target)

        return ft.Pagelet(
            ref=pagelet_ref,
            expand=True,
            appbar=NavBar.app_bar(page_label, on_menu_click=handle_menu_click),
            drawer=NavBar.drawer(on_change=handle_drawer_change),
            content=ft.Container(
                content=outlet,
                expand=True,
                padding=20,
            ),
        )
