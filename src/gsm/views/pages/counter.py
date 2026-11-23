# src/gsm/views/pages/counter.py
import flet as ft

from gsm.states.counter_state import CounterState


class CounterPage:
    """Page 'Compteur'."""

    @staticmethod
    @ft.component
    def transitionedBtn() -> ft.Row:  # Transitioned btn (Declarative)
        state, set_state = ft.use_state(True)

        return ft.Row(
            controls=[
                ft.Container(
                    width=100,
                    bgcolor=ft.Colors.GREEN if state else ft.Colors.RED,
                    border_radius=5,
                    animate=ft.Animation(1000, curve=ft.AnimationCurve.EASE_IN_OUT),
                    content=ft.Button(
                        ft.AnimatedSwitcher(
                            duration=700,
                            transition=ft.AnimatedSwitcherTransition.FADE,
                            content=ft.Text(
                                "GO!" if state else "Stop!", key=ft.ValueKey(state)
                            ),
                        ),
                        bgcolor=ft.Colors.TRANSPARENT,
                        color=ft.Colors.WHITE,
                        on_click=lambda _: set_state(not state),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=5),
                            mouse_cursor=ft.MouseCursor.CLICK,
                        ),
                    ),
                ),
                ft.Text(
                    str(state),
                    opacity=1 if state else 0.4,
                    animate_opacity=700,
                ),
            ]
        )

    @staticmethod
    @ft.component
    def view() -> ft.Control:
        state, _ = ft.use_state(lambda: CounterState())

        def handle_change(e: ft.Event[ft.TextField]) -> None:
            try:
                state.set_value(int(e.control.value))
            except ValueError:
                pass

        text_color = ft.Colors.GREEN if state.is_even else ft.Colors.DEEP_ORANGE

        # --- Version 1 : champ éditable, cadre animé (inchangée) --------
        value_field = ft.Container(
            content=ft.TextField(
                value=str(state.value),
                width=100,
                text_align=ft.TextAlign.CENTER,
                on_change=handle_change,
            ),
            padding=6,
            border_radius=8,
            border=ft.Border.all(2, text_color),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        )

        editable_controls = [
            ft.IconButton(
                ft.Icons.REMOVE,
                tooltip="Décrémenter",
                on_click=lambda _: state.decrement(),
            ),
            value_field,
            ft.IconButton(
                ft.Icons.ADD,
                tooltip="Incrémenter",
                on_click=lambda _: state.increment(),
            ),
        ]
        editable_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=editable_controls,
        )

        # --- Version 2 : lecture seule, texte avec un vrai fondu --------
        # `key=ft.ValueKey(state.value)` est indispensable : sans lui,
        # AnimatedSwitcher voit "le même Text, juste mis à jour" et ne
        # joue AUCUNE transition (comportement documenté de Flutter/Flet
        # : même type + même clé => mise à jour, pas d'animation).
        faded_display = ft.AnimatedSwitcher(
            content=ft.Text(
                str(state.value),
                key=ft.ValueKey(state.value),
                size=54,
                weight=ft.FontWeight.BOLD,
                color=text_color,
            ),
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=700,
        )

        return ft.Column(
            controls=[
                ft.Text("Compteur", size=28, weight=ft.FontWeight.BOLD),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Divider(),
                        CounterPage.transitionedBtn(),
                        ft.Divider(),
                        editable_row,
                        ft.Divider(),
                        faded_display,
                    ],
                ),
            ],
        )


if __name__ == "__main__":

    def main(page: ft.Page):
        page.title = "Flet counter example"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.render(CounterPage.view)

    ft.run(main)
