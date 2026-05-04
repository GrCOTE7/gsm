import asyncio

import flet as ft

from devs.navigation import NAV_ITEMS, route_to_index


def Drawer(page: ft.Page) -> ft.NavigationDrawer:
    def on_drawer_change(e) -> None:
        index = e.control.selected_index
        if 0 <= index < len(NAV_ITEMS):
            target_route = NAV_ITEMS[index]["route"]
            if page.route != target_route:
                page.run_task(page.push_route, target_route)
        # pas besoin de close_drawer: push_route reconstruit la vue et ferme le drawer

    drawer = ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(
                icon=item["icon"],
                selected_icon=item["selected_icon"],
                label=item["label"],
            )
            for item in NAV_ITEMS
        ],
        selected_index=route_to_index(page.route),
        on_change=on_drawer_change,
    )
    return drawer


def AppBar(page: ft.Page) -> ft.AppBar:
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

    def open_drawer(e) -> None:
        page.run_task(open_drawer_safe)

    return ft.AppBar(
        leading=ft.IconButton(icon=ft.Icons.MENU, on_click=open_drawer),
        leading_width=48,
        title=ft.Text("GC7 Test"),
        center_title=False,
        bgcolor=ft.Colors.SURFACE,
        elevation=2,
    )
