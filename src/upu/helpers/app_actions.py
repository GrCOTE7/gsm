"""Actions transverses (URL, fermeture app) selon la plateforme."""

from __future__ import annotations

import os
import webbrowser

import flet as ft

from upu.services.android_bridge import launch_url_intent
from upu.helpers.snackbar import show_snackbar


def _as_page(target: object) -> ft.Page | None:
    if isinstance(target, ft.Page):
        return target

    control = getattr(target, "control", None)
    return getattr(control, "page", None)


def _get_platform_name(page: ft.Page | None) -> str:
    platform = getattr(page, "platform", None)
    if platform is None:
        return ""
    return str(getattr(platform, "name", str(platform))).lower()


def _is_mobile(page: ft.Page | None) -> bool:
    platform = getattr(page, "platform", None)
    if platform is not None:
        platform_is_mobile = getattr(platform, "is_mobile", None)
        if callable(platform_is_mobile):
            return bool(platform_is_mobile())
    return _get_platform_name(page) in {"android", "ios"}


def _is_web(page: ft.Page | None) -> bool:
    if page is None:
        return False
    if bool(getattr(page, "web", False)):
        return True
    return _get_platform_name(page) == "web"


def open_url(e: object, url: str) -> None:
    """Ouvre *url* en tenant compte de la plateforme (mobile vs desktop)."""
    page = _as_page(e)
    if _get_platform_name(page) == "android" and launch_url_intent(url):
        return

    if _is_mobile(page) and page is not None and hasattr(page, "launch_url"):

        async def _open_mobile_url() -> None:
            try:
                await page.launch_url(url)
            except Exception:
                webbrowser.open(url)

        page.run_task(_open_mobile_url)
        return

    if page is not None and hasattr(page, "launch_url"):

        async def _open_desktop_url() -> None:
            try:
                await page.launch_url(url)
            except Exception:
                webbrowser.open(url)

        page.run_task(_open_desktop_url)
        return

    webbrowser.open(url)


def close_page(page: ft.Page | None, code: int = 0) -> None:
    """Ferme l'application si possible selon le runtime.

    Android: fermeture process; app desktop/mobile: fermeture fenetre;
    Web: impossible de fermer l'onglet de facon fiable, on affiche un message.
    """
    if _get_platform_name(page) == "android":
        os._exit(code)

    if page is None:
        return

    if _is_web(page):
        show_snackbar(
            page,
            "T'es en mode Web ! La fermeture automatique est donc bloquée par le navigateur...\n→ Ferme l'onglet comme d'hab ! La croix le + en haut à droite !",
            color=ft.Colors.RED_400,
            bgcolor=ft.Colors.TRANSPARENT,
            duration=7000,
            floating=True,
            show_close_icon=True,
        )
        return

    if not hasattr(page, "window"):
        return

    async def _close_window() -> None:
        await page.window.close()

    page.run_task(_close_window)


def close_app(e: object, code: int = 0) -> None:
    close_page(_as_page(e), code)
