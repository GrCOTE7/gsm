import flet as ft

from .constants import theme
from . import gc7
from . import screen_utils


def status_line(current_time: str, page: ft.Page, sample_value: str) -> str:
    current_time = gc7.curr_time()
    theme_label = "sombre" if page.theme_mode == ft.ThemeMode.DARK else "clair"
    return f"{current_time} - {page.route} - Thème {theme_label} - {sample_value}"


def sport_title(txt: str) -> ft.Container:
    return ft.Container(
        padding=-10,
        content=ft.Stack(
            controls=[
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            txt,
                            ft.TextStyle(
                                size=70,
                                weight=ft.FontWeight.BOLD,
                                foreground=ft.Paint(
                                    color=theme["TITLE_STROKE"],
                                    stroke_width=5,
                                    stroke_join=ft.StrokeJoin.ROUND,
                                    style=ft.PaintingStyle.STROKE,
                                ),
                            ),
                        ),
                    ],
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            txt,
                            ft.TextStyle(
                                size=70,
                                weight=ft.FontWeight.BOLD,
                                color=theme["TITLE_FILL"],
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )


def build_main_column(
    page: ft.Page,
    app_name: str,
    sport_version: str,
    on_theme_change=None,
) -> tuple:
    colors = screen_utils.get_colors_theme(page)
    version_text = ft.Text("v_" + sport_version, color=colors["ink"])
    column = ft.Column(
        controls=[
            sport_title(app_name),
            version_text,
            gc7.toggleTheme(page, on_change=on_theme_change),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        tight=True,
    )
    return column, version_text


def zoom_help_text(page: ft.Page) -> ft.Text:
    return ft.Text(
        "Pincez avec 2 doigts pour zoomer, double-tapez pour reinitialiser",
        size=14,
        color=screen_utils.get_colors_theme(page)["ink"],
    )


def status_text(current_time: str, page: ft.Page, sample_value: str) -> ft.Text:
    return ft.Text(
        status_line(current_time, page, sample_value),
        size=14,
        color=screen_utils.get_colors_theme(page)["ink"],
    )
