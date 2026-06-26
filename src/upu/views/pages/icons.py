import flet as ft

from upu.views.templates.default import named_view


def build() -> ft.Control:
    icons_list = [
        "APPS",
        "HOME",
        "DIRECTIONS_RUN",
        "SETTINGS",
        "ADD",
        "DELETE",
        "EDIT",
        "SEARCH",
        "FAVORITE",
        "STAR",
        "INFO",
        "WARNING",
        "ERROR",
        "CHECK",
        "CLOSE",
        "MENU",
        "CLOSE",
        "ARROW_UPWARD",
        "ARROW_DOWNWARD",
        "ARROW_BACK",
        "ARROW_FORWARD",
        "REFRESH",
        "SAVE",
        "PRINT",
        "SHARE",
        "DOWNLOAD",
        "UPLOAD",
    ]

    def col(content, w):
        return ft.Container(
            width=w,
            content=ft.Row(
                [content],
                # alignment=ft.MainAxisAlignment.CENTER,
            ),
        )

    sport_container = ft.Container(
        width=320,
        height=302,
        padding=10,
        border_radius=7,
        content=ft.Column(
            controls=[
                ft.Row(
                    [
                        col(
                            ft.Text(
                                " O*",
                                size=16,
                                tooltip=ft.Tooltip(message="OUTLINED"),
                                weight=ft.FontWeight.BOLD,
                            ),
                            40,
                        ),
                        col(
                            ft.Text(
                                " F*",
                                size=16,
                                tooltip=ft.Tooltip(message="FILLED"),
                                weight=ft.FontWeight.BOLD,
                            ),
                            w=40,
                        ),
                        col(
                            ft.Text(
                                "Nom*",
                                tooltip=ft.Tooltip(message="Nom de l'icône"),
                                size=16,
                                weight=ft.FontWeight.BOLD,
                            ),
                            120,
                        ),
                    ]
                ),
                *[
                    ft.Row(
                        [
                            col(
                                ft.Icon(getattr(ft.Icons, f"{icon}_OUTLINED"), size=28),
                                40,
                            ),
                            col(ft.Icon(getattr(ft.Icons, f"{icon}"), size=28), 40),
                            col(ft.Text(icon, size=18), 120),
                        ]
                    )
                    for icon in icons_list
                ],
            ],
            scroll=ft.ScrollMode.AUTO,
            height=300,
        ),
    )

    return named_view(
        ft.Row(
            controls=[
                ft.Icon(icon=ft.Icons.TUNE, size=28),
                ft.Text("Icônes", size=28, weight=ft.FontWeight.BOLD),
            ],
            # vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        "Icônes Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non "
        "urna sit amet augue tempor faucibus. Cras facilisis, purus ut "
        "ullamcorper tristique, libero lectus vehicula elit, vitae posuere "
        "quam erat at magna. Donec porta, turpis nec eleifend tincidunt, "
        "massa turpis gravida sapien, sed feugiat odio velit ut nisl of Icônes.",
        sport_container,
    )
