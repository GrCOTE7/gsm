import os
import flet as ft

from upu.controllers.app_controller import create_app

RUNNING_IN_DOCKER = os.environ.get("FLET_DOCKER", "0") == "1"

if RUNNING_IN_DOCKER:
    ft.run(
        create_app,
        host="0.0.0.0",
        port=8000,
        view=ft.AppView.WEB_BROWSER,
    )
else:
    ft.run(create_app)


# Docker desktop doit être lancé
# docker compose up -d --build
# OU

# docker compose build --no-cache
# docker compose up -d

# docker exec -it gsm_app sh
