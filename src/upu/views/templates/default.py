import flet as ft


def named_view(
    title: str | ft.Control,
    body: str,
    extra: ft.Control | None = None,
    bottom: ft.Control | None = None,
    extra_top_gap: int = 16,
    body_text_align: ft.TextAlign = ft.TextAlign.JUSTIFY,
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
            width=3640,
            content=ft.Text(
                body,
                size=16,
                text_align=body_text_align,
            ),
        ),
    ]

    if extra is not None:
        controls.extend([ft.Container(height=extra_top_gap), extra])

    content_column = ft.Column(
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=controls,
        scroll=ft.Scrollbar(True),
    )

    page_controls: list[ft.Control] = [
        ft.Container(expand=True, content=content_column),
    ]
    if bottom is not None:
        page_controls.append(bottom)

    return ft.SafeArea(
        expand=True,
        minimum_padding=ft.Padding(top=20, right=20, bottom=10, left=20),
        content=ft.Column(
            expand=True,
            controls=page_controls,
        ),
    )
