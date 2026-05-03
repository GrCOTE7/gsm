# Se placer dans la racine du projet
# Set-Location -Path "$PSScriptRoot/myApp"

# Lancer explicitement l'app racine
# uv run --active flet run -r audio_04.py
# Utilise pyproject.toml path pour trouver le projet et les dépendances
uv run --active flet run -r
