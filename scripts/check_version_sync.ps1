$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$pyprojectPath = Join-Path $projectRoot "pyproject.toml"
$appBuildPath = Join-Path $projectRoot "src\upu\app_data\app_build.json"

if (-not (Test-Path -Path $pyprojectPath) -or -not (Test-Path -Path $appBuildPath)) {
  return
}

$pyprojectContent = Get-Content -Path $pyprojectPath -Raw -Encoding UTF8
$appBuildContent = Get-Content -Path $appBuildPath -Raw -Encoding UTF8

$projectSectionMatch = [regex]::Match(
  $pyprojectContent,
  '(?ms)^\[project\]\s*(?<body>.*?)(^\[|\z)'
)

$pyprojectVersion = ""
if ($projectSectionMatch.Success) {
  $projectBody = $projectSectionMatch.Groups["body"].Value
  $pyprojectVersionMatch = [regex]::Match(
    $projectBody,
    '(?m)^\s*version\s*=\s*"(?<version>[^"]+)"'
  )
  if ($pyprojectVersionMatch.Success) {
    $pyprojectVersion = $pyprojectVersionMatch.Groups["version"].Value.Trim()
  }
}

$appBuildVersion = ""
try {
  $appBuild = $appBuildContent | ConvertFrom-Json -AsHashtable
  if ($null -ne $appBuild -and $appBuild.ContainsKey("version")) {
    $appBuildVersion = [string]$appBuild["version"]
    $appBuildVersion = $appBuildVersion.Trim()
  }
}
catch {
  # Keep script non-blocking for local run helpers.
}

if ([string]::IsNullOrWhiteSpace($pyprojectVersion) -or [string]::IsNullOrWhiteSpace($appBuildVersion)) {
  Write-Host "[version-check] Impossible de lire les versions (pyproject/app_build)." -ForegroundColor DarkYellow
  return
}

if ($pyprojectVersion -ne $appBuildVersion) {
  Write-Host "[version-check] Version mismatch: pyproject.toml=$pyprojectVersion ; src/upu/app_data/app_build.json=$appBuildVersion" -ForegroundColor DarkYellow
}
