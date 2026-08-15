# src/gsm/layouts/main_layout.py
import flet as ft
from gsm.components.nav_bar import NavBar
from gsm.config.app_window import AppWindow
from gsm.routing.routes_registry import PAGES


class MainLayout:
    """
    Coquille persistante de l'application (header + zone de contenu).

    C'est une "layout route" au sens du Router déclaratif de Flet : elle
    est déclarée comme `component` d'une `ft.Route` qui a des `children`,
    et elle place ses enfants via `ft.use_route_outlet()` — l'équivalent
    exact d'un `<Outlet />` en React Router.
    """

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
                if ft.is_route_active(page_def.path, exact=(page_def.path == "/"))
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

        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                expand=True,
                controls=[
                    # XXX menu burger + logo + slogan
                    # ft.Container(margin=ft.Margin(top=50)), ← Espace pour NavBar 
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("GSM", size=20, weight=ft.FontWeight.BOLD),
                            NavBar.view(),
                        ],
                    ),
                    ft.Divider(),
                    ft.Container(content=outlet, expand=True),
                ],
            ),
        )
