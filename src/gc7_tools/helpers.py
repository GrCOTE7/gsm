import flet as ft


def sepa(color="LIGHT_GREEN_ACCENT_400"):
    return ft.Column(
        controls=[
            ft.Divider(
                height=16,
                thickness=2,
                color=getattr(ft.Colors, color),
            ),
        ],
    )


def sepa_outlined(color="LIGHT_GREEN_ACCENT_400"):
    return ft.Column(
        controls=[
            ft.Container(
                height=5,
                border=ft.Border.all(2, getattr(ft.Colors, color)),
                border_radius=4,
            )
        ]
    )
