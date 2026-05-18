# Se placer dans la racine du projet
Set-Location -Path "$PSScriptRoot"

# Vérifie silencieusement l'alignement des versions; message orange uniquement en cas d'écart.
& "$PSScriptRoot\scripts\check_version_sync.ps1"

# Le daemon Gradle généré par Flet demande trop de mémoire sur cette machine.
# Réduction agressive : -Xmx1.5G pour que le compilateur Kotlin ait assez de mémoire native.
$env:GRADLE_OPTS = '-Dorg.gradle.jvmargs="-Xmx1500m -XX:MaxMetaspaceSize=512m -XX:ReservedCodeCacheSize=128m -XX:+HeapDumpOnOutOfMemoryError" -Dorg.gradle.daemon=false'

# Nettoie les artefacts Flutter intermédiaires qui peuvent casser la copie d'assets sous Windows.
$staleFlutterDirs = @(
	"$PSScriptRoot\build\flutter\build\app\intermediates\flutter\release\flutter_assets",
	"$PSScriptRoot\build\flutter\build\app\intermediates\flutter\release"
)
foreach ($dir in $staleFlutterDirs) {
	Remove-Item -Path $dir -Recurse -Force -ErrorAction SilentlyContinue
}

# Évite de conserver des APK précédents (split/universal) qui prêtent à confusion.
Remove-Item -Path "$PSScriptRoot\build\apk\*.apk" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$PSScriptRoot\build\apk\*.apk.sha1" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$PSScriptRoot\build\flutter\build\app\outputs\flutter-apk\*.apk" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$PSScriptRoot\build\flutter\build\app\outputs\flutter-apk\*.apk.sha1" -Force -ErrorAction SilentlyContinue

# Lancer explicitement le build APK de l'app
uv run --active python -m flet.cli build apk -v
