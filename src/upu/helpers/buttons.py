from __future__ import annotations

from typing import Any

import flet as ft


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

    return ft.FilledButton(*args, style=final_style, **kwargs)
