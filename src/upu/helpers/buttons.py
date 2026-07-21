from __future__ import annotations
import flet as ft
from upu.helpers.app_actions import open_url

from typing import Any


def filled_button(
    *args: Any,
    radius: int = 7,
    style: ft.ButtonStyle | None = None,
    **kwargs: Any,
) -> ft.FilledButton:
    """Create a FilledButton with a default rounded shape.

    The default corner radius is 7, while still allowing callers to override
    other style attributes through the optional style argument.
    """
    final_style = style or ft.ButtonStyle()
    if getattr(final_style, "shape", None) is None:
        final_style.shape = ft.RoundedRectangleBorder(radius=radius)
    if getattr(final_style, "mouse_cursor", None) is None:
        final_style.mouse_cursor = ft.MouseCursor.CLICK

    return ft.FilledButton(*args, style=final_style, **kwargs)


def extLink(txt='open_url()', url='https://example.com'):
    return ft.Container(
        padding=ft.Padding.only(bottom=10),
        content=ft.Row(
            controls=[
                filled_button(
                    content=ft.Container(
                        # padding=ft.Padding.symmetric(horizontal=10, vertical=2),
                        content=ft.Row(
                            controls=[
                                ft.Text(txt),
                                ft.Icon(icon=ft.Icons.OPEN_IN_NEW, size=16),
                            ],
                            spacing=8,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ),
                    on_click=lambda e: open_url(e, url),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

