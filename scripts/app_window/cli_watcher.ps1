<#
    cli_watcher.ps1 — Lie les 2 CLI dédiées du mode gu (./go gu).

    Lancé par go.ps1 (mode interne _<app>_child) pour chaque CLI dédiée :
    quand l'une des deux CLI est fermée, ce watcher ferme l'autre.

    Mécanique :
    - go.ps1 écrit le PID de la console dans %TEMP%\gsm_cli_<app>.pid ;
    - chaque watcher surveille le .pid de l'AUTRE app : s'il meurt sans qu'un
      remplacement planifié soit en cours (flag %TEMP%\gsm_cli_replacing posé
      par app_launcher pendant un respawn), la CLI courante est fermée
      (taskkill de son pwsh → la fenêtre wt se ferme) ;
    - si la CLI courante est fermée, le watcher (enfant du pwsh) meurt avec elle.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$App
)

$ErrorActionPreference = 'SilentlyContinue'

$tempDir = $env:TEMP
$myPidFile = Join-Path $tempDir "gsm_cli_$App.pid"
$other = if ($App -eq 'gsm') { 'upu' } else { 'gsm' }
$otherPidFile = Join-Path $tempDir "gsm_cli_$other.pid"
$replacingFlagPath = Join-Path $tempDir "gsm_cli_replacing"

# Garde-fou : un seul watcher par CLI (fichier lock avec le PID du watcher).
$lockFile = Join-Path $tempDir "gsm_cli_$App.watcher.pid"
if (Test-Path $lockFile) {
    $lockPid = Get-Content $lockFile
    if ($lockPid -match '^\d+$' -and (Get-Process -Id ([int]$lockPid) -ErrorAction SilentlyContinue)) {
        exit  # un watcher est déjà actif pour cette CLI
    }
}
Set-Content -Path $lockFile -Value $PID -Encoding ascii

function Get-PidFrom([string]$file) {
    if (-not (Test-Path $file)) { return $null }
    $value = Get-Content $file
    if ($value -match '^\d+$') { return [int]$value }
    return $null
}

function Test-CliPid([string]$pidFile, [string]$appName) {
    $p = Get-PidFrom $pidFile
    if ($null -eq $p) { return $false }
    $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$p"
    return ($null -ne $proc -and $proc.Name -match 'pwsh|powershell' -and
        $proc.CommandLine -like "*go.ps1*_${appName}_child*")
}

function Test-MyCliAlive {
    $p = Get-PidFrom $myPidFile
    if ($null -eq $p) { return $false }
    return [bool](Get-Process -Id $p -ErrorAction SilentlyContinue)
}

$otherSeen = $false
while ($true) {
    Start-Sleep -Seconds 2

    # Ma CLI est fermée → ce watcher s'arrête.
    if (-not (Test-MyCliAlive)) { exit }

    if (Test-CliPid $otherPidFile $other) {
        $otherSeen = $true
        continue
    }
    if (-not $otherSeen) { continue }  # l'autre CLI n'a jamais existé → pas de lien

    # L'autre CLI existait et n'est plus là : attendre la fin d'un éventuel
    # remplacement planifié (flag posé par le launcher pendant un respawn gu).
    $waited = 0
    while ((Test-Path $replacingFlagPath) -and $waited -lt 40) {
        Start-Sleep -Milliseconds 500
        $waited += 1
    }

    # Vérification finale : si l'autre est toujours absente, c'est une VRAIE
    # fermeture → on ferme aussi la CLI courante.
    if (-not (Test-CliPid $otherPidFile $other)) {
        if (-not (Test-MyCliAlive)) { exit }
        $myPid = Get-PidFrom $myPidFile
        if ($null -ne $myPid) {
            taskkill /PID $myPid /T /F 2>$null | Out-Null
        }
        exit
    }
}
