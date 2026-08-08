#!/bin/bash
cd "$(dirname "$0")"

export UV_PROJECT_ENVIRONMENT=".uv-venv"

mode="${1:-}"

if [ "$mode" = "w" ]; then
    echo "Lancement de l'application Flet - MODE WEB"
    uv sync --extra desktop --extra web
    uv run python -m flet.cli run src/main_gsm.py -r --web
else
    echo "Lancement de l'application Flet - MODE APP"
    uv sync --extra desktop
    uv run python -m flet.cli run src/main_gsm.py -r
fi
