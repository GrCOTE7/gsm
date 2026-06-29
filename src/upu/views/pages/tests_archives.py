import flet as ft

from upu.views.templates.default import named_view
from upu.views.footers.ready_more import ready_more
from gc7_tools.helpers import sepa_major, sepa_outlined

from upu.guests.g260530_nom import subject


def build() -> ft.Control:

    return named_view(
        ft.Row(
            controls=[
                ft.Icon(ft.CupertinoIcons.ARCHIVEBOX_FILL, size=28),
                ft.Text("Tests (Archives)", size=28, weight=ft.FontWeight.W_600),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        "Page archives des tests rapides.",
        extra_top_gap=0,
        extra=ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        controls=[sepa_major(),subject(), sepa_major()]
                    ),
                ),
                ready_more(True),  # ☢️ fix footer en bas
            ],
        ),
    )
