#!/bin/bash
cd "$(dirname "$0")"

uv run flet run --web --host 0.0.0.0 --port 8550
