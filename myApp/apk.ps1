# Se placer dans la racine du projet (src reste une archive)
Set-Location -Path "$PSScriptRoot\.."

# Lancer explicitement le build de l'app
# uv run flet run --android
./apk
