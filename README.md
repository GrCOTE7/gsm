# <img src="src/assets/icon.png" alt="Aegis Stack" width="25"> GSM


<!-- [![CI](https://github.com/grcote7/gsm/workflows/CI/badge.svg)](https://github.com/grcote7/gsm//actions/workflows/ci.yml)
[![Documentation](https://github.com/grcote7/gsm/workflows/Deploy%20Documentation/badge.svg)](https://github.com/grcote7/gsm/actions/workflows/docs.yml) -->
[![GitHub Release](https://img.shields.io/github/v/release/GrCOTE7/gsm)](https://github.com/GrCOTE7/gsm)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Commits per Month](https://img.shields.io/github/commit-activity/m/grcote7/gsm)](https://github.com/grcote7/gsm/commits)
[![Total Commits](https://img.shields.io/github/commit-activity/t/grcote7/gsm)](https://github.com/grcote7/gsm/commits)
[![Last Commit](https://img.shields.io/github/last-commit/grcote7/gsm)](https://github.com/grcote7/gsm/commits)
<svg xmlns="http://www.w3.org/2000/svg" width="71" height="20" role="img" aria-label="Android"><title>Android</title><g shape-rendering="crispEdges"><rect width="0" height="20" fill="#555"/><rect x="0" width="71" height="20" fill="#3ddc84"/></g><g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="110"><image x="5" y="3" width="14" height="14" href="data:image/svg+xml;base64,PHN2ZyBmaWxsPSIjZmZmIiByb2xlPSJpbWciIHZpZXdCb3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48dGl0bGU+QW5kcm9pZDwvdGl0bGU+PHBhdGggZD0iTTE4LjQzOTUgNS41NTg2Yy0uNjc1IDEuMTY2NC0xLjM1MiAyLjMzMTgtMi4wMjc0IDMuNDk4LS4wMzY2LS4wMTU1LS4wNzQyLS4wMjg2LS4xMTEzLS4wNDMtMS44MjQ5LS42OTU3LTMuNDg0LS44LTQuNDItLjc4Ny0xLjg1NTEuMDE4NS0zLjM1NDQuNDY0My00LjI1OTcuODIwMy0uMDg0LS4xNDk0LTEuNzUyNi0zLjAyMS0yLjAyMTUtMy40ODY0YTEuMTQ1MSAxLjE0NTEgMCAwIDAtLjE0MDYtLjE5MTRjLS4zMzEyLS4zNjQtLjkwNTQtLjQ4NTktMS4zNzktLjIwMy0uNDc1LjI4Mi0uNzEzNi45MzYxLS4zODg2IDEuNTAxOSAxLjk0NjYgMy4zNjk2LS4wOTY2LS4yMTU4IDEuOTQ3MyAzLjM1OTMuMDE3Mi4wMzEtLjQ5NDYuMjY0Mi0xLjM5MjYgMS4wMTc3QzIuODk4NyAxMi4xNzYuNDUyIDE0Ljc3MiAwIDE4Ljk5MDJoMjRjLS4xMTktMS4xMTA4LS4zNjg2LTIuMDk5LS43NDYxLTMuMDY4My0uNzQzOC0xLjkxMTgtMS44NDM1LTMuMjkyOC0yLjc0MDItNC4xODM2YTEyLjEwNDggMTIuMTA0OCAwIDAgMC0yLjEzMDktMS42ODc1Yy42NTk0LTEuMTIyIDEuMzEyLTIuMjU1OSAxLjk2NDktMy4zODQ4LjIwNzctLjM2MTUuMTg4Ni0uNzk1Ni0uMDA3OS0xLjExOTFhMS4xMDAxIDEuMTAwMSAwIDAgMC0uODUxNS0uNTMzMmMtLjUyMjUtLjA1MzYtLjkzOTIuMzEyOC0xLjA0ODguNTQ0OXptLS4wMzkxIDguNDYxYy4zOTQ0LjU5MjYuMzI0IDEuMzMwNi0uMTU2MyAxLjY1MDMtLjQ3OTkuMzE5Ny0xLjE4OC4wOTg1LTEuNTgyLS40OTQxLS4zOTQ0LS41OTI3LS4zMjQtMS4zMzA3LjE1NjMtMS42NTA0LjQ3MjctLjMxNSAxLjE4MTItLjEwODYgMS41ODIuNDk0MXpNNy4yMDcgMTMuNTI3M2MuNDgwMy4zMTk3LjU1MDYgMS4wNTc3LjE1NjMgMS42NTA0LS4zOTQuNTkyNi0xLjEwMzguODEzOC0xLjU4NC40OTQxLS40OC0uMzE5Ny0uNTUwMy0xLjA1NzctLjE1NjMtMS42NTA0LjQwMDgtLjYwMjEgMS4xMDg3LS44MTA2IDEuNTg0LS40OTQxeiIvPjwvc3ZnPg=="/><text x="445" y="140" transform="scale(.1)" fill="#fff" textLength="430">Android</text></g></svg>

## Collaboration

[Pour contribuer au dev, lire THERADOC](https://github.com/GrCOTE7/gsm/blob/main/THERA.md)

## Run the app

### Win

Éxécuter :

```bash
./go
```

Lancer le build APK :

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
uv run flet run src/main.py --android
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

### Windows

```bash
flet build windows -v
```

### Windows Pb de place

Efface les builds précédents

```bash
uv run rm -r c:\gsm\src\build\flutter\build -Force -ErrorAction SilentlyContinue
rm -r $env:LOCALAPPDATA\Temp\serious_python_* -Force -ErrorAction SilentlyContinueflet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).

---

## Structure

```bash
c:\gsm/
├── src/           ← Application active (refactorisée)
├── build/         ← Artefacts de build
├── .git/          ← Version control
├── .venv/         ← Environnement Python
├── .vscode/       ← Config VS Code
├── pyproject.toml ← Dépendances (uv)
├── README.md
├── apk.ps1        ← Build APK
└── go.ps1         ← Lanceur
```

---

Pour les mises à jour :

* Process du déclenchement des updates :
  → Mise à jour à partir des push/main → GH - releases

Semantic versioning (semantic-release): major.minor.patch

* `upgrade: description` → **major** ✔
* `feat: desc` → **minor** ✔
* `fix: desc` ou `perf: desc` → **patch** ✔

* besoin d'utiliser toujours la même clé de signature (keystore)
entre les <> versions.

* 1 Générer le keystore une seule fois (à faire localement, une seule fois) :

```bash
& "C:\Program Files\Java\jdk-21\bin\keytool.exe" -genkeypair -v -keystore upu-release.keystore -alias upu-key -keyalg RSA -keysize 2048 -validity 10000

```

ou

```bash
keytool -genkey -v -keystore upu-release.keystore \ -alias upu-key -keyalg RSA -keysize 2048 -validity 10000
```

ou

```bash
keytool -genkeypair -v \
  -keystore upu-release.keystore \
  -alias upu \
  -keyalg RSA -keysize 2048 -validity 10000
```

* 2 Encoder en base64 :

## Linux / macOS

```bash
base64 -w 0 upu-release.keystore
```

## Windows PowerShell

```bash
[Convert]::ToBase64String([IO.File]::ReadAllBytes("upu-release.keystore"))
```

Chemin complet car _ laisse croire à un scope

```bash
[Convert]::ToBase64String([IO.File]::ReadAllBytes("D:\_gc\aGC7\Teck\upu-release.keystore")) > D:\_gc\aGC7\Teck\keystore.b64.txt
```

```bash
PS D:\_gc\aGC7\Teck> Get-ChildItem -Path D:\_gc -Filter upu-release.keystore -Recurse

    Directory: D:\_gc\aGC7\Teck

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          13/05/2026    16:27           2730 upu-release.keystore

PS D:\_gc\aGC7\Teck> 
```

* 3 Ajouter les 4 secrets dans Settings → Secrets and variables → Actions du repo

Secret                  Valeur
ANDROID_KEYSTORE_B64    le base64 du .keystore
ANDROID_STORE_PASSWORD  mot de passe du keystore
ANDROID_KEY_ALIAS       ex. upu-key
ANDROID_KEY_PASSWORD    mot de passe de la clé (Svt mme que STORE_PW)

* [ ] Vérif la signature

C:\Users\utilisateur\AppData\Local\Android\Sdk\build-tools\34.0.0\apksigner.bat verify --print-certs UpU.apk

---

## ❌ Pour logs du mobile dans PC

Debug / Iphone :

.\adb logcat | Select-String "com.mycompany.upu"

.\adb logcat | Select-String "python" | Select-String "com.mycompany.upu"

❌ debug android / PC → Android Studio ?

| Action                                    | Rebuild APK ? |
|-------------------------------------------|---------------|
| Modifier du Python                        | ❌ Non         |
| Modifier du Flet                          | ❌ Non         |
| Modifier la logique d’update              | ❌ Non         |
| Modifier comment tu télécharges l’APK     | ❌ Non         |
| Modifier comment tu lances l’installation | ❌ Non         |
| Ajouter un appel Android natif            | ✔️ Oui        |
| Modifier le manifest Android              | ✔️ Oui        |
| Ajouter un service Android                | ✔️ Oui        |
| Modifier le template Android de Flet      | ✔️ Oui        |

---

Actuel goal: Problème de fin de process d'upgrade
Add theradoc
