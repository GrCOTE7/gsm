"""Section Versions : Python, Flet, paquets Flet, version GSM."""

import flet as ft

from ....helpers.diagnostic import collect_versions
from .section_ui import divider, heading, row


def build() -> ft.Control | None:
    data = collect_versions()

    py = data["python"]
    flet = data["flet"]
    app = data["app"]

    venv_marker = "✓" if py["venv_active"] else "✗"

    return ft.Column(
        spacing=4,
        controls=[
            heading("🐍 Python"),
            row("Version", py["version"]),
            row("Implémentation", py["implementation"]),
            row("Venv actif", venv_marker),
            divider(),
            heading("🎨 Flet"),
            row("flet", flet["flet"]),
            row("flet-cli", flet["flet-cli"]),
            row("flet-desktop", flet["flet-desktop"]),
            row("flet-web", flet["flet-web"]),
            divider(),
            heading("📦 Application"),
            row(app["name"], app["version"]),
        ],
    )
