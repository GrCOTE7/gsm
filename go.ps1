# Se placer dans la racine du projet
Set-Location -Path "$PSScriptRoot"

# Vérifie silencieusement l'alignement des versions; message orange uniquement en cas d'écart.
& "$PSScriptRoot\scripts\check_version_sync.ps1"

# Lancer explicitement l'app racine
# uv run --active flet run -r audio_04.py
# Utilise pyproject.toml path pour trouver le projet et les dépendances
# uv run --active python -m flet.cli run -r src/main.py
uv run --active python -m flet.cli run -r
