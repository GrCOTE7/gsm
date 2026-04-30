import asyncio
import io
import math
import struct
import wave

import flet as ft
import flet_audio as fta


def _clock_tick_bytes(
    freq: int,
    ms: int = 110,
    sample_rate: int = 22050,
    transient_freq: int = 2900,
) -> bytes:
    frames_count = int(sample_rate * ms / 1000)
    amp = int(0.5 * 32767)
    buf = io.BytesIO()

    with wave.open(buf, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(
            b"".join(
                struct.pack(
                    "<h",
                    _clock_sample(
                        i, frames_count, sample_rate, freq, transient_freq, amp
                    ),
                )
                for i in range(frames_count)
            )
        )

    return buf.getvalue()


def _clock_sample(
    i: int,
    frames_count: int,
    sample_rate: int,
    freq: int,
    transient_freq: int,
    amp: int,
) -> int:
    t = i / sample_rate
    p = i / max(frames_count - 1, 1)

    # Enveloppe typique d'un mécanisme: attaque franche puis décroissance rapide.
    env = math.exp(-7.5 * p)

    # Corps du "tic": fondamental + harmonique métallique légère.
    body = math.sin(2 * math.pi * freq * t) + 0.38 * math.sin(
        2 * math.pi * 2.35 * freq * t
    )

    # Transitoire courte pour le "clic" initial.
    transient = math.sin(2 * math.pi * transient_freq * t) * math.exp(-42 * p)

    sample = amp * env * (0.78 * body + 0.22 * transient)
    return max(-32767, min(32767, int(sample)))


def main(page: ft.Page):
    page.title = "Countdown avec tic-tac"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    tac_src = _clock_tick_bytes(1120, ms=120, transient_freq=2500)

    players = [
        fta.Audio(
            src=tac_src,
            volume=1,
            release_mode=fta.ReleaseMode.STOP,
        ),
        fta.Audio(
            src=tac_src,
            volume=1,
            release_mode=fta.ReleaseMode.STOP,
        ),
    ]
    page.services.extend(players)

    secondes_input = ft.TextField(
        label="Durée (secondes)",
        value="10",
        width=180,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    remaining_text = ft.Text("10", size=56, weight=ft.FontWeight.BOLD)
    status_text = ft.Text("Prêt", size=18)

    run_id = 0
    is_running = False

    def set_running(value: bool) -> None:
        nonlocal is_running
        is_running = value
        start_button.disabled = value
        stop_button.disabled = not value
        page.update()

    async def countdown(current_id: int, total: int) -> None:
        nonlocal run_id

        set_running(True)
        for sec in range(total, -1, -1):
            if current_id != run_id:
                return

            remaining_text.value = str(sec)
            if sec > 0:
                status_text.value = "Tic" if sec % 2 == 0 else "Tac"
                page.run_task(players[sec % 2].play)
                page.update()
                await asyncio.sleep(1)
            else:
                status_text.value = "Terminé"
                page.update()

        set_running(False)

    def show_error(message: str) -> None:
        snackbar = ft.SnackBar(
            content=ft.Text(message), behavior=ft.SnackBarBehavior.FLOATING
        )
        page.overlay.append(snackbar)
        snackbar.open = True
        page.update()

    def on_start(_) -> None:
        nonlocal run_id

        if is_running:
            return

        try:
            total = int(secondes_input.value or "")
            if total <= 0:
                raise ValueError
        except ValueError:
            show_error("Entre un nombre entier > 0")
            return

        run_id += 1
        status_text.value = "Démarrage..."
        page.update()
        page.run_task(countdown, run_id, total)

    def on_stop(_) -> None:
        nonlocal run_id

        if not is_running:
            return

        run_id += 1
        status_text.value = "Arrêté"
        set_running(False)

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
    ft.run(main)
