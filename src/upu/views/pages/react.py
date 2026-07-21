import flet as ft
from urllib import request as urlrequest

try:
    from flet_webview import WebView as EmbeddedWebView
except Exception:  # noqa: BLE001
    EmbeddedWebView = None

from upu.helpers.app_actions import open_url
from upu.views.templates.default import named_view

COTE_URL = "https://cote7.com"


def build() -> ft.Control:
    status = ft.Text(
        "Chargement de cote7.com dans la vue intégrée.",
        size=12,
        color=ft.Colors.BLUE_GREY_300,
    )

    webview_container = ft.Container(
        width=340,
        height=520,
        border_radius=10,
        padding=8,
        border=ft.Border(
            top=ft.BorderSide(1, ft.Colors.BLUE_GREY_700),
            right=ft.BorderSide(1, ft.Colors.BLUE_GREY_700),
            bottom=ft.BorderSide(1, ft.Colors.BLUE_GREY_700),
            left=ft.BorderSide(1, ft.Colors.BLUE_GREY_700),
        ),
        bgcolor=ft.Colors.BLACK,
    )

    def _embedding_block_reason(url: str) -> str | None:
        try:
            req = urlrequest.Request(url, method="HEAD")
            with urlrequest.urlopen(req, timeout=6) as response:
                xfo = (response.headers.get("X-Frame-Options") or "").strip().upper()
                csp = (response.headers.get("Content-Security-Policy") or "").lower()

            if xfo in {"DENY", "SAMEORIGIN"}:
                return f"Blocage serveur: X-Frame-Options={xfo}."

            if "frame-ancestors" in csp:
                return "Blocage serveur: CSP frame-ancestors interdit l'embed."
        except Exception:
            return None

        return None

    def _build_react_surface() -> ft.Control:
        if EmbeddedWebView is None:
            return ft.Container(
                expand=True,
                padding=12,
                content=ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER_300),
                        ft.Text(
                            "WebView indisponible: package flet-webview manquant.",
                            size=14,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            "Installe-le puis relance l'app, ou utilise Ouvrir externe.",
                            size=12,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.Colors.BLUE_GREY_200,
                        ),
                    ],
                ),
            )

        reason = _embedding_block_reason(COTE_URL)
        if reason is not None:
            status.value = (
                f"Impossible d'embarquer {COTE_URL}: {reason} "
                "Ouvre le site en externe ou modifie les headers serveur."
            )
            return ft.Container(
                expand=True,
                padding=12,
                content=ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.BLOCK, color=ft.Colors.AMBER_300),
                        ft.Text(
                            "Le serveur bloque l'integration en iframe/webview.",
                            size=14,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            reason,
                            size=12,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.Colors.BLUE_GREY_200,
                        ),
                        ft.FilledButton(
                            "Ouvrir cote7.com",
                            icon=ft.Icons.OPEN_IN_NEW,
                            on_click=lambda e: open_url(e, COTE_URL),
                        ),
                    ],
                ),
            )

        try:
            return EmbeddedWebView(
                url=COTE_URL,
                expand=True,
            )
        except Exception:  # noqa: BLE001
            status.value = (
                "WebView non supportée sur cette plateforme. "
                "Utilise l'ouverture externe."
            )
            return ft.Container(
                expand=True,
                padding=12,
                content=ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.INFO_OUTLINE, color=ft.Colors.AMBER_300),
                        ft.Text(
                            "WebView non supportée ici (souvent en mode Web).",
                            size=14,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.FilledButton(
                            "Ouvrir cote7.com",
                            icon=ft.Icons.OPEN_IN_NEW,
                            on_click=lambda e: open_url(e, COTE_URL),
                        ),
                    ],
                ),
            )

    webview_container.content = _build_react_surface()

    return named_view(
        ft.Row(
            controls=[
                ft.Icon(ft.Icons.DATA_OBJECT, size=28),
                ft.Text("React", size=28, weight=ft.FontWeight.W_600),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        "Vue cote7.com embarquée dans Flet.",
        extra=ft.Column(
            width=340,
            controls=[
                status,
                ft.Container(height=10),
                webview_container,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
