# src/gsm/views/pages/about.py
import flet as ft

from gsm.helpers.separators import sepa
from gsm.helpers.refs import aff, gh_link, gh_url, year_day


class HomePage:
    """Page 'À propos'."""

    @staticmethod
    @ft.component
    def view() -> ft.Control:
        print(f"Home Page - Day #{year_day()}")
        return ft.Column(
            controls=[
                ft.Text("Accueil", size=28, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Application Flet déclarative\n\n'GSM', projet collaboratif francophone basé sur Python et Flet (Declarative mode - React & Flutter-like)."
                ),
                sepa(),
                ft.Text(
                    f"Pour participer au projet : GH ! {gh_url}",
                    weight=ft.FontWeight.BOLD,
                ),
                gh_link(),
                sepa(),
                aff(f"Jour de l'année : {year_day()}"),
            ],
        )
