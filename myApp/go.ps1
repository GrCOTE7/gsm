# Se placer dans la racine du projet (src reste une archive)
Set-Location -Path "$PSScriptRoot\.."

# Lancer explicitement l'app racine
uv run --active flet run -r main.py
