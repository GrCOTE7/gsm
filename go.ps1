# Windows launcher
#
# La fenêtre CLI dédiée (lancée par wt.exe) démarre avec un PATH minimal
# (sans 'python', sans 'uv') : on cible donc explicitement un interpréteur,
# en priorité le venv du projet.
Set-Location $PSScriptRoot

# Journal de démarrage : indispensable pour diagnostiquer une console dédiée
# qui « ne s'ouvre pas » — elle vit dans sa propre fenêtre, donc ses erreurs ne
# remontent jamais dans le terminal qui a lancé ./go. Actif par défaut ; mettre
# GSM_GO_DEBUG=0 pour le désactiver. Le fichier est réinitialisé par le parent.
$goDebug = $env:GSM_GO_DEBUG -ne "0"
$goLogPath = Join-Path $env:TEMP "gsm_go_debug.log"
if ($goDebug -and $args.Count -eq 0) {
    Set-Content -Path $goLogPath -Value "" -Encoding utf8
}
function Write-GoDebug([string]$Message) {
    if (-not $goDebug) { return }
    $line = "{0} [{1}] {2}" -f (Get-Date -Format "HH:mm:ss.fff"), $PID, $Message
    Add-Content -Path $goLogPath -Value $line -Encoding utf8
}
Write-GoDebug "start args='$($args -join ' ')' PWD=$(Get-Location)"
Write-GoDebug "PATH=$env:PATH"
Write-GoDebug "VIRTUAL_ENV=$env:VIRTUAL_ENV UV_PROJECT_ENVIRONMENT=$env:UV_PROJECT_ENVIRONMENT"
trap { Write-GoDebug "ERREUR: $_"; break }

function Resolve-LauncherPython {
    <#
    Retourne l'interpréteur à utiliser pour lancer main.py :
    le venv du projet en priorité, sinon 'uv' (qui gère lui-même le venv),
    sinon un python du PATH. Retourne $null si rien n'est trouvé.
    #>
    $venvPy = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
    if (Test-Path $venvPy) { return $venvPy }
    if (Get-Command uv -ErrorAction SilentlyContinue) { return "uv" }
    if (Get-Command python -ErrorAction SilentlyContinue) { return "python" }
    if (Get-Command python3 -ErrorAction SilentlyContinue) { return "python3" }
    return $null
}

$mainPy = Join-Path $PSScriptRoot "scripts\app_window\main.py"

# CLI dédiée (mode interne _<app>_child[_mode]) : on enregistre le PID de la
# console (%TEMP%\gsm_cli_<app>.pid) et on lance le watcher de liaison — fermer
# l'une des deux CLI (mode gu) ferme aussi l'autre. Le watcher est idempotent
# (un seul par CLI via son fichier lock).
if ($args.Count -gt 0 -and $args[0] -match '^_(gsm|upu)_child') {
    $cliApp = $Matches[1]
    Set-Content -Path (Join-Path $env:TEMP "gsm_cli_$cliApp.pid") -Value $PID -Encoding ascii

    # Titre unique de la console : il permet au launcher de retrouver SA
    # fenêtre (et pas celle d'une CLI précédente restée ouverte) pour la
    # positionner et la mettre au premier plan.
    $cliTitle = "GSM-CLI::$PID"
    try { $Host.UI.RawUI.WindowTitle = $cliTitle } catch { }
    $env:GSM_CLI_WINDOW_TITLE = $cliTitle
    Write-GoDebug "titre console=$cliTitle"

    $watcherPwsh = Join-Path $PSHOME "pwsh.exe"
    if (-not (Test-Path $watcherPwsh)) { $watcherPwsh = "pwsh" }
    Start-Process -WindowStyle Hidden -FilePath $watcherPwsh -ArgumentList @(
        "-NoProfile", "-NonInteractive", "-WindowStyle", "Hidden",
        "-File", (Join-Path $PSScriptRoot "scripts\app_window\cli_watcher.ps1"),
        "-App", $cliApp
    ) | Out-Null
}

$python = Resolve-LauncherPython
if (-not $python) {
    Write-Host "[ERROR] Python introuvable (venv manquant ?). Exécutez 'uv sync' puis relancez ./go."
    Write-GoDebug "python introuvable"
    exit 1
}
Write-GoDebug "python=$python"

if ($python -eq "uv") {
    & $python run python $mainPy @args
}
else {
    & $python $mainPy @args
}
Write-GoDebug "fin (exit=$LASTEXITCODE)"
