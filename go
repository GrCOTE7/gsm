#!/bin/bash
cd "$(dirname "$0")"

uv sync --extra desktop

mode="${1:-}"

if [ "$mode" = "w" ]; then
    echo "Lancement de l'application Flet - MODE WEB"
    uv run --active python -m flet.cli run -r --web
else
    echo "Lancement de l'application Flet - MODE APP"
    uv run --active python -m flet.cli run -r
fi
