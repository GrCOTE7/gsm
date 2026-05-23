# $initialDir = Get-Location
# try {
#   Set-Location -Path "$PSScriptRoot"
#   uv run --active flet run -r -w .\main.py
# }
# finally {
#   Set-Location -Path $initialDir
# }
# Se placer dans la racine du projet (src reste une archive)
Set-Location -Path "$PSScriptRoot\.."

# Lancer explicitement l'app racine
./go
