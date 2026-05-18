import flet as ft


def user_number_locale(page: ft.Page) -> str:
    locale_config = page.locale_configuration
    locale_info = locale_config.current_locale if locale_config else None
    if not locale_info:
        return "en-US"
    if locale_info.language_code == "fr":
        return "fr-FR"
    return "en-US"


def on_locale_change(e: ft.Event[ft.Page]) -> None:
    locale_config = e.page.locale_configuration
    locale_info = locale_config.current_locale if locale_config else None
    if locale_info:
        print(locale_info.language_tag)


def attach_locale_logger(page: ft.Page) -> None:
    page.on_locale_change = on_locale_change
