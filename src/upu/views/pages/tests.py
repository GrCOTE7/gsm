import flet as ft

from upu.views.templates.default import named_view
from upu.views.footers.ready_more import ready_more
from upu.helpers.app_actions import close_app, open_url

from gc7_tools.helpers import sepa, sepa_outlined

from upu.guests import g260799_ as guest
from typing import cast
from upu.helpers.snackbar import show_snackbar

# print(dir(page))
def _tests_header() -> ft.Row:

    def simple_tap(e: ft.TapEvent):
        disclaimer = "🔔 Really want to close ? Then double tap ! (Or CTRL + C in CLI)"
        page = e.page
        print(disclaimer)
        # show_snackbar(page, disclaimer, bgcolor=ft.Colors.ORANGE_400)
        show_snackbar(page, disclaimer, color=ft.Colors.ORANGE_200, bgcolor=ft.Colors.TRANSPARENT, duration=7000, floating=True, show_close_icon=True)

    return ft.Row(
        controls=[
            ft.GestureDetector(
                ft.Icon(
                    ft.Icons.ARCHIVE_OUTLINED,
                    size=18,
                    color=ft.Colors.CYAN_400,
                    tooltip="Aller aux Archives",
                ),
                margin=ft.Margin(0, 0, 0, 0),
                on_tap=lambda e: e.page.run_task(e.page.push_route, "/archives"),  # type: ignore
                mouse_cursor=ft.MouseCursor.CLICK,
            ),
            ft.Container(
                expand=True,
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.SCIENCE, size=30),
                        ft.Text(
                            "Tests",
                            size=28,
                            weight=ft.FontWeight.W_600,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    # vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
            ),
            ft.GestureDetector(
                content=ft.Icon(
                    ft.CupertinoIcons.CLEAR_CIRCLED,
                    size=18,
                    color=ft.Colors.RED_200,
                    tooltip="Fermer l'App",
                ),
                mouse_cursor=ft.MouseCursor.CLICK,
                on_tap=simple_tap,
                on_double_tap=lambda e: close_app(e),
            ),
        ],
    )


def build() -> ft.Control:

    return named_view(
        _tests_header(),
        "Page pour tests rapides.",
        extra_top_gap=0,
        # extra=sepa_outlined('ORANGE_400'),
        extra=ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        controls=[
                            sepa_outlined("CYAN_400"),
                            guest.subject(),
                            # sepa_outlined("CYAN_400"),
                            # ft.Text("→ Ready où ? Ici sera le prochain test !"),
                            # sepa_outlined("CYAN_400"),
                        ]
                    ),
                ),
                ready_more(),
            ],
        ),
    )
