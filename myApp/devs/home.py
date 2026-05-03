import flet as ft

from devs.page_content import named_view


def build() -> ft.Control:
    return named_view(
        "Home",
        "Home Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus "
        "lacinia, nisl at fermentum posuere, mauris sapien vulputate lorem, "
        "eu feugiat risus leo vitae arcu. Integer aliquet, sem id convallis "
        "blandit, justo erat tincidunt nibh, at efficitur mi velit in nisl of Home.",
    )
