# src/gsm/views/not_found.py
import flet as ft


class NotFoundPage:
    """Page affichée quand aucune route ne correspond (404)."""

    @staticmethod
    @ft.component
    def view() -> ft.Control:
        return ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("404", size=48, weight=ft.FontWeight.BOLD),
                ft.Text("Page introuvable", size=20),
                ft.FilledButton(
                    "Retour à l'accueil",
                    on_click=lambda _: ft.context.page.navigate("/"),
                ),
            ],
        )
