# Se placer dans la racine du projet
Set-Location -Path "$PSScriptRoot"

# Vérifie silencieusement l'alignement des versions; message orange uniquement en cas d'écart.
& "$PSScriptRoot\scripts\check_version_sync.ps1"

uv sync

# Lancer explicitement l'app racine
# uv run --active flet run -r audio_04.py
# Utilise pyproject.toml path pour trouver le projet et les dépendances
# uv run --active python -m flet.cli run -r src/main.py


echo "Lancement de l'application Flet - MODE NORMAL"
uv run --active python -m flet.cli run -r # BON & NORMAL

# echo "Lancement de l'application Flet - MODE WEB"
# uv run --active python -m flet.cli run -r --web # Pour zoomer si détails
