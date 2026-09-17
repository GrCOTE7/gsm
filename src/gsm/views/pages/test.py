# src/gsm/views/pages/test.py
import flet as ft

from ...components.diagnostic import DiagnosticBlock
from ...views.partials.header import Header


class TestPage:
    """Page 4 'Test'."""

    @staticmethod
    @ft.component
    def view() -> ft.Control:
        return ft.Column(
            controls=[
                Header.view(),
                ft.Text("Test ready.", size=28, weight=ft.FontWeight.BOLD),
                DiagnosticBlock.view(),
                ft.Text(
                    "Pour participer au projet : GH ! http://GitHub.com/GrCOTE7/GSM",
                    weight=ft.FontWeight.BOLD,
                ),
            ],
        )
