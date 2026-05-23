import io
import math
import struct
import wave

import flet as ft
import flet_audio as fta


def build_beep_bytes() -> bytes:
    sr = 22050
    n = sr // 8
    amplitude = 24000
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
                        amplitude
                        * math.sin(2 * math.pi * 1200 * i / sr)
                        * math.exp(-6 * i / n)
                    ),
                )
                for i in range(n)
            )
        )
    return out.getvalue()


class BeepEngine:
    def __init__(self, page: ft.Page):
        self.page = page
        self.beep = build_beep_bytes()
        self.player = fta.Audio(
            src=self.beep,
            volume=1,
            release_mode=fta.ReleaseMode.STOP,
        )
        self.page.services.append(self.player)
        self.play_in_flight = False

    def reset_player(self) -> None:
        for service in list(self.page.services):
            if isinstance(service, fta.Audio):
                self.page.services.remove(service)
        self.player = fta.Audio(
            src=self.beep,
            volume=1,
            release_mode=fta.ReleaseMode.STOP,
        )
        self.page.services.append(self.player)
        self.play_in_flight = False

    async def play(self) -> None:
        await self.player.play()

    async def safe_play(self) -> None:
        if self.play_in_flight:
            return
        self.play_in_flight = True
        try:
            await self.player.play()
        except RuntimeError:
            pass
        finally:
            self.play_in_flight = False
