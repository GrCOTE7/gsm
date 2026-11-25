import flet as ft

from gsm.services.update_service import get_update_info
from upu.helpers.app_actions import open_url
from upu.helpers.buttons import filled_button


def build_release_update_card(
    info: dict | None = None, width: int = 360
) -> ft.Control:
    """Carte « Mises à jour » : versions locale/GitHub et lien vers la release.

    `info` vient de `gsm.services.update_service.get_update_info()` : le passer
    évite un second appel réseau quand l'appelant l'a déjà récupéré.
    """
    info = info or get_update_info()

    local_version = str(info.get("local_version") or "?")
    latest_version = str(info.get("latest_version") or "?")
    update_available = bool(info.get("update_available"))
    release_url = str(info.get("html_url") or "")

    def open_latest_release(e):
        if release_url:
            open_url(e, release_url)

    status_text = (
        "Nouvelle version disponible" if update_available else "Application a jour"
    )
    status_color = ft.Colors.ORANGE_500 if update_available else ft.Colors.GREEN_500

    return ft.Container(
        width=width,
        margin=ft.Margin.symmetric(vertical=10),
        padding=ft.Padding.symmetric(horizontal=10, vertical=10),
        border_radius=7,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text("Mises à jour", weight=ft.FontWeight.BOLD, size=18),
                ft.Text(f"Version locale: {local_version}"),
                ft.Text(f"Dernière stable GitHub: {latest_version}"),
                ft.Text(status_text, color=status_color, weight=ft.FontWeight.W_600),
                filled_button(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.OPEN_IN_NEW, size=18),
                            ft.Text("Voir les dernières releases"),
                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    on_click=open_latest_release,
                ),
            ],
        ),
    )
