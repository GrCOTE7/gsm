$initialDir = Get-Location

function Test-IgnoredCommitSubject {
    param(
        [string]$Subject
    )

    if ([string]::IsNullOrWhiteSpace($Subject)) {
        return $true
    }

    return $Subject -imatch '^(Merge( branch| remote-tracking branch| pull request)?\b|chore\(release\):\s|release:\s)'
}

function Get-EffectiveCommitSubject {
    $subjects = @(git log -20 --pretty=%s)
    if ($LASTEXITCODE -ne 0 -or $subjects.Count -eq 0) {
        return $null
    }

    foreach ($subject in $subjects) {
        $trimmedSubject = ([string]$subject).Trim()
        if (-not (Test-IgnoredCommitSubject -Subject $trimmedSubject)) {
            return $trimmedSubject
        }
    }

    return $null
}

try {
    Set-Location -Path "$PSScriptRoot"

    git rev-parse --is-inside-work-tree *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Ce dossier n'est pas un dépôt Git."
        exit 1
    }

    $branch = (git rev-parse --abbrev-ref HEAD).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -eq "HEAD") {
        Write-Error "Branche courante invalide (detached HEAD)."
        exit 1
    }

    $upstream = (git rev-parse --abbrev-ref --symbolic-full-name "@{u}" 2>$null).Trim()
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($upstream)) {
        Write-Error "Aucune branche distante configurée pour '$branch'."
        Write-Host "Exemple: git push -u origin $branch"
        exit 1
    }

    git fetch --quiet
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Échec du fetch distant. Push annulé."
        exit 1
    }

    $counts = (git rev-list --left-right --count "$upstream...HEAD").Trim()
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($counts)) {
        Write-Error "Impossible de lire l'état ahead/behind."
        exit 1
    }

    $parts = $counts -split '\s+'
    if ($parts.Count -lt 2) {
        Write-Error "Format inattendu pour l'état ahead/behind: $counts"
        exit 1
    }

    $behind = [int]$parts[0]
    $ahead = [int]$parts[1]

    if ($behind -gt 0) {
        Write-Error "La branche locale est en retard de $behind commit(s) sur $upstream."
        Write-Host "Fais un pull/rebase avant le push."
        exit 1
    }

    if ($ahead -eq 0) {
        $hasUncommittedChanges = $false

        git diff --quiet
        if ($LASTEXITCODE -eq 1) {
            $hasUncommittedChanges = $true
        }
        elseif ($LASTEXITCODE -ne 0) {
            Write-Error "Impossible de verifier les changements non commites (working tree)."
            exit 1
        }

        git diff --cached --quiet
        if ($LASTEXITCODE -eq 1) {
            $hasUncommittedChanges = $true
        }
        elseif ($LASTEXITCODE -ne 0) {
            Write-Error "Impossible de verifier les changements non commites (index)."
            exit 1
        }

        $untrackedFiles = @(git ls-files --others --exclude-standard)
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Impossible de verifier les fichiers non suivis."
            exit 1
        }

        $hasUntrackedFiles = ($untrackedFiles | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }).Count -gt 0
        if ($hasUntrackedFiles) {
            $hasUncommittedChanges = $true
        }

        if ($hasUncommittedChanges) {
            Write-Host "Veuillez commit avant de push !"
            exit 0
        }

        Write-Host "Rien a push (branche a jour avec $upstream)."
        exit 0
    }

    $lastCommitSubject = Get-EffectiveCommitSubject
    if ([string]::IsNullOrWhiteSpace($lastCommitSubject)) {
        Write-Error "Impossible de lire le dernier message de commit."
        exit 1
    }

    Write-Host "Push en cours: $branch -> $upstream"
    git push
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Push echoue."
        exit 1
    }

    if ($lastCommitSubject -imatch '^(fix|feat|upgrade)(\([^)]+\))?(!)?:') {
        $plus15 = (Get-Date).AddMinutes(15).ToString("yyyy-MM-dd HH:mm:ss")
        Write-Host "Fin de l'update max : ~ $plus15"
    }
    else {
        Write-Host "Push fait"
    }
}
finally {
    Set-Location -Path $initialDir
}
