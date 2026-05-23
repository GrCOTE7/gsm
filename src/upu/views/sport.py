import flet as ft

from upu.helpers.app_actions import open_url
from upu.helpers.buttons import filled_button
from upu.views.page_template import named_view


def build() -> ft.Control:
    def open_example_com(e):
        open_url(e, "https://example.com")

    sport_container = ft.Container(
        width=320,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.DIRECTIONS_RUN),
                        ft.Text("Ready for next session"),
                    ]
                ),
                filled_button(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.OPEN_IN_NEW, size=16),
                            ft.Text("Visiter example.com"),
                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    on_click=open_example_com,
                ),
            ]
        ),
    )

    return named_view(
        ft.Row(
            controls=[
                ft.Icon(ft.Icons.DIRECTIONS_RUN, size=28),
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
