import flet as ft


def named_view(title: str, body: str) -> ft.Control:
    return ft.Container(
        expand=True,
        padding=ft.Padding(top=24, right=20, bottom=20, left=20),
        content=ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(title, size=28, weight=ft.FontWeight.W_600),
                ft.Container(height=16),
                ft.Container(
                    width=320,
                    content=ft.Text(
                        body,
                        size=16,
                        text_align=ft.TextAlign.JUSTIFY,
                    ),
                ),
            ],
        ),
    )
