import asyncio
import threading

import flet as ft

try:
    import winsound
except ImportError:
    winsound = None


def main(page: ft.Page):
    page.title = "Countdown avec tic-tac"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    secondes_input = ft.TextField(
        label="Durée (secondes)",
        value="10",
        width=180,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    remaining_text = ft.Text(value="10", size=56, weight=ft.FontWeight.BOLD)
    status_text = ft.Text(value="Prêt", size=18)

    task_id = 0
    is_running = False

    def play_tick(seconds_left: int) -> None:
        if winsound is None:
            return

        # Légère alternance de fréquence pour un effet "tic-tac".
        freq = 930 if seconds_left % 2 == 0 else 670
        threading.Thread(
            target=winsound.Beep,
            args=(freq, 120),
            daemon=True,
        ).start()

    async def run_countdown(current_task_id: int, total_seconds: int) -> None:
        nonlocal is_running, task_id

        is_running = True
        start_button.disabled = True
        stop_button.disabled = False
        page.update()

        for sec in range(total_seconds, -1, -1):
            if current_task_id != task_id:
                return

            remaining_text.value = str(sec)
            if sec > 0:
                status_text.value = "Tic" if sec % 2 == 0 else "Tac"
                play_tick(sec)
            else:
                status_text.value = "Terminé"

            page.update()
            if sec > 0:
                await asyncio.sleep(1)

        is_running = False
        start_button.disabled = False
        stop_button.disabled = True
        page.update()

    def on_start(_) -> None:
        nonlocal task_id

        if is_running:
            return

        try:
            total = int(secondes_input.value or "")
            if total <= 0:
                raise ValueError
        except ValueError:
            snackbar = ft.SnackBar(
                content=ft.Text("Entre un nombre entier > 0"),
                behavior=ft.SnackBarBehavior.FLOATING,
            )
            page.overlay.append(snackbar)
            snackbar.open = True
            page.update()
            return

        task_id += 1
        status_text.value = "Démarrage..."
        page.update()
        page.run_task(run_countdown, task_id, total)

    def on_stop(_) -> None:
        nonlocal is_running, task_id

        if not is_running:
            return

        task_id += 1
        is_running = False
        status_text.value = "Arrêté"
        start_button.disabled = False
        stop_button.disabled = True
        page.update()

    start_button = ft.Button("Démarrer", on_click=on_start)
    stop_button = ft.OutlinedButton("Stop", on_click=on_stop, disabled=True)

    page.add(
        ft.Column(
            controls=[
                ft.Text("Countdown", size=28, weight=ft.FontWeight.W_700),
                secondes_input,
                remaining_text,
                status_text,
                ft.Row(
                    [start_button, stop_button], alignment=ft.MainAxisAlignment.CENTER
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=16,
        )
    )


if __name__ == "__main__":
    ft.run(main=main)
