#!/bin/bash

# Aller à la racine du projet
cd "$(dirname "$0")"

# Lancer l'app en mode web
uv run flet run --web
