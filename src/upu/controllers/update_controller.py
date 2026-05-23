import asyncio
import threading
from pathlib import Path
from typing import cast

import flet as ft
from upu.services.release_service import get_update_log_path, open_release_url
from upu.config import is_update_available, get_latest_release_info
from upu.helpers.buttons import filled_button
from upu.helpers.snackbar import show_snackbar
import subprocess


class UpdateController:
    def __init__(self, page):
        self.page = page
        self._update_dialog = None
        self._desktop_update_dialog = None

    async def maybe_prompt_for_update(self, version):
        self.version = version
        update_available = await asyncio.to_thread(is_update_available, version)
        if not update_available:
            return

        latest_release = await asyncio.to_thread(get_latest_release_info)
        # Android/iOS peut encore etre en phase de rendu au tout premier tick.
        if self._is_mobile_platform():
            await asyncio.sleep(0.77)
        self.show_update_dialog(latest_release)

    def show_update_dialog(self, latest_release: dict[str, str | bool]) -> None:
        latest_version = str(latest_release.get("version") or self.version)
        release_url = str(
            latest_release.get("download_url") or latest_release.get("html_url") or ""
        )

        actions = cast(
            list[ft.Control],
            [
                ft.TextButton(
                    content=ft.Text("Plus tard"),
                    on_click=self.close_update_dialog,
                ),
                filled_button(
                    content=ft.Text("Mettre a jour"),
                    on_click=lambda e: self.install_update(release_url),
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
        self._open_dialog(dialog)
        self.page.update()

    def _open_dialog(self, dialog: ft.AlertDialog) -> None:
        # page.open() est la voie recommandee par Flet et fonctionne mieux sur mobile.
        page_open = getattr(self.page, "open", None)
        if callable(page_open):
            page_open(dialog)
            return

        overlay = getattr(self.page, "overlay", None)
        if overlay is None:
            return
        if dialog not in overlay:
            overlay.append(dialog)
        dialog.open = True

    def _is_mobile_platform(self) -> bool:
        platform = getattr(self.page, "platform", None)
        if platform is None:
            return False

        platform_is_mobile = getattr(platform, "is_mobile", None)
        if callable(platform_is_mobile):
            return bool(platform_is_mobile())

        return str(getattr(platform, "name", str(platform))).lower() in {
            "android",
            "ios",
        }

    def install_update(self, release_url: str) -> None:
        self.close_update_dialog()
        show_snackbar(self.page, "Tentative d'ouverture de la mise a jour...", 7700)
        opened = open_release_url(self.page, release_url, force=True)
        if not opened:
            show_snackbar(
                self.page, "Impossible d'ouvrir le lien de mise a jour.", 7700
            )
            return
        show_snackbar(
            self.page,
            f"Si rien ne s'ouvre, consultez le log: {get_update_log_path()}",
            7700,
        )

    def close_update_dialog(self, e=None) -> None:
        if self._update_dialog is None:
            return
        self._update_dialog.open = False
        self.page.update()

    def run_git_action(self, action_label: str, args: list[str]) -> None:
        show_snackbar(self.page, f"Execution git {action_label}...", 7700)
        self.page.run_task(self._run_git_action_async, action_label, args)

    async def _run_git_action_async(self, action_label: str, args: list[str]) -> None:
        result = await asyncio.to_thread(self._exec_git, args)
        code, stdout, stderr = result

        if action_label == "pull" and code == 0:
            status_code, status_stdout, _ = await asyncio.to_thread(
                self._exec_git, ["status", "-sb"]
            )
            if status_code == 0 and "ahead" in status_stdout:
                show_snackbar(
                    self.page,
                    "git pull OK (ff-only). Votre branche locale contient deja des commits en avance sur origin.",
                    7700,
                )
                return

        if code == 0:
            first_line = (stdout or "OK").strip().splitlines()[0]
            show_snackbar(self.page, f"git {action_label} OK: {first_line}", 4000)
            return
        message = (stderr or stdout or "Erreur inconnue").strip().splitlines()[0]
        show_snackbar(self.page, f"git {action_label} KO: {message}", 7700)

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

    def _project_root(self) -> Path:
        return Path(__file__).resolve().parents[3]
