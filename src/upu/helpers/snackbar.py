from __future__ import annotations

import flet as ft


def show_snackbar(
    page: ft.Page,
    message: str,
    duration: int = 3000,
    *,
    floating: bool = True,
    show_close_icon: bool = True,
) -> None:
    if not str(message).strip():
        return

    previous_snackbar = getattr(page, "_upu_last_snackbar", None)
    if previous_snackbar is not None:
        page_close = getattr(page, "close", None)
        if callable(page_close):
            try:
                page_close(previous_snackbar)
            except Exception:
                pass

        try:
            previous_snackbar.open = False
        except Exception:
            pass

    snackbar = ft.SnackBar(
        content=ft.Text(message),
        duration=duration,
        behavior=(ft.SnackBarBehavior.FLOATING if floating else None),
        show_close_icon=show_close_icon,
    )

    page_open = getattr(page, "open", None)
    if callable(page_open):
        try:
            page_open(snackbar)
            setattr(page, "_upu_last_snackbar", snackbar)
            page.update()
            return
        except Exception:
            pass

    overlay = getattr(page, "overlay", None)
    if overlay is not None:
        if previous_snackbar in overlay:
            overlay.remove(previous_snackbar)
        if snackbar not in overlay:
            overlay.append(snackbar)
        snackbar.open = True
        setattr(page, "_upu_last_snackbar", snackbar)
        page.update()
        return

    setattr(page, "snack_bar", snackbar)
    setattr(page, "_upu_last_snackbar", snackbar)
    page_snackbar = getattr(page, "snack_bar", None)
    if page_snackbar is not None:
        page_snackbar.open = True
    page.update()
