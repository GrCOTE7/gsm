import flet as ft

from devs.navigation import NAV_ITEMS, route_to_index


def Drawer(page: ft.Page) -> ft.NavigationDrawer:
    def on_drawer_change(e) -> None:
        index = e.control.selected_index
        if 0 <= index < len(NAV_ITEMS):
            target_route = NAV_ITEMS[index]["route"]
            if page.route != target_route:
                page.run_task(page.push_route, target_route)
        page.run_task(page.close_drawer)

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
    def open_drawer(e) -> None:
        if page.views:
            top_view = page.views[-1]
            if top_view.drawer is not None:
                top_view.drawer.selected_index = route_to_index(page.route)
        page.run_task(page.show_drawer)

    return ft.AppBar(
        leading=ft.IconButton(icon=ft.Icons.MENU, on_click=open_drawer),
        leading_width=48,
        title=ft.Text("MyApp"),
        center_title=False,
        bgcolor=ft.Colors.SURFACE,
        elevation=2,
    )
