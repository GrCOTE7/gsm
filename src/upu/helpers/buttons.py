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

_VALID_ALIGNS = {
    "start",
    "center",
    "end",
    "space_between",
    "space_around",
    "space_evenly",
}

_ALIGN_MAP = {
    "start": ft.MainAxisAlignment.START,
    "center": ft.MainAxisAlignment.CENTER,
    "end": ft.MainAxisAlignment.END,
    "space_between": ft.MainAxisAlignment.SPACE_BETWEEN,
    "space_around": ft.MainAxisAlignment.SPACE_AROUND,
    "space_evenly": ft.MainAxisAlignment.SPACE_EVENLY,
}


def _resolve_align(align: str | None) -> ft.MainAxisAlignment:
    """Normalise align en ft.MainAxisAlignment ; retombe sur START si invalide."""
    if align not in _VALID_ALIGNS:
        align = "start"
    return _ALIGN_MAP[align]


def _link_row(
    txt: str, *, color: str | None = None, spacing: int = 6, align: str | None = "start"
) -> ft.Row:
    """Contenu partagé (texte + icône) pour les liens externes."""
    return ft.Row(
        controls=[
            ft.Text(txt, color=color),
            ft.Icon(ft.Icons.OPEN_IN_NEW, size=16),
        ],
        spacing=spacing,
        alignment=_resolve_align(align),
    )


def extLink(txt="open_url()", url="https://example.com", tooltip=None, align="start"):
    """Lien texte simple, cliquable, sans fond de bouton."""
    return ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.CLICK,
        on_tap=lambda e: open_url(e, url),
        content=ft.Container(
            content=_link_row(txt, color=ft.Colors.CYAN_400, align=align),
            tooltip=tooltip,
            ink=True,
        ),
    )


def extLinkBtn(
    txt="open_url()", url="https://example.com", tooltip=None, align="start"
):
    """Variante en FilledButton du même lien."""
    return ft.Container(
        content=ft.Row(
            controls=[
                filled_button(
                    content=_link_row(txt, spacing=8),
                    tooltip=tooltip,
                    on_click=lambda e: open_url(e, url),
                ),
            ],
            alignment=_resolve_align(align),
        ),
    )


def extLinkOri(txt="open_url()", url="https://example.com"):
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
