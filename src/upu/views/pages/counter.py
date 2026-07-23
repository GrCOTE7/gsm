import flet as ft

from gc7_tools.helpers import sepa_major, sepa_outlined


def imperative_counter() -> ft.Control:
    count = ft.Text("0")

    def increment(_e: ft.ControlEvent) -> None:
        count.value = str(int(count.value) + 1)

# * [ ] ici transitional btn

    return ft.Container(
        padding=20,
        content=ft.Row(
            spacing=12,
            controls=[
                ft.Text(
                    "Imperative mode",
                    size=24,
                    weight=ft.FontWeight.W_600,
                ),
                count,
                ft.Button(
                    "Increment",
                    key="increment",
                    on_click=increment,  # type: ignore
                ),
            ],
        ),
    )


def build() -> ft.Control:

    return ft.Container(
        padding=20,
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text("Compteurs", size=24, weight=ft.FontWeight.W_600),
                sepa_outlined(),
                imperative_counter(),
                sepa_outlined(),
            ],
        ),
    )
