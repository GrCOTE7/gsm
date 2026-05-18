# =====================================================================
#  reset_gh.ps1
#  Réinitialise complètement le dépôt Git local et force un push propre
#  vers github.com/grcote7/gsm sans perdre le code actuel.
#
# Activer en décommentant la ligne du push
# Lancer ainsi: ./scripts/reset_gh.ps1
#
# =====================================================================

Write-Host "=== RESET DU DEPOT GIT ===" -ForegroundColor Cyan

# Vérification que Git est installé
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  Write-Host "ERREUR: Git n'est pas installé." -ForegroundColor Red
  exit 1
}

# Vérification que l'on est bien dans un projet
if (-not (Test-Path ".git")) {
  Write-Host "ATTENTION: Aucun dossier .git trouvé. Rien à réinitialiser." -ForegroundColor Yellow
  exit 1
}

# Sauvegarde temporaire du code
$backup = "./backup_before_reset"
if (Test-Path $backup) {
  Remove-Item -Recurse -Force $backup
}
Write-Host "Sauvegarde du code dans $backup ..."
New-Item -ItemType Directory -Path $backup | Out-Null
Copy-Item -Recurse -Force * $backup

# Suppression du dépôt Git
Write-Host "Suppression du dossier .git ..."
Remove-Item -Recurse -Force .git

# Réinitialisation du dépôt
Write-Host "Réinitialisation du dépôt Git ..."
git init
git add .
git commit -m "Initial commit (reset)"

# Configuration de la branche principale
git branch -M main

# Ajout du remote GitHub
$remote = "https://github.com/grcote7/gsm.git"
Write-Host "Ajout du remote $remote ..."
git remote add origin $remote

# Push forcé
Write-Host "Push forcé vers GitHub ..."
# git push -f origin main

Write-Host ""
Write-Host "=== RESET TERMINE AVEC SUCCES ===" -ForegroundColor Green
Write-Host "Votre code est intact et le dépôt GitHub a été réinitialisé."
Write-Host "Une sauvegarde locale est disponible dans: $backup"
