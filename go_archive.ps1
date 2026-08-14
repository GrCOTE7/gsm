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
        [int]$Height,
        [switch]$Silent
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

    # 1) Tente TOUJOURS la console courante en priorité.
    # WT_SESSION peut être hérité d'un parent VS Code/WT alors que ce process
    # enfant a bien sa propre fenêtre console déplaçable.
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

    if (-not $Silent) {
        if ($env:TERM_PROGRAM -eq "vscode") {
            Write-Warning "Terminal intégré VS Code détecté: cette vue ne peut pas être déplacée comme une fenêtre externe."
        }
        else {
            Write-Warning "Déplacement CLI impossible (fenêtre introuvable ou MoveWindow a échoué)"
        }
    }

    return $false
}

function Move-WindowsTerminalWindowWithRetry {
    param(
        [int]$Left,
        [int]$Top,
        [int]$Width,
        [int]$Height,
        [int]$Attempts = 20,
        [int]$DelayMs = 120
    )

    for ($i = 0; $i -lt $Attempts; $i++) {
        if (Move-WindowsTerminalWindow -Left $Left -Top $Top -Width $Width -Height $Height -Silent) {
            return $true
        }

        # Le host console peut apparaître légèrement après le démarrage du script enfant.
        [System.Threading.Thread]::Sleep($DelayMs)
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
        return (Move-WindowsTerminalWindowWithRetry -Left $Left -Top $Top -Width $Width -Height $Height)
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

    return $Defaultj'ai 2 app s python - flet
}

function Get-ChildPowerShellExe {
    foreach ($name in @("pwsh", "powershell")) {
        $cmd = Get-Command $name -ErrorAction SilentlyContinue
        if ($cmd -and $cmd.Source) {
            return $cmd.Source
        }
    }

    return $null
}

function Get-UvExe {
    $hint = [System.Environment]::GetEnvironmentVariable("GSM_UV_EXE")
    if ($hint -and (Test-Path $hint)) {
        return $hint
    }

    $uvCmd = Get-Command uv -ErrorAction SilentlyContinue
    if ($uvCmd -and $uvCmd.Source) {
        return $uvCmd.Source
    }

    $candidates = @(
        "$PSScriptRoot\.venv\Scripts\uv.exe",
        "$PSScriptRoot\.uv-venv\Scripts\uv.exe"
    )

    foreach ($candidate in $candidates) {
        if (Test-Path $candidate) {
            return $candidate
        }
    }

    throw "Impossible de trouver uv (ni dans PATH, ni dans .venv/.uv-venv)."
}

function Invoke-Uv {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Args
    )

    $uvExe = Get-UvExe
    & $uvExe @Args
}

function Start-UvDetached {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Args
    )

    $uvExe = Get-UvExe
    Start-Process -FilePath $uvExe -ArgumentList $Args -WorkingDirectory $PSScriptRoot | Out-Null
}

function Start-GoChildWindow {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ChildMode,
        [int]$Left = 0,
        [switch]$ForceCli
    )

    $childPwshExe = Get-ChildPowerShellExe
    if (-not $childPwshExe) {
        throw "Impossible de trouver un exécutable PowerShell (pwsh ou powershell) pour lancer les fenêtres enfants."
    }

    Set-Item "Env:GSM_UV_EXE" "$(Get-UvExe)"

    $childArgs = @("-NoExit", "-File", $PSCommandPath, $ChildMode)

    if ($Left -ne 0) {
        $childArgs += "$Left"
    }

    if ($ForceCli) {
        $childArgs += "forcecli"
    }

    # Important: lancement direct du shell enfant (hors wt.exe) pour obtenir
    # une vraie fenêtre console déplacable de façon fiable.
    Start-Process -FilePath $childPwshExe -ArgumentList $childArgs -WorkingDirectory $PSScriptRoot | Out-Null
}

$mode = if ($args.Count -gt 0) { "$($args[0])".ToLowerInvariant() } else { "" }

$gsmWindowLeft = Get-EnvInt -Name "GSM_WINDOW_LEFT" -Default 1913
$upuWindowLeft = Get-EnvInt -Name "UPU_WINDOW_LEFT" -Default 2445

# --- Mode interne : ce process EST le second terminal, dédié à upu ------
# Déclenché uniquement quand ce script se relance lui-même (voir mode "u"
# plus bas) — pas un mode que tu tapes toi-même en ligne de commande.
if ($mode -eq "_upu_child") {
    # Optionnel: permet au parent de forcer la position/CLI pour le mode "u"
    # sans modifier durablement le .env.
    $childUpuLeft = $upuWindowLeft
    $forceUpuCli = $false

    if ($args.Count -gt 1) {
        $parsedLeft = 0
        if ([int]::TryParse("$($args[1])", [ref]$parsedLeft)) {
            $childUpuLeft = $parsedLeft
        }
    }

    if ($args.Count -gt 2 -and "$($args[2])".ToLowerInvariant() -eq "forcecli") {
        $forceUpuCli = $true
    }

    # Alimente la conf UPU lue par l'app (process enfant uniquement).
    Set-Item "Env:UPU_WINDOW_LEFT" "$childUpuLeft"

    if ($forceUpuCli) {
        Move-WindowsTerminalWindowWithRetry -Left $childUpuLeft -Top 779 -Width 540 -Height 300 | Out-Null
    }
    else {
        Move-CliIfNeeded -EnvVarName "UPU_WINDOW_CLI" -Left $childUpuLeft -Top 779 | Out-Null
    }

    Set-Location -Path "$PSScriptRoot"
    Invoke-Uv -Args @("run", "--active", "python", "-m", "flet.cli", "run", "./main_upu.py", "-r")
    return
}

if ($mode -eq "_gsm_child") {
    $childGsmLeft = $gsmWindowLeft
    $forceGsmCli = $false

    if ($args.Count -gt 1) {
        $parsedLeft = 0
        if ([int]::TryParse("$($args[1])", [ref]$parsedLeft)) {
            $childGsmLeft = $parsedLeft
        }
    }

    if ($args.Count -gt 2 -and "$($args[2])".ToLowerInvariant() -eq "forcecli") {
        $forceGsmCli = $true
    }

    # Alimente la conf GSM lue par l'app (process enfant uniquement).
    Set-Item "Env:GSM_WINDOW_LEFT" "$childGsmLeft"

    if ($forceGsmCli) {
        Move-WindowsTerminalWindowWithRetry -Left $childGsmLeft -Top 779 -Width 540 -Height 300 | Out-Null
    }
    else {
        Move-CliIfNeeded -EnvVarName "GSM_WINDOW_CLI" -Left $childGsmLeft -Top 779 | Out-Null
    }

    Set-Location -Path "$PSScriptRoot"
    & "$PSScriptRoot\scripts\check_version_sync.ps1"
    Invoke-Uv -Args @("sync", "--extra", "desktop")
    Invoke-Uv -Args @("run", "python", "-m", "flet.cli", "-V")

    Write-Host "Lancement de l'application Flet - MODE APP"
    Invoke-Uv -Args @("run", "python", "-m", "flet.cli", "run", "./src/main_gsm.py", "-r")
    return
}

# --- Mode normal ----------------------------------------------------------

# Place le terminal courant sous la fenêtre de l'app gsm, si demandé.
$gsmCliMoved = $false
if ($mode -ne "gu" -and $mode -ne "u") {
    $gsmCliMoved = Move-CliIfNeeded -EnvVarName "GSM_WINDOW_CLI" -Left $gsmWindowLeft -Top 779
}

Set-Location -Path "$PSScriptRoot"
# $env:UV_PROJECT_ENVIRONMENT = ".uv-venv"

# Vérifie silencieusement l'alignement des versions; message orange uniquement en cas d'écart.
& "$PSScriptRoot\scripts\check_version_sync.ps1"

# if ($mode -eq "w") {
#     uv sync --extra desktop --extra web
# }
# else {
#     uv sync --extra desktop
# }
# uv run python -m flet.cli -V

if ($mode -eq "gu") {
    $wantGsmCli = (Get-EnvInt -Name "GSM_WINDOW_CLI" -Default 0) -eq 1
    $wantUpuCli = (Get-EnvInt -Name "UPU_WINDOW_CLI" -Default 0) -eq 1

    if ($wantUpuCli) {
        Start-GoChildWindow -ChildMode "_upu_child" -Left $upuWindowLeft -ForceCli
    }
    else {
        Start-UvDetached -Args @("run", "--active", "python", "-m", "flet.cli", "run", "./main_upu.py", "-r")
    }

    if ($wantGsmCli) {
        Start-GoChildWindow -ChildMode "_gsm_child" -Left $gsmWindowLeft -ForceCli
    }
    else {
        Start-UvDetached -Args @("run", "python", "-m", "flet.cli", "run", "./src/main_gsm.py", "-r")
    }

    return
}
elseif ($mode -eq "u") {
    Write-Host "Lancement de l'application Flet UPU - MODE APP"
    Set-Item "Env:UPU_WINDOW_LEFT" "$gsmWindowLeft"
    $wantUpuCli = (Get-EnvInt -Name "UPU_WINDOW_CLI" -Default 0) -eq 1

    if ($wantUpuCli) {
        Start-GoChildWindow -ChildMode "_upu_child" -Left $gsmWindowLeft -ForceCli
    }
    else {
        Start-UvDetached -Args @("run", "--active", "python", "-m", "flet.cli", "run", "./main_upu.py", "-r")
    }

    return
}
elseif ($mode -eq "w") {
    Write-Host "Lancement de l'application Flet GSM - MODE WEB"
    Invoke-Uv -Args @("run", "python", "-m", "flet.cli", "run", "./src/main_gsm.py", "-r", "--web")
}
else {
    Write-Host "Lancement de l'application Flet GSM - MODE APP"
    $wantGsmCli = (Get-EnvInt -Name "GSM_WINDOW_CLI" -Default 0) -eq 1

    # Si une CLI sous la fenêtre est demandée mais impossible à déplacer
    # (ex: terminal intégré VS Code), on bascule vers un child dédié.
    if ($wantGsmCli -and (-not $gsmCliMoved)) {
        Start-GoChildWindow -ChildMode "_gsm_child" -Left $gsmWindowLeft -ForceCli
        return
    }

    Invoke-Uv -Args @("run", "python", "-m", "flet.cli", "run", "./src/main_gsm.py", "-r")
}
