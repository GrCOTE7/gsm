# Windows launcher
#
# La fenêtre CLI dédiée (lancée par wt.exe) démarre avec un PATH minimal
# (sans 'python', sans 'uv') : on cible donc explicitement un interpréteur,
# en priorité le venv du projet.
Set-Location $PSScriptRoot

$venvPy = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
$uv = Get-Command uv -ErrorAction SilentlyContinue
$python = $null

if (Test-Path $venvPy) {
    $python = $venvPy
}
elseif ($uv) {
    $python = "uv"
}
elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $python = "python"
}
elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $python = "python3"
}
else {
    Write-Host "[ERROR] Python introuvable (venv manquant ?). Exécutez 'uv sync' puis relancez ./go."
    exit 1
}

$mainPy = Join-Path $PSScriptRoot "scripts\app_window\main.py"
if ($python -eq "uv") {
    & $python run python $mainPy @args
}
else {
    & $python $mainPy @args
}


# Pour linux
# #!/usr/bin/env bash
# python3 "$(dirname "$0")/launcher.py" "$@"
# (chmod +x go)
