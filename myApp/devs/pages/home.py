import flet as ft

from devs.pages.page_template import named_view


def build() -> ft.Control:
    return named_view(
        ft.Row(
            controls=[
                ft.Icon(ft.Icons.HOME),
                ft.Text("Home", size=28, weight=ft.FontWeight.W_600),
            ],
            # vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        "Home Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus "
        "lacinia, nisl at fermentum posuere, mauris sapien vulputate lorem, "
        "eu feugiat risus leo vitae arcu. Integer aliquet, sem id convallis "
        "blandit, justo erat tincidunt nibh, at efficitur mi velit in nisl of Home.",
    )
