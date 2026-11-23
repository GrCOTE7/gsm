import flet as ft
from ...config.app_env import app_env


class Header:
    """Header partial view"""

    @staticmethod
    @ft.component
    def view() -> ft.Control:

        return ft.Column(
            controls=[
                ft.Text("Header.", size=28, weight=ft.FontWeight.BOLD),
            ]
        )
