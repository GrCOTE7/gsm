import flet as ft

from devs.pages.page_template import named_view


def build() -> ft.Control:
    sport_container = ft.Container(
        width=320,
        padding=ft.Padding.symmetric(horizontal=10, vertical=3),
        border_radius=7,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        content=ft.Text("Contenu additionnel dans un container"),
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
