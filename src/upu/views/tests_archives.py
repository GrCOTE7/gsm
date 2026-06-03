import flet as ft

from upu.views.page_template import named_view


def build() -> ft.Control:

    def ext_link(e, type):
        if type == 1:
            open_url(e, "https://example.com/1")
        open_url(e, "https://example.com/1")

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
                ft.Icon(ft.Icons.SCIENCE, size=28),
                ft.Text("Tests (Archives)", size=28, weight=ft.FontWeight.W_600),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        "Page archives de tests rapides.",
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
                ft.Row(
                    height=28,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.VerticalDivider(
                            width=16,
                            thickness=3,
                            color=ft.Colors.LIGHT_GREEN_ACCENT_400,
                        ),
                        ft.Text("Ready for more...", size=14),
                    ],
                ),
            ]
        ),
    )
