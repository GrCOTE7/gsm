import flet as ft

from gc7_tools.helpers import sepa_major, sepa_outlined


def imperative_counter() -> ft.Control:
    count = ft.Text("0")

    def increment(_e: ft.ControlEvent) -> None:
        count.value = str(int(count.value) + 1)

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

@ft.component
def declarative_counter_component() -> ft.Control:
    count, set_count = ft.use_state(0)

    def increment(_e: ft.ControlEvent) -> None:
        set_count(count.value + 1)

    return ft.Container(
        padding=20,
        content=ft.Row(
            spacing=12,
            controls=[
                ft.Text(
                    "Declarative mode",
                    size=24,
                    weight=ft.FontWeight.W_600,
                ),
                ft.Text(str(count)),
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
                sepa_major(),
                declarative_counter_component(),
                sepa_major(),
                # memorized_counter(),
                sepa_outlined(),
            ],
        ),
    )


# def declarative_counter() -> ft.Control:
#     count, set_count = ft.use_state(0)

#     def increment(_e: ft.ControlEvent) -> None:
#         set_count(count.value + 1)

#     return ft.Container(
#         padding=20,
#         content=ft.Row(
#             spacing=12,
#             controls=[
#                 ft.Text(
#                     "Declarative mode",
#                     size=24,
#                     weight=ft.FontWeight.W_600,
#                 ),
#                 ft.Text(str(count.value)),
#                 ft.Button(
#                     "Increment",
#                     key="increment",
#                     on_click=increment,  # type: ignore
#                 ),
#             ],
#         ),
#     )


# def memorized_counter() -> ft.Control:
#     count = ft.Text("0")

#     def increment(_e: ft.ControlEvent) -> None:
#         count.value = str(int(count.value) + 1)

#     return ft.Container(
#         padding=20,
#         content=ft.Row(
#             spacing=12,
#             controls=[
#                 ft.Text(
#                     "Memorized counter",
#                     size=24,
#                     weight=ft.FontWeight.W_600,
#                 ),
#                 count,
#                 ft.Button(
#                     "Increment",
#                     key="increment",
#                     on_click=increment,  # type: ignore
#                 ),
#             ],
#         ),
#     )
