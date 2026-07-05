#!/bin/bash
cd "$(dirname "$0")"

uv sync --extra desktop
uv run src/main.py
# --web --host 0.0.0.0 --port 8550
