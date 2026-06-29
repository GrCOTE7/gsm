import flet as ft

from upu.views.templates.default import named_view
from upu.views.footers.ready_more import ready_more
from gc7_tools.helpers import sepa_major, sepa_outlined

# from upu.guests.g260530_nom import subject as s1
# from upu.guests.g260602_mln_913 import subject as s2

from upu.guests import REGISTRY


def build() -> ft.Control:
    controls = []

    controls.append(sepa_outlined())

    for s in reversed(REGISTRY):
        controls.append(s())
        controls.append(sepa_outlined())
    
    # print("REGISTRY =", REGISTRY)
    
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
                    content=ft.Column(controls=controls, scroll=ft.ScrollMode.AUTO)
                ),
                ready_more(True)
            ],
        ),
    )
