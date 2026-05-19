import asyncio
import subprocess
import webbrowser
from pathlib import Path
from typing import cast

import logging as lg

import flet as ft

import gc7_tools.gc7 as gc7
import gc7_tools.screen_utils as screen_utils

from upu.config import (
    APP_NAME,
    DEFAULT_ROUTE,
    VERSION,
    WINDOW_LEFT,
    get_latest_release_info,
    is_update_available,
)
from upu.routes.registry import get_view_builder, has_route
from upu.services.release_service import get_update_log_path, open_release_url
from upu.ui.navigation import AppBar, Drawer


class AppController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.app_name = APP_NAME
        self.version = VERSION
        self._update_check_started = False
        self._update_dialog: ft.AlertDialog | None = None
        self._desktop_update_dialog: ft.AlertDialog | None = None
        self._setup()

    def _setup(self) -> None:
        screen_utils.gc7_rules(self.page, left=WINDOW_LEFT)
        self.page.title = f"{self.app_name} - v{self.version}"
        self.page.on_route_change = self._route_change
        self.page.on_view_pop = self._view_pop

        self.page.run_task(self.page.push_route, DEFAULT_ROUTE)

        self._invite()

    def _invite(self) -> None:
        print(self.version, "-", gc7.curr_time(), self.page.route, ">")

    def _route_change(self, e: ft.RouteChangeEvent) -> None:
        print(self.version, "-", gc7.curr_time(), e.route, ">")
        lg.basicConfig(level=lg.INFO)
        lg.info(f" {self.version} - {gc7.curr_time()} {e.route} >")
        self._render_route(e.route or DEFAULT_ROUTE)

    def _build_view(self, route: str) -> ft.View:
        builder = get_view_builder(route)
        return ft.View(
            route=route,
            appbar=AppBar(self.page, self.app_name),
            drawer=Drawer(self.page),
            padding=0,
            spacing=0,
            controls=[builder()],
        )
        # return ft.View(
        #     route=route,
        #     appbar=AppBar(self.page, self.app_name),
        #     drawer=Drawer(self.page),
        #     padding=0,
        #     spacing=0,
        #     controls=[
        #         ft.Container(
        #             bgcolor="#777777",
        #             border_radius=ft.border_radius.all(25),
        #             expand=True,
        #             content=builder(),
        #         )
        #     ],
        # )

    def _render_route(self, raw_route: str) -> None:
        self.page.views.clear()
        route = raw_route.split("?")[0]
        route = route if has_route(route) else DEFAULT_ROUTE
        self.page.views.append(self._build_view(route))
        self.page.update()
        if not self._update_check_started:
            self._update_check_started = True
            self.page.run_task(self._maybe_prompt_for_update)

    async def _maybe_prompt_for_update(self) -> None:
        update_available = await asyncio.to_thread(is_update_available, self.version)
        if not update_available:
            return

        latest_release = await asyncio.to_thread(get_latest_release_info)
        self._show_update_dialog(latest_release)

    def _show_update_dialog(self, latest_release: dict[str, str | bool]) -> None:
        latest_version = str(latest_release.get("version") or self.version)
        release_url = str(
            latest_release.get("download_url") or latest_release.get("html_url") or ""
        )

        actions = cast(
            list[ft.Control],
            [
                ft.TextButton(
                    content=ft.Text("Plus tard"),
                    on_click=self._close_update_dialog,
                ),
                ft.FilledButton(
                    content=ft.Text("Mettre a jour"),
                    on_click=lambda e: self._install_update(release_url),
                ),
            ],
        )

        dialog = ft.AlertDialog()
        dialog.modal = True
        dialog.title = ft.Text("Nouvelle version disponible")
        dialog.content = ft.Column(
            tight=True,
            spacing=8,
            controls=[
                ft.Text(f"Version actuelle: {self.version}"),
                ft.Text(f"Version disponible: {latest_version}"),
                ft.Text(
                    "Une mise a jour est disponible. Voulez-vous telecharger la nouvelle APK maintenant ?"
                ),
            ],
        )
        dialog.actions = actions
        dialog.actions_alignment = ft.MainAxisAlignment.END

        self._update_dialog = dialog
        if dialog not in self.page.overlay:
            self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def _close_update_dialog(self, e=None) -> None:
        if self._update_dialog is None:
            return
        self._update_dialog.open = False
        self.page.update()

    def _show_snackbar(self, message: str, duration: int = 2500) -> None:
        self.page.show_dialog(ft.SnackBar(content=ft.Text(message), duration=duration))

    def _is_mobile_platform(self) -> bool:
        platform = getattr(self.page, "platform", None)
        if platform is None:
            return False

        is_mobile = getattr(platform, "is_mobile", None)
        if callable(is_mobile):
            return bool(is_mobile())

        platform_name = getattr(platform, "name", str(platform)).lower()
        return platform_name in {"android", "ios"}

    def _close_desktop_update_dialog(self, e=None) -> None:
        if self._desktop_update_dialog is None:
            return
        self._desktop_update_dialog.open = False
        self.page.update()

    def _show_desktop_update_dialog(self, release_url: str) -> None:
        dialog = ft.AlertDialog()
        dialog.modal = True
        dialog.title = ft.Text("Mise a jour (desktop)")
        dialog.content = ft.Column(
            tight=True,
            spacing=8,
            controls=[
                ft.Text("En local/dev, vous pouvez synchroniser le depot Git."),
                ft.Text("Choisissez une action:"),
            ],
        )
        dialog.actions = cast(
            list[ft.Control],
            [
                ft.TextButton(
                    content=ft.Text("Annuler"),
                    on_click=self._close_desktop_update_dialog,
                ),
                ft.OutlinedButton(
                    content=ft.Text("Git fetch"),
                    on_click=lambda e: self._run_git_action(
                        "fetch", ["fetch", "--all", "--prune"]
                    ),
                ),
                ft.FilledButton(
                    content=ft.Text("Git pull"),
                    on_click=lambda e: self._run_git_action(
                        "pull", ["pull", "--ff-only"]
                    ),
                ),
                ft.TextButton(
                    content=ft.Text("Voir la release"),
                    on_click=lambda e: self._open_release_from_desktop_dialog(
                        release_url
                    ),
                ),
            ],
        )
        dialog.actions_alignment = ft.MainAxisAlignment.END

        self._desktop_update_dialog = dialog
        if dialog not in self.page.overlay:
            self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def _open_release_from_desktop_dialog(self, release_url: str) -> None:
        self._close_desktop_update_dialog()
        opened = open_release_url(self.page, release_url, force=True)
        if not opened:
            self._show_snackbar("Impossible d'ouvrir le lien de mise a jour.", 3000)
            return
        self._show_snackbar(
            f"Si rien ne s'ouvre, consultez le log: {get_update_log_path()}",
            3500,
        )

    def _project_root(self) -> Path:
        return Path(__file__).resolve().parents[3]

    def _run_git_action(self, action_label: str, args: list[str]) -> None:
        self._close_desktop_update_dialog()
        self._show_snackbar(f"Execution git {action_label}...", 1800)
        self.page.run_task(self._run_git_action_async, action_label, args)

    async def _run_git_action_async(self, action_label: str, args: list[str]) -> None:
        result = await asyncio.to_thread(self._exec_git, args)
        code, stdout, stderr = result

        if action_label == "pull" and code == 0:
            status_code, status_stdout, _ = await asyncio.to_thread(
                self._exec_git, ["status", "-sb"]
            )
            if status_code == 0 and "ahead" in status_stdout:
                self._show_snackbar(
                    "git pull OK (ff-only). Votre branche locale contient deja des commits en avance sur origin.",
                    5200,
                )
                return

        if code == 0:
            first_line = (stdout or "OK").strip().splitlines()[0]
            self._show_snackbar(f"git {action_label} OK: {first_line}", 4000)
            return
        message = (stderr or stdout or "Erreur inconnue").strip().splitlines()[0]
        self._show_snackbar(f"git {action_label} KO: {message}", 4500)

    def _exec_git(self, args: list[str]) -> tuple[int, str, str]:
        try:
            completed = subprocess.run(
                ["git", *args],
                cwd=self._project_root(),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            return completed.returncode, completed.stdout or "", completed.stderr or ""
        except OSError as exc:
            return 1, "", str(exc)

    def _close_app_best_effort(self) -> bool:
        # Sur mobile, plusieurs versions de Flet exposent des APIs differentes.
        # On tente la fermeture via window.close(), puis via des variantes connues.
        try:
            window = getattr(self.page, "window", None)
            close_fn = getattr(window, "close", None) if window is not None else None
            if callable(close_fn):
                close_fn()
                return True
        except Exception:
            pass

        for attr_name in ("window_close", "close"):
            try:
                fn = getattr(self.page, attr_name, None)
                if callable(fn):
                    fn()
                    return True
            except Exception:
                continue

        return False

    async def _close_app_after_install_delay(self, delay_seconds: float = 1.2) -> None:
        import sys

        await asyncio.sleep(delay_seconds)
        closed = self._close_app_best_effort()
        if not closed:
            if self._is_mobile_platform():
                sys.exit(0)

    def _install_update(self, release_url: str) -> None:

        print(">>> CLICK REÇU DANS _install_update()")

        self._close_update_dialog()

        self._show_snackbar("Tentative d'ouverture de la mise a jour...", 2000)
        opened = open_release_url(self.page, release_url, force=True)
        if not opened:
            self._show_snackbar("Impossible d'ouvrir le lien de mise a jour.", 3000)
            return

        if self._is_mobile_platform():
            # Revenir à l'accueil AVANT de fermer : si Android reprend l'app
            # depuis l'arrière-plan, elle sera déjà sur la bonne page.
            self._render_route(DEFAULT_ROUTE)
            self.page.run_task(self._close_app_after_install_delay)
            return

        self._show_snackbar(
            f"Si rien ne s'ouvre, consultez le log: {get_update_log_path()}",
            7700,
        )

    async def _view_pop(self, e: ft.ViewPopEvent) -> None:
        if e.view is not None and e.view in self.page.views:
            self.page.views.remove(e.view)
        target_route = self.page.views[-1].route if self.page.views else DEFAULT_ROUTE
        await self.page.push_route(target_route)

    def go_to(self, route: str) -> None:
        if (self.page.route or DEFAULT_ROUTE) == route:
            self._render_route(route)
            return
        self.page.run_task(self._push_route_async, route)

    async def _push_route_async(self, route: str) -> None:
        await self.page.push_route(route)


def create_app(page: ft.Page) -> None:
    AppController(page)
