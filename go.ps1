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


$mode = if ($args.Count -gt 0) { "$($args[0])".ToLowerInvariant() } else { "" }

# if ($mode -eq "p") {
#     Move-WindowsTerminalWindow -Left 2460 -Top 779 -Width 540 -Height 300
# }

if ([int]$env:UPU_WINDOW_CLI -eq 1) {
    Move-WindowsTerminalWindow `
        -Left 2460 `
        -Top 779 `
        -Width 540 `
        -Height 300
}

# Move-WindowsTerminalWindow -Left 2460 -Top 779 -Width 540 -Height 300

Set-Location -Path "$PSScriptRoot"

& "$PSScriptRoot\scripts\check_version_sync.ps1"

uv sync --extra desktop

##################################################################

# Se placer dans la racine du projet
Set-Location -Path "$PSScriptRoot"

# Vérifie silencieusement l'alignement des versions; message orange uniquement en cas d'écart.
& "$PSScriptRoot\scripts\check_version_sync.ps1"


# Lancer explicitement l'app racine
# uv run --active flet run -r audio_04.py
# Utilise pyproject.toml path pour trouver le projet et les dépendances
# uv run --active python -m flet.cli run -r src/main.py

uv sync --extra desktop

$mode = if ($args.Count -gt 0) { "$($args[0])".ToLowerInvariant() } else { "" }

uv run flet -V

if ($mode -eq "w") {
    echo "Lancement de l'application Flet - MODE WEB"
    uv run --active python -m flet.cli run -r --web
}
else {
    echo "Lancement de l'application Flet - MODE APP"
    uv run --active python -m flet.cli run -r
}
