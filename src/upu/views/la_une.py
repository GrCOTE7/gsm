import flet as ft

import gc7_tools.gc7 as gc7
import gc7_tools.home_ui as home_ui
import gc7_tools.locale_utils as locale_utils
import gc7_tools.screen_utils as screen_utils

APP_NAME = "Sport 2026"
SPORT_VERSION = "0.0.1"


def une(page: ft.Page):
    screen_utils.gc7_rules(page, left=1912)  # 1520 ou 1912

    # page.theme_mode = ft.ThemeMode.DARK  # Comment to light
    # page.bgcolor = screen_utils.get_colors_theme(page)["bg"]

    currentTime = gc7.curr_time()
    sample_value = gc7.nf(1234.57)

    page.title = f"{currentTime} - {APP_NAME} v_{SPORT_VERSION}"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    help_text = home_ui.zoom_help_text(page)
    stat_text = home_ui.status_text(currentTime, page, sample_value)

    theme_texts = []
    on_theme_change = screen_utils.make_theme_change_handler(page, lambda: theme_texts)

    original_on_theme_change = on_theme_change

    def on_theme_change():
        original_on_theme_change()
        stat_text.value = home_ui.status_line(currentTime, page, sample_value)

    content_column, version_text = home_ui.build_main_column(
        page, APP_NAME, SPORT_VERSION, on_theme_change=on_theme_change
    )
    theme_texts.extend([version_text, help_text, stat_text])

    zoomable_view = screen_utils.make_zoomable_view(page, content_column)

    # page.add(zoomable_view)
    # page.add(help_text)
    # page.add(stat_text)

    content = ft.Column(
        controls=[
            zoomable_view,
            help_text,
            stat_text,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    locale_utils.attach_locale_logger(page)

    print(currentTime, "-", page.route, "-", page.theme_mode, ">")

    return content


# ft.run(main)
