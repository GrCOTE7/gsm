from upu.routes.registry import get_view_builder, has_route
from upu.ui.navigation import AppBar, Drawer
import flet as ft
from upu.config import APP_NAME


class NavigationController:
    def __init__(self, page):
        self.page = page

    def route_change(self, e: ft.RouteChangeEvent) -> None:
        print("Route change:", e.route)
        self.render_route(e.route or "/")

    def build_view(self, route: str) -> ft.View:
        builder = get_view_builder(route)
        return ft.View(
            route=route,
            appbar=AppBar(self.page, APP_NAME),
            drawer=Drawer(self.page),
            padding=0,
            spacing=0,
            controls=[builder()],
        )

    def render_route(self, raw_route: str) -> None:
        self.page.views.clear()
        route = raw_route.split("?")[0]
        route = route if has_route(route) else "/"
        self.page.views.append(self.build_view(route))
        self.page.update()

    async def view_pop(self, e: ft.ViewPopEvent) -> None:
        if e.view is not None and e.view in self.page.views:
            self.page.views.remove(e.view)
        target_route = self.page.views[-1].route if self.page.views else "/"
        await self.page.push_route(target_route)

    def go_to(self, route: str) -> None:
        if (self.page.route or "/") == route:
            self.render_route(route)
            return
        self.page.run_task(self.push_route_async, route)

    async def push_route_async(self, route: str) -> None:
        await self.page.push_route(route)
