import asyncio
import threading
from pathlib import Path
from typing import cast

import flet as ft
import gc7_tools.screen_utils as screen_utils

from upu.config import APP_NAME, VERSION, WINDOW_LEFT, DEFAULT_ROUTE
from upu.controllers.settings_controller import SettingsController
from upu.controllers.update_controller import UpdateController
from upu.controllers.navigation_controller import NavigationController


class AppController:
    def __init__(self, page: ft.Page):
        self.page = page
        self._pending_home = False
        self.settings_controller = SettingsController(page)
        self.update_controller = UpdateController(page)
        self.navigation_controller = NavigationController(page)
        self._setup()

    def _setup(self) -> None:
        screen_utils.gc7_rules(self.page, left=WINDOW_LEFT)
        self.page.title = f"{APP_NAME} - v{VERSION}"
        self.page.on_app_lifecycle_state_change = (
            lambda e: self.settings_controller.on_lifecycle_change(
                e, self.navigation_controller, self._pending_home
            )
        )
        self.page.on_route_change = self.navigation_controller.route_change
        self.page.on_view_pop = self.navigation_controller.view_pop
        self.settings_controller.invite()
        self.navigation_controller.render_route(DEFAULT_ROUTE)
        self.page.run_task(self.update_controller.maybe_prompt_for_update, VERSION)


def create_app(page: ft.Page) -> None:
    AppController(page)
