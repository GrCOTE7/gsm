# Se placer dans la racine du projet
Set-Location -Path "$PSScriptRoot"

# Lancer explicitement le build APK de l'app
uv run flet build apk -v
