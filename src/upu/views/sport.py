import webbrowser

import flet as ft

from upu.views.page_template import named_view


def build() -> ft.Control:
    def open_example_com(e):
        page = getattr(e.control, "page", None)
        platform = getattr(page, "platform", None)
        is_mobile = False
        if platform is not None:
            platform_is_mobile = getattr(platform, "is_mobile", None)
            if callable(platform_is_mobile):
                is_mobile = bool(platform_is_mobile())
            else:
                platform_name = getattr(platform, "name", str(platform)).lower()
                is_mobile = platform_name in {"android", "ios"}

        if is_mobile and page is not None and hasattr(page, "launch_url"):

            async def _open_mobile_url() -> None:
                try:
                    await page.launch_url("https://example.com")
                except Exception:
                    webbrowser.open("https://example.com")

            page.run_task(_open_mobile_url)
            return

        webbrowser.open("https://example.com")

    sport_container = ft.Container(
        width=320,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.DIRECTIONS_RUN),
                        ft.Text("Ready for next session"),
                    ]
                ),
                ft.FilledButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.OPEN_IN_NEW, size=16),
                            ft.Text("Visiter example.com"),
                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    on_click=open_example_com,
                ),
            ]
        ),
    )

    return named_view(
        ft.Row(
            controls=[
                ft.Icon(ft.Icons.DIRECTIONS_RUN, size=28),
                ft.Text("Sport", size=28, weight=ft.FontWeight.W_600),
            ],
            # vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        "Sport Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non "
        "urna sit amet augue tempor faucibus. Cras facilisis, purus ut "
        "ullamcorper tristique, libero lectus vehicula elit, vitae posuere "
        "quam erat at magna. Donec porta, turpis nec eleifend tincidunt, "
        "massa turpis gravida sapien, sed feugiat odio velit ut nisl of Sport.",
        sport_container,
    )
