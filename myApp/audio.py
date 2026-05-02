import asyncio
import io
import math
import struct
import wave

import flet as ft
import flet_audio as fta


def _beep_bytes() -> bytes:
    sr = 22050
    n = sr // 8
    out = io.BytesIO()
    with wave.open(out, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(
            b"".join(
                struct.pack(
                    "<h",
                    int(
                        14000
                        * math.sin(2 * math.pi * 1200 * i / sr)
                        * math.exp(-6 * i / n)
                    ),
                )
                for i in range(n)
            )
        )
    return out.getvalue()


def main(page: ft.Page):
    page.title = "Countdown minimal"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    start = 10

    txt = ft.Text(str(start), size=80, weight=ft.FontWeight.BOLD)
    status = ft.Text("", size=14)
    start_btn = ft.Button("Démarrer", visible=False)
    beep = _beep_bytes()
    player = fta.Audio(src=beep, volume=1, release_mode=fta.ReleaseMode.STOP)
    page.services.append(player)
    page.add(txt, status, start_btn)

    is_running = False
    play_in_flight = False

    def reset_player() -> None:
        nonlocal player, play_in_flight
        for service in list(page.services):
            if isinstance(service, fta.Audio):
                page.services.remove(service)
        player = fta.Audio(src=beep, volume=1, release_mode=fta.ReleaseMode.STOP)
        page.services.append(player)
        play_in_flight = False

    async def safe_play() -> None:
        nonlocal play_in_flight
        if play_in_flight:
            return
        play_in_flight = True
        try:
            await player.play()
        except RuntimeError:
            pass
        finally:
            play_in_flight = False

    async def run_countdown() -> None:
        nonlocal is_running
        if is_running:
            return
        is_running = True
        start_btn.disabled = True
        page.update()

        for sec in range(start, -1, -1):
            txt.value = str(sec)
            page.update()
            if sec > 0:
                page.run_task(safe_play)
                await asyncio.sleep(1)

        is_running = False
        start_btn.disabled = False
        page.update()

    async def boot() -> None:
        reset_player()
        await asyncio.sleep(0.2)
        try:
            await player.play()
            await run_countdown()
        except RuntimeError:
            status.value = "Clique sur Demarrer pour activer le son"
            start_btn.visible = True
            page.update()

    def on_start(_):
        reset_player()
        status.value = ""
        page.update()
        page.run_task(run_countdown)

    start_btn.on_click = on_start
    page.run_task(boot)


if __name__ == "__main__":
    ft.run(main)
