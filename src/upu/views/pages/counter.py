import flet as ft


def imperative_counter() -> ft.Control:
    count = 0
    text = ft.Text("0")

    def increment(_e) -> None:
        nonlocal count
        count += 1
        text.value = str(count)

    return ft.Row(
        [
            text,
            ft.Button("Increment", on_click=increment),
        ]
    )


# type: ignore


@ft.component
def declarative_counter_component() -> ft.Control:
    count, set_count = ft.use_state(0)

    return ft.Row(
        [
            ft.Text(str(count)),
            ft.Button(
                "Increment",
                on_click=lambda _: set_count(count + 1),
            ),
        ]
    )


def build() -> ft.Control:
    return ft.Column(
        [
            imperative_counter(),
            # declarative_counter_component(),
        ]
    )
