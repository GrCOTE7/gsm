import flet as ft

from upu.views.templates.default import named_view

# UPU est l'ancienne application, conservée pour mémoire : elle ne propose
# volontairement aucune mise à jour (pas de build_release_update_card ici).


def build() -> ft.Control:
    return named_view(
        ft.Row(
            controls=[
                ft.Icon(ft.Icons.HOME, size=32),
                ft.Text("GSM Project", size=28, weight=ft.FontWeight.W_600),
            ],
            # vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        "→ http://GitHub.com/GrCOTE7/GSM"
        "\n\n"
        "Home Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus "
        "lacinia, nisl at fermentum posuere, mauris sapien vulputate lorem, "
        "eu feugiat risus leo vitae arcu. Integer aliquet, sem id convallis "
        "blandit, justo erat tincidunt nibh, at efficitur mi velit in nisl of Home 1.0.10+.",
    )
