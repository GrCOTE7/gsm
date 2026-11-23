# src/gsm/views/pages/about.py
import flet as ft


class AboutPage:
    """Page 'À propos'."""

    @staticmethod
    @ft.component
    def view() -> ft.Control:
        return ft.Column(
            controls=[
                ft.Text("À propos", size=28, weight=ft.FontWeight.BOLD),
            ],
        )
