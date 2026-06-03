import flet as ft

from upu.views.page_template import named_view

from upu.guests.mlm_913 import tests_views


def ready():
    return ft.Text("→ Ready for quick test21!", size=14, weight=ft.FontWeight.W_400)


def build() -> ft.Control:

    return named_view(
        ft.Row(
            controls=[
                ft.Icon(ft.Icons.SCIENCE, size=28),
                ft.Text("Tests", size=28, weight=ft.FontWeight.W_600),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        "Page pour tests rapides.",
        extra_top_gap=0,
        extra=tests_views(),
    )


def main(page: ft.Page):
    page.add(
        ft.Row(
            controls=[
                ft.Icon(ft.Icons.SCIENCE, size=28),
                ft.Text("Tests", size=28, weight=ft.FontWeight.W_600),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        # tests_views(), # 
    )
