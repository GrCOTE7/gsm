"""Section Système : OS, architecture, contexte d'exécution."""

import flet as ft

from ....config.app_env import app_env
from ....helpers.diagnostic import collect_system
from .section_ui import heading, row


def build() -> ft.Control | None:
    data = collect_system()
    is_local = app_env.is_local()
    platform = app_env.platform()

    docker_marker = "✓" if data["docker"] else "✗"
    local_marker = "✓" if is_local else "✗"

    return ft.Column(
        spacing=4,
        controls=[
            heading("🖥️ Système"),
            row("OS", f"{data['os']} {data['os_release']}"),
            row("Architecture", data["architecture"]),
            row("Docker", docker_marker),
            row("Local", local_marker),
            row("Platform", platform),
            row("PID", str(data["pid"])),
            row("Hostname", data["hostname"]),
        ],
    )
