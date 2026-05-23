import flet as ft
import gc7_tools.gc7 as gc7

from upu.config import DEFAULT_ROUTE, VERSION
from upu.services.i18n_service import I18nService


class SettingsController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.i18n = I18nService()

    def set_language(self, lang_code: str):
        self.i18n.set_language(lang_code)
        self.page.update()

    def toggle_theme(self):
        is_light = self.page.theme_mode == ft.ThemeMode.LIGHT
        self.page.theme_mode = ft.ThemeMode.DARK if is_light else ft.ThemeMode.LIGHT
        self.page.update()

    def on_lifecycle_change(self, e, navigation_controller, pending_home):
        state = str(getattr(e, "state", "")).lower()
        if state == "resume" and pending_home:
            navigation_controller.render_route(DEFAULT_ROUTE)

    def invite(self):
        print(VERSION, "-", gc7.curr_time(), self.page.route, ">")

    def is_mobile_platform(self):
        platform = getattr(self.page, "platform", None)
        if platform is None:
            return False

        is_mobile = getattr(platform, "is_mobile", None)
        if callable(is_mobile):
            return bool(is_mobile())

        platform_name = getattr(platform, "name", str(platform)).lower()
        return platform_name in {"android", "ios"}
