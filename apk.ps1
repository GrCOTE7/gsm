# Se placer dans la racine du projet
Set-Location -Path "$PSScriptRoot"

# Le daemon Gradle généré par Flet demande trop de mémoire sur cette machine.
# Réduction agressieve : -Xmx1.5G pour que le compilateur Kotlin ait assez de mémoire native.
$env:GRADLE_OPTS = '-Dorg.gradle.jvmargs="-Xmx1500m -XX:MaxMetaspaceSize=512m -XX:ReservedCodeCacheSize=128m -XX:+HeapDumpOnOutOfMemoryError" -Dorg.gradle.daemon=false'

# Nettoie les artefacts Flutter intermédiaires qui peuvent casser la copie d'assets sous Windows.
$staleFlutterDirs = @(
	"$PSScriptRoot\build\flutter\build\app\intermediates\flutter\release\flutter_assets",
	"$PSScriptRoot\build\flutter\build\app\intermediates\flutter\release"
)
foreach ($dir in $staleFlutterDirs) {
	Remove-Item -Path $dir -Recurse -Force -ErrorAction SilentlyContinue
}

# Lancer explicitement le build APK de l'app
uv run flet build apk -v
