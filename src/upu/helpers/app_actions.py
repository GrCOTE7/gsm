"""Actions transverses (URL, fermeture app) selon la plateforme."""

from __future__ import annotations

import os
import webbrowser

import flet as ft

from upu.services.android_bridge import launch_url_intent


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
    """Ferme l'application: Android -> os._exit, sinon fermeture fenetre."""
    if _get_platform_name(page) == "android":
        os._exit(code)

    if page is None or not hasattr(page, "window"):
        return

    async def _close_window() -> None:
        await page.window.close()

    page.run_task(_close_window)


def close_app(e: object, code: int = 0) -> None:
    close_page(_as_page(e), code)
