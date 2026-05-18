import webbrowser

import flet as ft

from upu.config import (
    GITHUB_LATEST_RELEASE_PAGE,
    VERSION,
    get_latest_release_info,
    get_latest_stable_version,
    is_update_available,
)


def build_release_update_card(width: int = 360) -> ft.Control:
    latest_release = get_latest_release_info(allow_remote=False)
    latest_version = get_latest_stable_version(allow_remote=False)
    update_available = is_update_available(VERSION, allow_remote=False)
    release_page_url = (
        str(latest_release.get("html_url") or "").strip() or GITHUB_LATEST_RELEASE_PAGE
    )

    def open_latest_release(e):
        page = getattr(e.control, "page", None)
        platform = getattr(page, "platform", None)
        is_mobile = False
        if platform is not None:
            platform_is_mobile = getattr(platform, "is_mobile", None)
            if callable(platform_is_mobile):
                is_mobile = bool(platform_is_mobile())
            else:
                platform_name = getattr(platform, "name", str(platform)).lower()
                is_mobile = platform_name in {"android", "ios"}

        if is_mobile and page is not None and hasattr(page, "launch_url"):

            async def _open_mobile_url() -> None:
                try:
                    await page.launch_url(release_page_url)
                except Exception:
                    webbrowser.open(release_page_url)

            page.run_task(_open_mobile_url)
            return

        webbrowser.open(release_page_url)

    status_text = (
        "Nouvelle version disponible" if update_available else "Application a jour"
    )
    status_color = ft.Colors.ORANGE_500 if update_available else ft.Colors.GREEN_500

    return ft.Container(
        width=width,
        padding=ft.Padding.symmetric(horizontal=10, vertical=3),
        border_radius=7,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text("Mises a jour", weight=ft.FontWeight.BOLD, size=18),
                ft.Text(f"Version locale: {VERSION}"),
                ft.Text(f"Derniere stable GitHub: {latest_version}"),
                ft.Text(status_text, color=status_color, weight=ft.FontWeight.W_600),
                ft.FilledButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.OPEN_IN_NEW, size=16),
                            ft.Text("Voir la derniere release"),
                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    on_click=open_latest_release,
                ),
            ],
        ),
    )
