# Git User Switcher (gu.ps1)

param(
    [ValidateSet("mp", "gc7")]
    [string]$set
)

# --- Charger le .env ---
$envPath = ".env"

if (Test-Path $envPath) {
    $envContent = Get-Content $envPath
}
else {
    Write-Host "⚠️ Fichier .env introuvable"
    exit 1
}

function Get-EnvValue($key) {
    $line = $envContent | Where-Object { $_ -match "^$key=" }
    if ($line) { return $line.Split("=")[1] }
    return $null
}

# --- Récupération des valeurs ---
$email_mp = Get-EnvValue "EMAIL_MP"
$email_gc7 = Get-EnvValue "EMAIL_GC7"

# --- Sans option : afficher l'identité actuelle ---
if (-not $set) {
    $name = git config --global user.name
    $email = git config --global user.email

    Write-Host "Current Git identity:"
    Write-Host "  user.name  = $name"
    Write-Host "  user.email = $email"
    exit
}

# --- Appliquer l'identité demandée ---
switch ($set) {
    "mp" {
        git config --global user.name "MP"
        git config --global user.email $email_mp
        Write-Host "Git identity set to MP"
    }
    "gc7" {
        git config --global user.name "GrCOTE7"
        git config --global user.email $email_gc7
        Write-Host "Git identity set to GrCOTE7"
    }
}
