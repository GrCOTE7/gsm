import flet as ft


class Footer:
    """Footer partial view"""

    @staticmethod
    @ft.component
    def view() -> ft.Control:

        return ft.Column(
            controls=[
                ft.Text("Footer.", size=28, weight=ft.FontWeight.BOLD),
            ]
        )
