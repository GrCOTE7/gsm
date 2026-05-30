import flet as ft

from upu.helpers.app_actions import close_app, open_url
from upu.helpers.buttons import filled_button
from upu.views.partials import build_release_update_card
from upu.views.page_template import named_view

import webbrowser


def open_external(e):
    webbrowser.open("https://example.com")


def build() -> ft.Control:

    def ext_link(e, type):
        if type == 1:
            open_url(e, "https://example.com/1")
        open_url(e, "https://example.com/1")

    def open_external(e):
        webbrowser.open("https://example.com")

    def provisorySubMenu():
        return ft.Container(
            padding=ft.Padding.only(bottom=20),
            content=ft.Row(
                controls=[
                    filled_button(
                        content="Tests2",
                        on_click=lambda e: e.page.go("/tests2"),
                    ),
                    filled_button(
                        content="Fermer l'application",
                        on_click=lambda e: close_app(e),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )

    def extLinks():
        return ft.Container(
            padding=ft.Padding.only(bottom=20),
            content=ft.Row(
                controls=[
                    filled_button(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.OPEN_IN_NEW, size=16),
                                ft.Text("open_url()"),
                            ],
                            spacing=8,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        on_click=lambda e: ext_link(e, 1),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )

    def nom_thomas():
        rep = "\n".join(
            " ".join(str(i * j) for j in range(1, i + 1)) for i in range(1, 6)
        )
        return ft.Text('Nom & Thomas \'s script:\n'+rep, size=20, weight=ft.FontWeight.W_500)

    return named_view(
        ft.Row(
            controls=[
                ft.Icon(ft.Icons.SCIENCE, size=28),
                ft.Text("Tests", size=28, weight=ft.FontWeight.W_600),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        "Page pour tests rapides.",
        extra_top_gap=0,
        extra=ft.Column(
            [
                provisorySubMenu(),
                extLinks(),
                build_release_update_card(),
                nom_thomas(),
            ]
        ),
    )
