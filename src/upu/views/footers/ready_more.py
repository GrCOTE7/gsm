import flet as ft
from gc7_tools.helpers import sepa_outlined


def ready_more() -> ft.Column:

    return ft.Column(
        controls=[
            sepa_outlined(),
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
            )
        ]
    )
