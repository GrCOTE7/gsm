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

# CLI dédiée (mode interne _<app>_child[_mode]) : on enregistre le PID de la
# console (%TEMP%\gsm_cli_<app>.pid) et on lance le watcher de liaison — fermer
# l'une des deux CLI (mode gu) ferme aussi l'autre. Le watcher est idempotent
# (un seul par CLI via son fichier lock).
if ($args.Count -gt 0 -and $args[0] -match '^_(gsm|upu)_child') {
    $cliApp = $Matches[1]
    Set-Content -Path (Join-Path $env:TEMP "gsm_cli_$cliApp.pid") -Value $PID -Encoding ascii
    $watcherPwsh = Join-Path $PSHOME "pwsh.exe"
    if (-not (Test-Path $watcherPwsh)) { $watcherPwsh = "pwsh" }
    Start-Process -WindowStyle Hidden -FilePath $watcherPwsh -ArgumentList @(
        "-NoProfile", "-NonInteractive", "-WindowStyle", "Hidden",
        "-File", (Join-Path $PSScriptRoot "scripts\app_window\cli_watcher.ps1"),
        "-App", $cliApp
    ) | Out-Null
}

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
