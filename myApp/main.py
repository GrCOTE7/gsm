import flet as ft
import flet_audio  # noqa: F401

import gc7_tools.gc7 as gc7
import gc7_tools.screen_utils as screen_utils

from audio import main as audio_main

APP_NAME = "MyApp Test GC7"
VERSION = "0.0.1"


def main(page: ft.Page):
    screen_utils.gc7_rules(page, left=1526)  # 1526 ou 1912
    page.title = f"{APP_NAME} - v{VERSION}"

    audio_main(page)

    page.add(ft.Text(f"{APP_NAME} is ready."))

    print(gc7.curr_time(), page.route, ">")


ft.run(main)
