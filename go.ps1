# Se placer dans la racine du projet
Set-Location -Path "$PSScriptRoot"

# Vérifie silencieusement l'alignement des versions; message orange uniquement en cas d'écart.
& "$PSScriptRoot\scripts\check_version_sync.ps1"


# Lancer explicitement l'app racine
# uv run --active flet run -r audio_04.py
# Utilise pyproject.toml path pour trouver le projet et les dépendances
# uv run --active python -m flet.cli run -r src/main.py

uv sync --extra desktop

$mode = if ($args.Count -gt 0) { "$($args[0])".ToLowerInvariant() } else { "" }

if ($mode -eq "w") {
    echo "Lancement de l'application Flet - MODE WEB"
    uv run --active python -m flet.cli run -r --web
}
else {
    echo "Lancement de l'application Flet - MODE APP"
    uv run --active python -m flet.cli run -r
}
