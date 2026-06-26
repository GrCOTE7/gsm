import flet as ft

from upu.views.templates.default import named_view
from upu.views.footers.ready_more import ready_more


def build() -> ft.Control:

    def nom_thomas():
        rep = "\n".join(
            " ".join(str(i * j) for j in range(1, i + 1)) for i in range(1, 6)
        )
        return ft.Text(
            "Nom & Thomas 's script:\n" + rep, size=20, weight=ft.FontWeight.W_500
        )

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
            [
                ft.Column(
                    controls=[
                        ft.Divider(
                            height=16,
                            thickness=2,
                            color=ft.Colors.LIGHT_GREEN_ACCENT_400,
                        ),
                    ],
                ),
                nom_thomas(),
                ft.Column(
                    controls=[
                        ft.Divider(
                            height=16,
                            thickness=2,
                            color=ft.Colors.LIGHT_GREEN_ACCENT_400,
                        ),
                    ],
                ),
                ready_more(), # ❌ fix footer en bas
            ]
        ),
    )
