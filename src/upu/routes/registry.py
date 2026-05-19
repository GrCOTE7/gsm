from collections.abc import Callable
from dataclasses import dataclass

import flet as ft

from upu.views import home, icons, settings, sport, tests

ViewBuilder = Callable[[], ft.Control]


@dataclass(frozen=True)
class RouteDefinition:
    route: str
    label: str
    icon: ft.IconData
    selected_icon: ft.IconData
    builder: ViewBuilder


ROUTES: tuple[RouteDefinition, ...] = (
    RouteDefinition(
        route="/home",
        label="Accueil",
        icon=ft.Icons.HOME_OUTLINED,
        selected_icon=ft.Icons.HOME,
        builder=home.build,
    ),
    RouteDefinition(
        route="/sport",
        label="Sport",
        icon=ft.Icons.DIRECTIONS_RUN_OUTLINED,
        selected_icon=ft.Icons.DIRECTIONS_RUN,
        builder=sport.build,
    ),
    RouteDefinition(
        route="/icons",
        label="Icônes",
        icon=ft.Icons.APPS,
        selected_icon=ft.Icons.DIRECTIONS_RUN,
        builder=icons.build,
    ),
    RouteDefinition(
        route="/settings",
        label="Parametres",
        icon=ft.Icons.SETTINGS_OUTLINED,
        selected_icon=ft.Icons.SETTINGS,
        builder=settings.build,
    ),
    RouteDefinition(
        route="/tests",
        label="Tests",
        icon=ft.Icons.OUTLINED_FLAG,
        selected_icon=ft.Icons.CLOSE,
        builder=tests.build,
    ),
)

VIEW_BUILDERS: dict[str, ViewBuilder] = {
    definition.route: definition.builder for definition in ROUTES
}

DEFAULT_VIEW_BUILDER = ROUTES[0].builder


def get_view_builder(route: str) -> ViewBuilder:
    return VIEW_BUILDERS.get(route, DEFAULT_VIEW_BUILDER)


def has_route(route: str) -> bool:
    return route in VIEW_BUILDERS


def get_routes() -> tuple[RouteDefinition, ...]:
    return ROUTES


def route_to_index(route: str) -> int:
    for index, definition in enumerate(ROUTES):
        if definition.route == route:
            return index
    return 0
