import flet as ft

from devs.pages.page_template import named_view


def build() -> ft.Control:
    sport_container = ft.Container(
        width=320,
        content=ft.Row(
            [ft.Icon(ft.Icons.DIRECTIONS_RUN), ft.Text("Ready for next session")]
        ),
    )

    return named_view(
        ft.Row(
            controls=[
                ft.Icon(ft.Icons.DIRECTIONS_RUN),
                ft.Text("Sport", size=28, weight=ft.FontWeight.W_600),
            ],
            # vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        "Sport Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non "
        "urna sit amet augue tempor faucibus. Cras facilisis, purus ut "
        "ullamcorper tristique, libero lectus vehicula elit, vitae posuere "
        "quam erat at magna. Donec porta, turpis nec eleifend tincidunt, "
        "massa turpis gravida sapien, sed feugiat odio velit ut nisl of Sport.",
        sport_container,
    )
