import flet as ft

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
