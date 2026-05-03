import asyncio

import flet as ft

try:
    from .beep_engine import BeepEngine
    from .countdown import run_countdown
except ImportError:
    from beep_engine import BeepEngine
    from countdown import run_countdown


def main(page: ft.Page):
    page.title = "Countdown minimal"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    start = 15

    txt = ft.Text(str(start), size=80, weight=ft.FontWeight.BOLD)
    status = ft.Text("", size=14)
    start_btn = ft.Button("Démarrer", visible=False)
    beep = BeepEngine(page)
    page.add(txt, status, start_btn)

    is_running = False

    async def run_countdown_ui() -> None:
        nonlocal is_running
        if is_running:
            return
        is_running = True
        start_btn.disabled = True
        page.update()

        def on_tick(sec: int) -> None:
            txt.value = str(sec)
            page.update()

        async def on_step(sec: int) -> None:
            in_first_five = sec > start - 5
            in_last_five = sec <= 5
            if in_first_five or in_last_five:
                page.run_task(beep.safe_play)

        await run_countdown(start=start, on_tick=on_tick, on_step=on_step)

        is_running = False
        start_btn.disabled = False
        page.update()

    async def boot() -> None:
        beep.reset_player()
        await asyncio.sleep(0.2)
        try:
            await beep.play()
            await run_countdown_ui()
        except RuntimeError:
            status.value = "Clique sur Démarrer pour activer le son"
            start_btn.visible = True
            page.update()

    def on_start(_):
        beep.reset_player()
        status.value = ""
        page.update()
        page.run_task(run_countdown_ui)

    start_btn.on_click = on_start
    page.run_task(boot)


if __name__ == "__main__":
    ft.run(main)
