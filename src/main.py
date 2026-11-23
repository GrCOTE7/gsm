# src/main.py
import os

import flet as ft

from gsm.bootstrap.app_bootstrap import AppBootstrap

if os.getenv("FLET_DOCKER") == "1":
    ft.run(AppBootstrap, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=8000)
else:
    ft.run(AppBootstrap)
