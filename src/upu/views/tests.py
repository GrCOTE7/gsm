import flet as ft

from upu.helpers.app_actions import close_app, open_url
from upu.helpers.buttons import filled_button
from upu.views.partials import build_release_update_card
from upu.views.page_template import named_view

import webbrowser


def open_external(e):
    webbrowser.open("https://example.com")


def build() -> ft.Control:

    def sepa():
        return ft.Column(
            controls=[
                ft.Divider(
                    height=16,
                    thickness=2,
                    color=ft.Colors.LIGHT_GREEN_ACCENT_400,
                ),
            ],
        )

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
                        on_click=lambda e: e.page.run_task(
                            e.page.push_route, "/tests2"
                        ),
                    ),
                    filled_button(
                        content="Archives",
                        on_click=lambda e: e.page.run_task(
                            e.page.push_route, "/archives"
                        ),
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
                sepa(),
                ft.Text('→ Ready for quick test!', size=14, weight=ft.FontWeight.W_400),
                sepa(),
                provisorySubMenu(),
                extLinks(),
                sepa(),
                build_release_update_card(),
            ]
        ),
    )
