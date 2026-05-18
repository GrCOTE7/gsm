import flet as ft
import asyncio
from datetime import datetime


class App:
    def __init__(self, page: ft.Page, sport_version: str) -> None:
        self.page = page
        self.total_seconds = self.sport_duration()
        self.remaining_seconds = self.total_seconds
        self.completed_runs = 0

        formatted_dt: str = datetime.now().strftime(format="%d/%m/%Y - %H:%M")
        page_title: str = page.title or ""

        self.timer_text = ft.Text(
            value=self.format_mmss(self.remaining_seconds),
            size=56,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.CYAN_ACCENT_200,
            text_align=ft.TextAlign.CENTER,
        )
        self.start_button_label = ft.Text(
            value=f"Démarrer ({self.format_mmss(self.total_seconds)})",
            weight=ft.FontWeight.BOLD,
        )
        self.start_button = ft.Button(
            content=self.start_button_label,
            on_click=self.on_start_click,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=14),
                padding=ft.Padding(28, 20, 28, 20),
            ),
            width=280,
            height=72,
        )

        header_controls: list[ft.Control] = [
            ft.Text(
                value=page_title,
                color=ft.Colors.CYAN_400,
                weight=ft.FontWeight.BOLD,
                size=24,
            )
        ]
        version_controls: list[ft.Control] = [
            ft.Text(
                value=sport_version,
                color=ft.Colors.CYAN_400,
                weight=ft.FontWeight.BOLD,
                size=24,
            )
        ]
        date_controls: list[ft.Control] = [
            ft.Text(
                value=formatted_dt,
                text_align=ft.TextAlign.CENTER,
            )
        ]
        timer_controls: list[ft.Control] = [self.timer_text]
        action_controls: list[ft.Control] = [self.start_button]
        app_controls: list[ft.Control] = [
            ft.Row(
                controls=header_controls,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=version_controls,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=date_controls,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=timer_controls,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=action_controls,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ]
        page.add(ft.Column(controls=app_controls, spacing=18))

    def format_mmss(self, total_seconds: int) -> str:
        mins, secs = divmod(max(0, total_seconds), 60)
        return f"{mins:02d}:{secs:02d}"

    def on_start_click(self, _e) -> None:
        if self.start_button.disabled or self.completed_runs >= 2:
            return
        self.remaining_seconds = self.total_seconds
        self.start_button.disabled = True
        self.start_button_label.value = "En cours..."
        self.page.update()
        self.page.run_task(self.run_countdown)

    async def run_countdown(self) -> None:
        while self.remaining_seconds >= 0:
            self.timer_text.value = self.format_mmss(self.remaining_seconds)
            self.page.update()
            if self.remaining_seconds == 0:
                break
            await asyncio.sleep(1)
            self.remaining_seconds -= 1

        self.completed_runs += 1
        if self.completed_runs >= 2:
            self.start_button.disabled = True
            self.start_button_label.value = "BRAVO ! :-)"
        else:
            self.start_button.disabled = False
            self.start_button_label.value = (
                f"Relancer ({self.format_mmss(self.total_seconds)})"
            )
        self.page.update()

    def sport_duration(self) -> int:

        j = datetime.now().day
        duree = j * 15 + 345
        # print(duree)
        # duree = 15

        return duree // 2
