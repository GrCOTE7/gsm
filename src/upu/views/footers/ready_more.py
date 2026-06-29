import flet as ft
from gc7_tools.helpers import sepa_outlined


def ready_more(always=False) -> ft.Column:
    
    always_msg = 'Always r' if always else 'R'
    always_msg += 'eady for more...'
    
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
                    ft.Text(always_msg, size=14),
                ],
            )
        ]
    )
