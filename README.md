# Test GC7 App

## Run the app

### Win

Éxécuter


```bash
./go
```

Lancer le build APK

```bash
./apk
```

### uv - Alternative à pip + env + flet run

Outil **ultra‑rapide** et minimaliste pour installer, exécuter et gérer des environnements.

Run as a desktop app:

```bash
uv run flet run
```

Run as a web app:

```bash
uv run flet run --web -r
OU MIEUX si App flet installée dans Phone :
uv run flet run --android
```

Option -r => Phone: http://<IP-de-votre-PC>:8550
(Voir avec ipconfig → Carte réseau sans fil Wi-Fi : IPv4)

---

Option 2 — Application Flet sur le téléphone (rendu natif identique à l'APK) ★

Installez l'application Flet depuis le Play Store. Puis lancez en local:

uv run flet run --web --host 0.0.0.0 --port 8550 -r
uv run flet run --web --host 192.168.80.205 --port 8550 -r

Avantages: rendu 100% fidèle à l'APK, hot reload, aucun build
Limite: l'app Flet doit être installée une fois sur le téléphone

Construire apk

```bash
uv run flet build apk -v
```

C:\gsm\build\flutter\android\app\build.gradle.kts

  → Vérifier val resolvedMinSdk = 24

et ajouter en fin de fichier :

// Work around AGP/Kotlin lint crashes in some Flutter plugins during release APK builds.
subprojects {
    tasks.matching {
        it.name == "lintVitalAnalyzeRelease" ||
            it.name == "lintAnalyzeRelease" ||
            it.name == "lintRelease"
    }.configureEach {
        enabled = false
    }
}

Avant :

tasks.register<Delete>("clean") {
    delete(rootProject.layout.buildDirectory)
}

* [ ] Voir la procédure exacte pour signer le fichier APK généré →  GgleStore

Pour savoir quel Py est utilisé par uv

```bash
 uv run python -c "import sys; print(sys.executable)"
```

For more details on running the app, refer to the [Getting Started Guide](https://flet.dev/docs/getting-started/).

## Build the app ONLY from C:\

### Android

```bash
uv run flet build apk -v
```

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://flet.dev/docs/publish/android/).

### iOS & macOS (Need macOS comme système hôte)

```bash
uv run flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://flet.dev/docs/publish/ios/).

```bash
uv run flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://flet.dev/docs/publish/macos/).

### Linux

```bash
uv run flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://flet.dev/docs/publish/linux/).

### Windows Pb de place

Efface les builds précédents

```bash
uv run rm -r c:\gsm\src\build\flutter\build -Force -ErrorAction SilentlyContinue
rm -r $env:LOCALAPPDATA\Temp\serious_python_* -Force -ErrorAction SilentlyContinueflet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).
