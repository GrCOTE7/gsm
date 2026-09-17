# src/gsm/views/pages/test.py
import flet as ft

from ...components.diagnostic import DiagnosticBlock
from ...config.app_env import app_env
from ...views.partials.header import Header


class TestPage:
    """Page 4 'Test'."""

    @staticmethod
    @ft.component
    def view() -> ft.Control:
        is_local = app_env.is_local()
        platform = app_env.plateform()
        return ft.Column(
            controls=[
                Header.view(),
                ft.Text("Test ready.", size=28, weight=ft.FontWeight.BOLD),
                ft.Text(f"{is_local = }", size=16),
                ft.Text(f"{platform = }", size=16),
                DiagnosticBlock.view(),
                ft.Text(
                    "Pour participer au projet : GH ! http://GitHub.com/GrCOTE7/GSM",
                    weight=ft.FontWeight.BOLD,
                ),
            ],
        )
