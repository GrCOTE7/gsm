import flet as ft


def named_view(
    title: str | ft.Control, body: str, extra: ft.Control | None = None
) -> ft.Control:
    title_control = (
        ft.Text(title, size=28, weight=ft.FontWeight.W_600)
        if isinstance(title, str)
        else title
    )
    controls = [
        title_control,
        ft.Container(height=16),
        ft.Container(
            width=320,
            content=ft.Text(
                body,
                size=16,
                text_align=ft.TextAlign.JUSTIFY,
            ),
        ),
    ]

    if extra is not None:
        controls.extend([ft.Container(height=16), extra])

    return ft.Container(
        expand=True,
        padding=ft.Padding(top=24, right=20, bottom=20, left=20),
        content=ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=controls,
        ),
    )
