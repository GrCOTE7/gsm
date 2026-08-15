# src/gsm/routing/router.py
import flet as ft
# from gsm.config.app_config import config
from gsm.layouts.main_layout import MainLayout
from gsm.routing.routes_registry import PAGES
from gsm.views.pages.not_found import NotFoundPage

class AppRouter:
    """
    Construit l'arbre `ft.Route` à partir du registre `PAGES`
    (gsm/routing/routes_registry.py) — seule source de vérité sur les pages.

    Depuis Flet 0.85, le routage déclaratif se fait avec `ft.Router` +
    `ft.Route` (inspiré de React Router) : plus besoin de gérer
    `page.on_route_change` / `page.views` à la main.
    """

    @staticmethod
    def _page_routes() -> list[ft.Route]:
        return [ft.Route(path=page.segment, component=page.component) for page in PAGES]

    @staticmethod
    def routes() -> list[ft.Route]:
        return [
            ft.Route(
                # Route "layout" sans `path` : elle englobe toutes les
                # routes filles avec le même MainLayout (header, footer...).
                component=MainLayout.view,
                children=[
                    # Routes filles : toutes les pages déclarées dans le registre
                    *AppRouter._page_routes(),
                    # Catch-all : doit rester en dernier, capture tout ce
                    # qui n'a matché aucune page ci-dessus. Reste englobée
                    # dans MainLayout (contrairement à `not_found=` du
                    # Router, qui s'affiche hors layout).
                    ft.Route(path=":path*", component=NotFoundPage.view),
                ],
            ),
        ]

    @staticmethod
    @ft.component
    def view() -> ft.Control:
        return ft.SafeArea(ft.Router(routes=AppRouter.routes()))


# ---------------------------------------------

# from gsm.views.home import HomeView
# from gsm.views.login import LoginView
# from gsm.views.settings import SettingsView

# "/", HomeView,
# "/login", LoginView,
# "/settings", SettingsView, auth_required=True,
# "/user/:id", UserView, auth_required=True,

# IMPORTANT :
# Si la vue est un composant décoré (fonction),
# on l’instancie et on l’enveloppe dans un contrôle simple.

# ---------------------------------------------

# from dataclasses import dataclass


# @dataclass
# class Route:
#     path: str
#     view: type
#     auth_required: bool = False
#     transition: str = "fade"


# ROUTES = [
#     Route("/", CounterView),
# ]

# import re


# def match_route(route: str):
#     for r in ROUTES:
#         pattern = "^" + re.sub(r":(\w+)", r"(?P<\1>[^/]+)", r.path) + "$"
#         m = re.match(pattern, route)
#         if m:
#             return r, m.groupdict()
#     return None, {}


# def resolve_route(route: str):
#     r, params = match_route(route)

#     if not r:
#         from gsm.views.pages.p404 import NotFoundView

#         return NotFoundView()

#     # Instanciation déclarative
#     return r.view(**params) if params else r.view()


# def attach_router(page):

#     def on_route_change(e):
#         page.views.clear()
#         page.views.append(resolve_route(page.route))
#         page.update()

#     page.on_route_change = on_route_change
