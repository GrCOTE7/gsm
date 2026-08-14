function Read-DotEnv {
    param([string]$Path)

    if (!(Test-Path $Path)) {
        return
    }

    Get-Content $Path | ForEach-Object {
        $line = $_.Trim()

        # Ignore commentaires et lignes vides
        if ($line -and !$line.StartsWith("#")) {
            $key, $value = $line -split "=", 2

            if ($key -and $value) {
                # Retire les espaces et commentaires éventuels
                $value = ($value -split "#")[0].Trim()

                Set-Item "Env:$($key.Trim())" $value
            }
        }
    }
}

Read-DotEnv "$PSScriptRoot\.env"

function Set-DotEnvValue {
    param(
        [string]$Path,
        [string]$Key,
        [string]$Value
    )

    $escapedKey = [regex]::Escape($Key)

    if (!(Test-Path $Path)) {
        Set-Content -Path $Path -Value "$Key=$Value"
        return
    }

    $lines = Get-Content $Path
    $found = $false

    $updated = $lines | ForEach-Object {
        if ($_ -match "^(\s*$escapedKey\s*=\s*)([^#]*?)(\s*(#.*)?)$") {
            $found = $true
            "$($matches[1])$Value$($matches[3])"
        }
        else {
            $_
        }
    }

    if (-not $found) {
        $updated += "$Key=$Value"
    }

    Set-Content -Path $Path -Value $updated
}

function Move-WindowsTerminalWindow {
    param(
        [int]$Left,
        [int]$Top,
        [int]$Width,
        [int]$Height
    )

    if (-not ("GsmWindowHelperV2" -as [type])) {
        Add-Type @"
using System;
using System.Runtime.InteropServices;

public class GsmWindowHelperV2
{
    public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

    [DllImport("user32.dll")]
    public static extern bool EnumWindows(EnumWindowsProc enumProc, IntPtr lParam);

    [DllImport("user32.dll")]
    public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);

    [DllImport("user32.dll")]
    public static extern bool IsWindowVisible(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern bool MoveWindow(
        IntPtr hWnd,
        int X,
        int Y,
        int nWidth,
        int nHeight,
        bool bRepaint);

    [DllImport("kernel32.dll")]
    public static extern IntPtr GetConsoleWindow();

    public static IntPtr FindWindowFromProcessId(uint pid)
    {
        IntPtr result = IntPtr.Zero;

        EnumWindows((hWnd, lParam) =>
        {
            uint windowPid;
            GetWindowThreadProcessId(hWnd, out windowPid);

            if (windowPid == pid && IsWindowVisible(hWnd))
            {
                result = hWnd;
                return false;
            }

            return true;
        }, IntPtr.Zero);

        return result;
    }
}
"@
    }

    $inWindowsTerminal = -not [string]::IsNullOrWhiteSpace($env:WT_SESSION)

    # 1) Console classique (hors Windows Terminal): cible directe précise.
    if (-not $inWindowsTerminal) {
        $hwnd = [GsmWindowHelperV2]::GetConsoleWindow()

        if ($hwnd -ne [IntPtr]::Zero -and [GsmWindowHelperV2]::IsWindowVisible($hwnd)) {
            $moved = [GsmWindowHelperV2]::MoveWindow(
                $hwnd,
                $Left,
                $Top,
                $Width,
                $Height,
                $true
            )

            if ($moved) {
                return $true
            }
        }
    }

    # 2) Fallback: ancêtres terminal connus uniquement
    # (évite de cibler VS Code/Explorer par erreur).
    $cursorPid = $PID
    $visited = @{}
    $parents = @()
    $hwnd = [IntPtr]::Zero

    while ($cursorPid -and -not $visited.ContainsKey($cursorPid)) {
        $visited[$cursorPid] = $true

        try {
            $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$cursorPid"
        }
        catch {
            break
        }

        if (-not $proc) {
            break
        }

        $parents += $proc
        $cursorPid = [int]$proc.ParentProcessId
    }

    $candidatePids = @()

    $terminalHostNames = if ($inWindowsTerminal) {
        @("windowsterminal", "wt", "openconsole", "conhost")
    }
    else {
        @("conhost", "openconsole", "windowsterminal", "wt")
    }

    foreach ($p in $parents) {
        $name = ""
        try {
            $name = (Get-Process -Id $p.ProcessId -ErrorAction Stop).ProcessName
        }
        catch {
            continue
        }

        if ($terminalHostNames -contains $name.ToLowerInvariant()) {
            $candidatePids += [uint32]$p.ProcessId
        }
    }

    $candidatePids = $candidatePids | Select-Object -Unique

    foreach ($pidCandidate in $candidatePids) {
        try {
            $procObj = Get-Process -Id $pidCandidate -ErrorAction Stop
            if ($procObj.MainWindowHandle -and $procObj.MainWindowHandle -ne 0) {
                $hwnd = [IntPtr]$procObj.MainWindowHandle
            }
            else {
                $hwnd = [GsmWindowHelperV2]::FindWindowFromProcessId($pidCandidate)
            }
        }
        catch {
            $hwnd = [IntPtr]::Zero
        }

        if ($hwnd -ne [IntPtr]::Zero) {
            break
        }
    }

    if ($hwnd -ne [IntPtr]::Zero) {
        $moved = [GsmWindowHelperV2]::MoveWindow(
            $hwnd,
            $Left,
            $Top,
            $Width,
            $Height,
            $true
        )

        if ($moved) {
            return $true
        }
    }

    if ($env:TERM_PROGRAM -eq "vscode") {
        Write-Warning "Terminal intégré VS Code détecté: cette vue ne peut pas être déplacée comme une fenêtre externe."
    }
    else {
        Write-Warning "Déplacement CLI impossible (fenêtre introuvable ou MoveWindow a échoué)"
    }

    return $false
}

# Repositionne CETTE fenêtre de terminal selon la variable d'env donnée,
# si elle vaut 1 — factorisé une seule fois, réutilisé pour gsm et upu.
function Move-CliIfNeeded {
    param(
        [string]$EnvVarName,
        [int]$Left,
        [int]$Top,
        [int]$Width = 540,
        [int]$Height = 300
    )

    $raw = [System.Environment]::GetEnvironmentVariable($EnvVarName)

    if ($raw -and [int]$raw -eq 1) {
        return (Move-WindowsTerminalWindow -Left $Left -Top $Top -Width $Width -Height $Height)
    }

    return $false
}

function Get-EnvInt {
    param(
        [string]$Name,
        [int]$Default
    )

    $raw = [System.Environment]::GetEnvironmentVariable($Name)
    $parsed = 0

    if ($raw -and [int]::TryParse($raw.Trim(), [ref]$parsed)) {
        return $parsed
    }

    return $Default
}

# --- MODIFICATION : nouvelle fonction pour initialiser l'environnement uv ---
function Initialize-UvEnvironment {
    # Si le parent a transmis le chemin de uv via la variable d'environnement UV_EXE
    if ($env:UV_EXE -and (Test-Path $env:UV_EXE)) {
        $uvDir = Split-Path $env:UV_EXE -Parent
        $env:Path = "$uvDir;$env:Path"
        Set-Alias -Name uv -Value $env:UV_EXE -Scope Script
        return $true
    }

    # Sinon, essayer de trouver uv dans le PATH actuel
    $uvExe = (Get-Command uv -ErrorAction SilentlyContinue).Source
    if ($uvExe) {
        $uvDir = Split-Path $uvExe -Parent
        $env:Path = "$uvDir;$env:Path"
        Set-Alias -Name uv -Value $uvExe -Scope Script
        return $true
    }

    # Chercher dans des emplacements courants si pas dans PATH
    $commonPaths = @(
        "$env:USERPROFILE\.cargo\bin\uv.exe",
        "$env:LOCALAPPDATA\Programs\uv\uv.exe",
        "$env:LOCALAPPDATA\Microsoft\WinGet\Links\uv.exe",
        "$env:ProgramFiles\uv\uv.exe"
    )
    foreach ($path in $commonPaths) {
        if (Test-Path $path) {
            $uvDir = Split-Path $path -Parent
            $env:Path = "$uvDir;$env:Path"
            $env:UV_EXE = $path
            Set-Alias -Name uv -Value $path -Scope Script
            return $true
        }
    }

    Write-Error "uv introuvable. Installez-le ou assurez-vous qu'il est dans le PATH."
    return $false
}

# ----------------------------------------------------------------------
#  CONFIGURATION (variables d'environnement)
# ----------------------------------------------------------------------
$gsmWindowLeft = Get-EnvInt -Name "GSM_WINDOW_LEFT" -Default 1913
$upuWindowLeft = Get-EnvInt -Name "UPU_WINDOW_LEFT" -Default 2445

# ----------------------------------------------------------------------
#  MODES SPÉCIAUX (commentés pour l'instant)
# ----------------------------------------------------------------------
# $mode = if ($args.Count -gt 0) { "$($args[0])".ToLowerInvariant() } else { "" }
#
# # En mode "u", force la CLI GSM sous la fenêtre, même si .env vaut 0.
# if ($mode -eq "u") {
#     Set-DotEnvValue -Path "$PSScriptRoot\.env" -Key "GSM_WINDOW_CLI" -Value "1"
#     Set-Item "Env:GSM_WINDOW_CLI" "1"
# }

# ----------------------------------------------------------------------
#  MODE INTERNE : _gsm_child
#  Utilisé comme fallback lorsque la console courante ne peut pas être
#  déplacée. Le script se relance dans une nouvelle fenêtre Windows Terminal
#  qui se positionnera sous l'application GSM.
# ----------------------------------------------------------------------
if ($args.Count -gt 0 -and "$($args[0])".ToLowerInvariant() -eq "_gsm_child") {
    # --- MODIFICATION : on initialise uv avant tout ---
    if (-not (Initialize-UvEnvironment)) {
        return
    }

    Move-CliIfNeeded -EnvVarName "GSM_WINDOW_CLI" -Left $gsmWindowLeft -Top 779

    Set-Location -Path "$PSScriptRoot"
    & "$PSScriptRoot\scripts\check_version_sync.ps1"
    uv sync --extra desktop
    uv run python -m flet.cli -V

    Write-Host "Lancement de l'application Flet - MODE APP"
    uv run python -m flet.cli run ./src/main_gsm.py -r
    return
}

# ----------------------------------------------------------------------
#  MODE INTERNE : _upu_child (commenté – réservé pour plus tard)
# ----------------------------------------------------------------------
# if ($args.Count -gt 0 -and "$($args[0])".ToLowerInvariant() -eq "_upu_child") {
#     if (-not (Initialize-UvEnvironment)) { return }
#     Move-CliIfNeeded -EnvVarName "UPU_WINDOW_CLI" -Left $upuWindowLeft -Top 779
#
#     Set-Location -Path "$PSScriptRoot"
#     uv run --active python -m flet.cli run ./main_upu.py -r
#     return
# }

# ----------------------------------------------------------------------
#  MODE NORMAL (aucun argument)
#  Lance uniquement l'application GSM.
# ----------------------------------------------------------------------
# Si GSM_WINDOW_CLI=1, tente de déplacer la console courante.
# Si échec (ex: terminal intégré VS Code), lance une nouvelle console
# qui exécutera l'application et se positionnera correctement.
$gsmCliMoved = $false
if ((Get-EnvInt -Name "GSM_WINDOW_CLI" -Default 0) -eq 1) {
    $gsmCliMoved = Move-CliIfNeeded -EnvVarName "GSM_WINDOW_CLI" -Left $gsmWindowLeft -Top 779

    if (-not $gsmCliMoved) {
        # --- MODIFICATION : on capture le chemin de uv avant de lancer l'enfant ---
        $uvExe = (Get-Command uv -ErrorAction SilentlyContinue).Source
        if ($uvExe) {
            $env:UV_EXE = $uvExe
        }
        else {
            Write-Warning "uv introuvable dans la session courante ; le processus enfant risque d'échouer."
        }

        # Fallback : on relance le script dans un nouveau Windows Terminal
        # avec le mode interne "_gsm_child".
        $pwshPath = Join-Path $PSHOME "pwsh.exe"
        $arguments = "-w new `"$pwshPath`" -NoExit -File `"$PSCommandPath`" _gsm_child"
        Start-Process wt.exe -ArgumentList $arguments
        return
    }
}

Set-Location -Path "$PSScriptRoot"
# $env:UV_PROJECT_ENVIRONMENT = ".uv-venv"

# Vérifie silencieusement l'alignement des versions; message orange uniquement en cas d'écart.
& "$PSScriptRoot\scripts\check_version_sync.ps1"

# Synchronise les dépendances (mode desktop uniquement pour le moment).
uv sync --extra desktop
uv run python -m flet.cli -V

Write-Host "Lancement de l'application Flet - MODE APP"
uv run python -m flet.cli run ./src/main_gsm.py -r

# ----------------------------------------------------------------------
#  ANCIEN CODE POUR LES MODES "u" et "w" (commenté)
#  À réactiver lorsque ces options seront implémentées.
# ----------------------------------------------------------------------
# if ($mode -eq "u") {
#     $needGsmCli = (Get-EnvInt -Name "GSM_WINDOW_CLI" -Default 0) -eq 1
#     $runGsmInChild = $needGsmCli -and (-not $gsmCliMoved)
#
#     if ($runGsmInChild) {
#         Start-Process wt.exe -ArgumentList "-w", "new", "pwsh", "-NoExit", "-File", $PSCommandPath, "_gsm_child"
#     }
#
#     # Ouvre un second terminal Windows Terminal, qui se relance lui-même
#     # avec le mode interne "_upu_child" : il se repositionne selon
#     # UPU_WINDOW_CLI puis lance main_upu.py — toute la logique (positions,
#     # lecture du .env) reste dans CE fichier, rien n'est dupliqué en ligne.
#     #
#     # Sur PowerShell 7.x (Core, ex. 7.6.4), -ArgumentList prend un vrai
#     # tableau : chaque élément est quoté automatiquement par .NET si
#     # besoin (espaces, etc.) — PAS de guillemets manuels ici, sinon on
#     # les retrouve littéralement dans l'argument (chemin cassé).
#     Start-Process wt.exe -ArgumentList "-w", "new", "pwsh", "-NoExit", "-File", $PSCommandPath, "_upu_child"
#
#     if ($runGsmInChild) {
#         return
#     }
# }
#
# if ($mode -eq "w") {
#     Write-Host "Lancement de l'application Flet - MODE WEB"
#     uv run python -m flet.cli run ./src/main_gsm.py -r --web
# }
# else {
#     Write-Host "Lancement de l'application Flet - MODE APP"
#     uv run python -m flet.cli run ./src/main_gsm.py -r
# }