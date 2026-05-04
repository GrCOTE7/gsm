import flet as ft

from devs.pages.page_template import named_view


def build() -> ft.Control:
    return named_view(
        ft.Row(
            controls=[
                ft.Icon(ft.Icons.SETTINGS),
                ft.Text("Settings", size=28, weight=ft.FontWeight.W_600),
            ],
            # vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        "Settings Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non "
        "urna sit amet augue tempor faucibus. Cras facilisis, purus ut "
        "ullamcorper tristique, libero lectus vehicula elit, vitae posuere "
        "quam erat at magna. Donec porta, turpis nec eleifend tincidunt, "
        "massa turpis gravida sapien, sed feugiat odio velit ut nisl of Settings.",
        extra=ft.Container(
            width=320,
            padding=ft.Padding.symmetric(horizontal=10, vertical=3),
            border_radius=7,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            content=ft.Column(controls=[ft.Text("Oki 21a"), ft.Text("OKi 21b")]),
        ),
    )
