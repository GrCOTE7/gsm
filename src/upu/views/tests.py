import flet as ft

from gc7_tools.helpers import sepa, sepa_outlined
from upu.views.page_template import named_view, ready
from upu.guests.mlm_913 import tests_views

# def ready():
#     return ft.Text("→ Ready for quick test21!", size=14, weight=ft.FontWeight.W_400)


def _tests_header() -> ft.Row:
    return ft.Row(
        controls=[
            ft.Icon(ft.Icons.SCIENCE, size=28),
            ft.Text("Tests", size=28, weight=ft.FontWeight.W_600),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
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

