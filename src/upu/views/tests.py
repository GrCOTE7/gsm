import webbrowser

import flet as ft

from upu.views.page_template import named_view


def build() -> ft.Control:

    def close_app():
        print("Je vais fermer")

    tests_container = ft.Row(
        [
            ft.Button(
                "Ouvrir Google",
                on_click=lambda _: webbrowser.open("https://www.google.com"),
            ),
            ft.Button("Fermer l'application", on_click=close_app),
        ]
    )

    return named_view(
        ft.Row(
            controls=[
                ft.Icon(ft.Icons.SCIENCE_OUTLINED, size=28),
                ft.Text("Tests", size=28, weight=ft.FontWeight.W_600),
            ],
            # vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        "Tests Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non "
        "urna sit amet augue tempor faucibus. Cras facilisis, purus ut "
        "ullamcorper tristique, libero lectus vehicula elit, vitae posuere "
        "quam erat at magna. Donec porta, turpis nec eleifend tincidunt, "
        "massa turpis gravida sapien, sed feugiat odio velit ut nisl of Tests.",
        tests_container,
    )
