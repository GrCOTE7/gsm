import asyncio
import time
from typing import cast

import flet as ft

from upu.config import CACHE_DELAY, get_latest_release_info
from upu.helpers.app_actions import close_app, open_url
from upu.helpers.buttons import filled_button
from upu.helpers.snackbar import show_snackbar
from upu.views.partials import build_release_update_card
from upu.views.page_template import named_view


def ext_link(e, type):
    if type == 1:
        open_url(e, "https://example.com/1")
    open_url(e, "https://example.com/1")


# ------------------------------------------------------------
#  CACHE
# ------------------------------------------------------------


class ReleaseCache:
    def __init__(self):
        self.url = ""
        self.timestamp = 0.0

    @property
    def is_valid(self) -> bool:
        return bool(self.url) and (time.monotonic() - self.timestamp) < CACHE_DELAY

    @property
    def age(self) -> int:
        return int(time.monotonic() - self.timestamp)

    @property
    def remaining(self) -> int:
        return max(0, int(CACHE_DELAY - (time.monotonic() - self.timestamp)))

    def set(self, url: str):
        self.url = url
        self.timestamp = time.monotonic()


cache = ReleaseCache()


# ------------------------------------------------------------
#  GITHUB FETCH
# ------------------------------------------------------------


def fetch_latest_apk_url() -> str:
    print("[fetch_latest_apk_url] start")
    release_info = get_latest_release_info(timeout_seconds=5, allow_remote=True)

    download_url = str(release_info.get("download_url") or "").strip()
    html_url = str(release_info.get("html_url") or "").strip()
    url = download_url or html_url
    print("[fetch_latest_apk_url] resolved:", url or "(vide)")
    return url or "(vide)"


# ------------------------------------------------------------
#  ASYNC CHECK
# ------------------------------------------------------------


async def check_latest(page: ft.Page, result_text: ft.Text, button: ft.Control):
    print("[check_latest] start")
    source = "ERROR"

    try:
        # Cache valide → direct
        if cache.is_valid:
            source = "CACHE"
            result_text.value = (
                f"Résultat:\n{cache.url} (CACHE {cache.age}s / {CACHE_DELAY}s)"
            )
            result_text.update()
        else:
            # Chargement
            result_text.value = "Résultat:\nChargement..."
            result_text.update()

            url = await asyncio.to_thread(fetch_latest_apk_url)
            cache.set(url)

            source = "GH"
            result_text.value = f"Résultat:\n{url} (GH)"
            result_text.update()

    except Exception as e:
        print("[check_latest] ERROR:", repr(e))

        if cache.url:
            source = "STALE"
            result_text.value = f"Résultat:\n{cache.url} (CACHE stale)"
        else:
            source = "ERROR"
            result_text.value = "Résultat:\nIndisponible."

        result_text.update()

    # Mise à jour du bouton
    button.disabled = not cache.is_valid
    button.update()

    # Snackbar systématique
    messages = {
        "GH": f"browser_download_url depuis GitHub — cache valide {cache.remaining}s",
        "CACHE": f"browser_download_url depuis CACHE — reste {cache.remaining}s",
        "STALE": "Erreur réseau — utilisation du cache expiré",
        "ERROR": "Erreur — aucune donnée disponible",
    }

    show_snackbar(page, messages[source], 5000)
    print("[check_latest] end, source =", source)


# ------------------------------------------------------------
#  UI BUILD
# ------------------------------------------------------------


def build() -> ft.Control:
    result_text = ft.Text("Résultat: Pas encore vérifié.", size=12)

    def on_run(e: ft.ControlEvent):
        page = cast(ft.Page, e.page)
        print("[on_run] clicked")
        page.run_task(check_latest, page, result_text, latest_btn)

    run_btn = filled_button(
        content=ft.Row(
            controls=[ft.Icon(ft.Icons.PLAY_ARROW, size=16), ft.Text("Run")],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        on_click=on_run,
    )
    latest_btn = filled_button(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.DOWNLOAD_FOR_OFFLINE_SHARP, size=18),
                ft.Text("Dernière version APK"),
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        disabled=True,
        on_click=lambda e: open_url(e, cache.url),
    )
    return named_view(
        ft.Row(
            controls=[
                ft.Icon(ft.Icons.FLAG, size=28),
                ft.Text("Tests2", size=28, weight=ft.FontWeight.W_600),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        "Tests de récupération de latest GH.",
        extra_top_gap=0,
        extra=ft.Column(
            [
                ft.Container(
                    padding=ft.Padding.only(bottom=20),
                    content=ft.Row(
                        controls=[
                            filled_button(
                                content="Tests",
                                on_click=lambda e: e.page.run_task(
                                    e.page.push_route, "/tests"
                                ),
                            ),
                            filled_button(
                                content="Archives",
                                on_click=lambda e: e.page.run_task(
                                    e.page.push_route, "/archives"
                                ),
                            ),
                            filled_button(
                                content="Fermer l'App",
                                on_click=lambda e: close_app(e),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ),
                result_text,
                ft.Row(
                    controls=[
                        run_btn,
                        latest_btn,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                build_release_update_card(),
            ]
        ),
    )
