# src/gsm/views/pages/home.py
import flet as ft

from gsm.helpers.separators import sepa
from gsm.helpers.refs import aff, gh_link, gh_url, year_day
from gsm.services.update_service import get_update_info
from gsm.views.partials.release_update_card import build_release_update_card


class HomePage:
    """Page 'Accueil'."""

    @staticmethod
    @ft.component
    def view() -> ft.Control:
        print(f"Home Page - Day #{year_day()}")

        controls: list[ft.Control] = [
            ft.Row(
                controls=[
                    ft.Icon(ft.Icons.HOME, size=32),
                    ft.Text("Accueil", size=28, weight=ft.FontWeight.BOLD),
                ],
            ),
            ft.Text(
                "Application Flet déclarative\n\n'GSM', projet collaboratif francophone basé sur Python et Flet (Declarative mode - React & Flutter-like)."
            ),
        ]

        # Carte « Mises à jour » : uniquement quand une release plus récente
        # que la version embarquée existe (sinon l'accueil reste sobre).
        update_info = get_update_info()
        if update_info["update_available"]:
            controls.append(build_release_update_card(update_info))

        controls.extend(
            [
                sepa(),
                ft.Text(
                    f"Pour participer au projet : GH ! {gh_url}",
                    weight=ft.FontWeight.BOLD,
                ),
                gh_link(),
                sepa(),
                aff(f"Jour de l'année : {year_day()}"),
            ]
        )

        return ft.Column(controls=controls)
