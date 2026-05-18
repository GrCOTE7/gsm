import flet as ft
import asyncio
from typing import cast


class Countdown(ft.Text):
    def __init__(self, seconds, size=100, color=ft.Colors.CYAN_ACCENT_200):
        super().__init__()
        self.seconds = seconds
        self.size = size
        self.color = color

    def did_mount(self):
        self.running = True
        page = cast(ft.Page, self.page)
        page.run_task(self.update_timer)

    def will_unmount(self):
        self.running = False

    async def update_timer(self):
        while self.seconds + 1 and self.running:
            mins, secs = divmod(self.seconds, 60)
            # print(secs)
            self.value = "{:02d}:{:02d}".format(mins, secs)
            self.update()
            await asyncio.sleep(1)
            self.seconds -= 1
