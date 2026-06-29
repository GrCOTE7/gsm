import asyncio

import flet as ft

from upu.config import DEFAULT_ROUTE
from upu.helpers.snackbar import show_snackbar
from upu.routes import get_routes, route_to_index
from upu.services.storage.storage_factory import create_storage
from upu.services.update_service import UpdateService

NAV_ITEMS = get_routes()

# 🖥️ 6) Intégration dans l’UI Flet


def _get_update_service(page: ft.Page) -> UpdateService:
    service = getattr(page, "_update_service", None)
    if service is None:
        service = UpdateService(create_storage(page))
        setattr(page, "_update_service", service)
    return service


def Drawer(page: ft.Page) -> ft.NavigationDrawer:
    def on_drawer_change(e) -> None:
        index = e.control.selected_index
        if 0 <= index < len(NAV_ITEMS):
            target_route = NAV_ITEMS[index].route
            if page.route != target_route:
                page.run_task(page.push_route, target_route)

    return ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(
                icon=item.icon,
                selected_icon=item.selected_icon,
                label=item.label,
            )
            for item in NAV_ITEMS
        ],
        selected_index=route_to_index(page.route),
        on_change=on_drawer_change,
    )


def AppBar(page: ft.Page, title: str) -> ft.AppBar:
    async def check_latest_safe() -> None:
        service = _get_update_service(page)

        try:
            latest = await asyncio.to_thread(service.check_latest)
            checked_at = service.get_last_check_at() or "inconnue"
            message = f"Derniere version: {latest} (check: {checked_at})"
        except Exception as exc:  # noqa: BLE001
            message = f"Echec check update: {exc}"

        show_snackbar(page, message, 5000)

    def on_check_latest(_e) -> None:
        page.run_task(check_latest_safe)

    async def open_drawer_safe() -> None:

        if getattr(page, "_drawer_opening", False):
            return

        setattr(page, "_drawer_opening", True)
        try:
            for attempt in range(2):
                if not page.views:
                    return

                top_view = page.views[-1]
                if top_view.drawer is None:
                    return

                top_view.drawer.selected_index = route_to_index(page.route)

                try:
                    await page.show_drawer()
                    return
                except RuntimeError as err:
                    msg = str(err)
                    timed_out = (
                        "Timeout waiting for invoke method listener" in msg
                        and ".show_drawer" in msg
                    )
                    if not timed_out or attempt == 1:
                        raise
                    await asyncio.sleep(0.05)
        finally:
            setattr(page, "_drawer_opening", False)

    def open_drawer(_e) -> None:
        page.run_task(open_drawer_safe)

    def go_default(_e) -> None:
        # DEFAULT_ROUTE[1:].capitalize()
        if page.route != DEFAULT_ROUTE:
            page.run_task(page.push_route, DEFAULT_ROUTE)

    def go_home_icon(_e) -> None:
        if page.route != "/home":
            page.run_task(page.push_route, "/home")

    def go_tests(_e) -> None:
        if page.route != "/tests":
            page.run_task(page.push_route, "/tests")

    def page_is(route_name) -> bool:
        return page.route[1:] == route_name

    print(f'{page_is("home") = }')

    arr = range(3)
    print(*arr[1:])

    tooltip=''
    mouse_cursor=ft.MouseCursor.CELL
    if not page_is('tests'):
        mouse_cursor = ft.MouseCursor.CLICK
        tooltip = 'Aller à la page Tests'

    return ft.AppBar(
        leading=ft.IconButton(icon=ft.Icons.MENU, on_click=open_drawer),
        leading_width=48,  # 48
        title=ft.Row(
            spacing=48,
            tight=True,
            controls=[
                ft.GestureDetector(
                    content=ft.Image(src="icon.png", width=32, height=32),
                    mouse_cursor=(
                        ft.MouseCursor.CELL if page_is("home") else ft.MouseCursor.CLICK
                    ),
                    on_tap=go_home_icon,
                    tooltip=None if page_is("home") else "Aller à l'accueil",
                ),
                
                ft.GestureDetector(
                    content=ft.Text(value=title),
                    mouse_cursor=mouse_cursor,
                    on_tap=go_tests,
                    tooltip=tooltip
                ),
            ],
        ),
        # actions=[
        #     ft.IconButton(
        #         icon=ft.Icons.SYSTEM_UPDATE_ALT,
        #         tooltip="Verifier la derniere version",
        #         on_click=on_check_latest,
        #     )
        # ],
        center_title=False,
        bgcolor=ft.Colors.SURFACE,
        elevation=2,
    )
