import flet as ft

from gc7_tools.helpers import sepa, sepa_outlined
from upu.views.page_template import named_view, ready
from upu.guests.mlm_913 import tests_views

# def ready():
#     return ft.Text("→ Ready for quick test21!", size=14, weight=ft.FontWeight.W_400)


def _tests_header() -> ft.Row:

    return ft.Row(
        controls=[
            ft.GestureDetector(
                ft.Icon(
                    ft.Icons.ARCHIVE_OUTLINED,
                    size=18,
                    color=ft.Colors.CYAN_400,
                    tooltip="Aller à la page Archives",
                ),
                margin=ft.Margin(0, 0, 0, 0),
                on_tap=lambda e: print("Go Archives !"), # ❌ reroute!
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
                on_tap=lambda e: print("Really want to close ? Then double tap !"),
                on_double_tap=lambda e: print("close !"), # ❌ real close!
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
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
                    content=tests_views(),
                ),
                sepa_outlined(),
                ready(),
            ],
        ),
    )
