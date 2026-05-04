import flet as ft

from devs.pages.page_template import named_view


def build() -> ft.Control:
    icons_list = [
        "HOME",
        "DIRECTIONS_RUN",
        "SETTINGS",
        "ADD",
        "DELETE",
        "EDIT",
        "SEARCH",
        "FAVORITE",
        "STAR",
        "INFO",
        "WARNING",
        "ERROR",
        "CHECK",
        "CLOSE",
        "MENU",
        "CLOSE",
        "ARROW_UPWARD",
        "ARROW_DOWNWARD",
        "ARROW_BACK",
        "ARROW_FORWARD",
        "REFRESH",
        "SAVE",
        "PRINT",
        "SHARE",
        "DOWNLOAD",
        "UPLOAD",
    ]
    sport_container = ft.Container(
        width=320,
        height=500,
        padding=ft.padding.symmetric(horizontal=10, vertical=3),
        border_radius=7,
        # bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        content=ft.Column(
            [
                ft.Row(
                    controls=[
                        ft.Icon(getattr(ft.Icons, f"{icon}_OUTLINED")),
                        ft.Icon(getattr(ft.Icons, f"{icon}")),
                        ft.Text(icon),
                    ],
                )
                for icon in icons_list
            ],
            scroll=ft.ScrollMode.AUTO,
            height=300,
        ),
    )

    return named_view(
        "Sport",
        "Sport Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non "
        "urna sit amet augue tempor faucibus. Cras facilisis, purus ut "
        "ullamcorper tristique, libero lectus vehicula elit, vitae posuere "
        "quam erat at magna. Donec porta, turpis nec eleifend tincidunt, "
        "massa turpis gravida sapien, sed feugiat odio velit ut nisl of Sport.",
        sport_container,
    )
