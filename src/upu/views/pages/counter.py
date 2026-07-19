import flet as ft


def build() -> ft.Control:
    counter_value = ft.Text("0")

    def increment(_e: ft.ControlEvent) -> None:
        counter_value.value = str(int(counter_value.value) + 1)
        try:
            counter_value.update()
        except RuntimeError:
            # Hors page montee (tests unitaires), la valeur est deja mise a jour.
            pass

    return ft.Container(
        padding=20,
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text("Compteur", size=24, weight=ft.FontWeight.W_600),
                counter_value,
                ft.Button("Increment", key="increment", on_click=increment),
            ],
        ),
    )