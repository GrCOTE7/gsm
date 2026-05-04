import flet as ft
import flet_audio  # noqa: F401

import gc7_tools.gc7 as gc7
import gc7_tools.screen_utils as screen_utils

from devs.appbar import AppBar, Drawer
from devs.pages import home, sport, settings

APP_NAME = "MyApp Test GC7"
VERSION = "0.0.1"

VIEWS = {
    "/home": home.build,
    "/sport": sport.build,
    "/settings": settings.build,
}


def main(page: ft.Page):
    screen_utils.gc7_rules(page, left=1526)  # 1526 ou 1912
    page.title = f"{APP_NAME} - v{VERSION}"

    def invite() -> None:
        print(gc7.curr_time(), page.route, ">")

    def build_view(route: str) -> ft.View:
        builder = VIEWS.get(route, home.build)
        return ft.View(
            route=route,
            appbar=AppBar(page),
            drawer=Drawer(page),
            padding=0,
            spacing=0,
            controls=[builder()],
        )

    def render_current_route() -> None:
        builder = VIEWS.get(page.route, home.build)
        route = page.route if page.route in VIEWS else "/home"
        page.views.clear()
        page.views.append(build_view(route))
        page.update()

    def on_route_change(e: ft.RouteChangeEvent) -> None:
        render_current_route()

    page.on_route_change = on_route_change

    async def on_view_pop(e: ft.ViewPopEvent) -> None:
        if e.view is not None and e.view in page.views:
            page.views.remove(e.view)
        target_route = page.views[-1].route if page.views else "/home"
        await page.push_route(target_route)

    page.on_view_pop = on_view_pop

    # from audio import main as audio_main # son 5 1eres et dernieres secondes d'un décompte
    # audio_main(page)

    if page.route not in VIEWS:
        page.run_task(page.push_route, "/home")
    else:
        render_current_route()

    invite()
    # print(page.width)


ft.run(main)
