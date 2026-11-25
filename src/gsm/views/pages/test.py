# src/gsm/views/pages/test.py
import flet as ft

from ...components.diagnostic import DiagnosticBlock
from ...views.partials.header import Header
from gsm.helpers.separators import sepa
from gsm.helpers.refs import aff, gh_link, gh_url, year_day


class TestPage:
    """Page 4 'Test'."""

    @staticmethod
    @ft.component
    def view() -> ft.Control:
        return ft.Column(
            controls=[
                # Header.view(),
                ft.Text("Test ready.", size=28, weight=ft.FontWeight.BOLD),
                DiagnosticBlock.view(),
                ft.Text(
                    f"Pour participer au projet : GH ! {gh_url}",
                    weight=ft.FontWeight.BOLD,
                ),
                gh_link(),
            ],
        )
