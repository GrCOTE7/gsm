"""Section Versions : Python, Flet, paquets Flet, version GSM."""

import flet as ft

from ....helpers.diagnostic import collect_versions


def _row(label: str, value: str) -> ft.Control:
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Text(label, weight=ft.FontWeight.W_500),
            ft.Text(value, selectable=True),
        ],
    )


def _heading(text: str) -> ft.Control:
    return ft.Text(text, size=14, weight=ft.FontWeight.BOLD, italic=True)


def build() -> ft.Control | None:
    data = collect_versions()

    py = data["python"]
    flet = data["flet"]
    app = data["app"]

    venv_marker = "✓" if py["venv_active"] else "✗"

    return ft.Column(
        spacing=4,
        controls=[
            _heading("🐍 Python"),
            _row("Version", py["version"]),
            _row("Implémentation", py["implementation"]),
            _row("Venv actif", venv_marker),
            ft.Divider(height=8),
            _heading("🎨 Flet"),
            _row("flet", flet["flet"]),
            _row("flet-cli", flet["flet-cli"]),
            _row("flet-desktop", flet["flet-desktop"]),
            _row("flet-web", flet["flet-web"]),
            ft.Divider(height=8),
            _heading("📦 Application"),
            _row(app["name"], app["version"]),
        ],
    )
