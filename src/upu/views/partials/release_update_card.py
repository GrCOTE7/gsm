import flet as ft

from upu.config import (
    GITHUB_LATEST_RELEASE_PAGE,
    VERSION,
    get_latest_release_info,
    get_latest_stable_version,
    is_update_available,
)
from upu.helpers.app_actions import open_url
from upu.helpers.buttons import filled_button


def build_release_update_card(width: int = 360) -> ft.Control:
    latest_release = get_latest_release_info(timeout_seconds=2, allow_remote=True)
    latest_version = get_latest_stable_version(timeout_seconds=2, allow_remote=True)
    update_available = is_update_available(VERSION, allow_remote=True)
    release_page_url = GITHUB_LATEST_RELEASE_PAGE.removesuffix("/latest")

    def open_latest_release(e):
        open_url(e, release_page_url)

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
                ft.Text(f"Version locale: {VERSION}"),
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
