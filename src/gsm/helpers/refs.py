import flet as ft
from upu.helpers.buttons import (
    extLink,
)  # XXX to transfer all upu.helpers in gsm.helpers

gh_url = "http://GitHub.com/GrCOTE7/GSM"


def gh_link(color="LIGHT_GREEN_ACCENT_400"):
    gh_link = extLink("Dépôt GitHub", gh_url, "Va et fork le projet !", "center")
    return gh_link


def year_day()-> int:
    from datetime import date

    return date.today().timetuple().tm_yday


def aff(txt):
    """Affiche le texte dans la console et le retourne."""
    return ft.Text(txt)
