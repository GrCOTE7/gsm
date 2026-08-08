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

function Move-WindowsTerminalWindow {
    param(
        [int]$Left,
        [int]$Top,
        [int]$Width,
        [int]$Height
    )

    Add-Type @"
using System;
using System.Runtime.InteropServices;

public class WindowHelper
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

    # Récupère WindowsTerminal.exe parent de pwsh
    $parent = Get-CimInstance Win32_Process -Filter "ProcessId=$PID"

    $terminal = Get-Process -Id $parent.ParentProcessId

    $hwnd = [WindowHelper]::FindWindowFromProcessId($terminal.Id)

    if ($hwnd -ne [IntPtr]::Zero) {
        [WindowHelper]::MoveWindow(
            $hwnd,
            $Left,
            $Top,
            $Width,
            $Height,
            $true
        ) | Out-Null
    }
    else {
        Write-Warning "Fenêtre Windows Terminal introuvable"
    }
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
        Move-WindowsTerminalWindow -Left $Left -Top $Top -Width $Width -Height $Height
    }
}

$mode = if ($args.Count -gt 0) { "$($args[0])".ToLowerInvariant() } else { "" }

# --- Mode interne : ce process EST le second terminal, dédié à upu ------
# Déclenché uniquement quand ce script se relance lui-même (voir mode "u"
# plus bas) — pas un mode que tu tapes toi-même en ligne de commande.
if ($mode -eq "_upu_child") {
    Move-CliIfNeeded -EnvVarName "UPU_WINDOW_CLI" -Left 2445 -Top 779

    Set-Location -Path "$PSScriptRoot"
    uv run --active python -m flet.cli run ./main_upu.py -r
    return
}

# --- Mode normal ----------------------------------------------------------

# Place le terminal courant sous la fenêtre de l'app gsm, si demandé —
# s'applique à TOUS les modes (défaut, web, u), puisque gsm tourne dans
# CE terminal dans les trois cas.
Move-CliIfNeeded -EnvVarName "GSM_WINDOW_CLI" -Left 1913 -Top 779

Set-Location -Path "$PSScriptRoot"
$env:UV_PROJECT_ENVIRONMENT = ".uv-venv"

# Vérifie silencieusement l'alignement des versions; message orange uniquement en cas d'écart.
& "$PSScriptRoot\scripts\check_version_sync.ps1"

if ($mode -eq "w") {
    uv sync --extra desktop --extra web
}
else {
    uv sync --extra desktop
}
uv run python -m flet.cli -V

if ($mode -eq "u") {
    # Ouvre un second terminal Windows Terminal, qui se relance lui-même
    # avec le mode interne "_upu_child" : il se repositionne selon
    # UPU_WINDOW_CLI puis lance main_upu.py — toute la logique (positions,
    # lecture du .env) reste dans CE fichier, rien n'est dupliqué en ligne.
    #
    # Sur PowerShell 7.x (Core, ex. 7.6.4), -ArgumentList prend un vrai
    # tableau : chaque élément est quoté automatiquement par .NET si
    # besoin (espaces, etc.) — PAS de guillemets manuels ici, sinon on
    # les retrouve littéralement dans l'argument (chemin cassé).
    Start-Process wt.exe -ArgumentList "pwsh", "-NoExit", "-File", $PSCommandPath, "_upu_child"
}

if ($mode -eq "w") {
    Write-Host "Lancement de l'application Flet - MODE WEB"
    uv run python -m flet.cli run ./src/main_gsm.py -r --web
}
else {
    Write-Host "Lancement de l'application Flet - MODE APP"
    uv run python -m flet.cli run ./src/main_gsm.py -r
}
