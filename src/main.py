import os
import flet as ft
import flet_audio  # noqa: F401

from upu.controllers.app_controller import create_app

# Détection automatique : Docker ou local ?
RUNNING_IN_DOCKER = os.environ.get("FLET_DOCKER", "0") == "1"

if RUNNING_IN_DOCKER:
    # Mode Web pour Docker
    ft.app(
        target=create_app,
        host="0.0.0.0",
        port=8000
    )
else:
    # Mode Desktop pour ton PC
    ft.run(create_app)

# Docker desktop doit être lancé
# docker compose up -d --build
# OU
# docker compose build --no-cache

# docker exec -it gsm_app sh  