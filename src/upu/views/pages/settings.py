import flet as ft

from upu.views.templates.default import named_view
from upu.views.partials import build_release_update_card


def build() -> ft.Control:
    return named_view(
        ft.Row(
            controls=[
                ft.Icon(ft.Icons.SETTINGS, size=28),
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
        extra=build_release_update_card(),
    )
