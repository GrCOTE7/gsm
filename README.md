# <img src="src/assets/icon.png" alt="Aegis Stack" width="25"> GSM


<!-- [![CI](https://github.com/grcote7/gsm/workflows/CI/badge.svg)](https://github.com/grcote7/gsm//actions/workflows/ci.yml)
[![Documentation](https://github.com/grcote7/gsm/workflows/Deploy%20Documentation/badge.svg)](https://github.com/grcote7/gsm/actions/workflows/docs.yml) -->
[![GitHub Release](https://img.shields.io/github/v/release/GrCOTE7/gsm)](https://github.com/GrCOTE7/gsm)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Commits per Month](https://img.shields.io/github/commit-activity/m/grcote7/gsm)](https://github.com/grcote7/gsm/commits)
[![Total Commits](https://img.shields.io/github/commit-activity/t/grcote7/gsm)](https://github.com/grcote7/gsm/commits)
[![Last Commit](https://img.shields.io/github/last-commit/grcote7/gsm)](https://github.com/grcote7/gsm/commits)
![Android](https://img.shields.io/badge/Android-3ddc84?logo=android&logoColor=white)

---

<div align="center">
  <a href = "https://discord.com/channels/1056923339546968127/1507316257580519445" title="Lance la comm. et reste branché !
À un moment, quelqu'un y répondra :-) !" target="_blank">

Tu ❤️ Python...? Rejoins le chat en LIVE !

[![Discord](https://img.shields.io/discord/1056923339546968127)](https://discord.com/channels/1056923339546968127/1507316257580519445)
</a>
</div>

---

## 🤝 Collaboration

Pour **contribuer** au dev de ce projet (Et **en connaître tous les rouages et secrets**) : **Lire [THERADOC](https://github.com/GrCOTE7/gsm/blob/main/THERA.md)**

## 🚀 Run the app

### * En ligne - Sans rien n'installer !

Dans le page du dépôt (Original, ou de votre fork), appuyer sir ' , ' et générer un workspace.

Dans le terminal qui apparaît :

```bash
uv run flet run --web
    # OU, raccourci
./go
```

NB : Dans un codespace, seule la version Flet Web fonctionne (Avec l'option --web), et attention, pas de refresh, hotreload, etc... Bref, ne sert qu'à partager un rendi, voire éditer du code, ou éventuellement coder un script très simple...


### * Local - Win OS

Éxécuter :

```bash
./go
```

Lancer le build APK pour construire l'app pour ton mobile ou tablette **Androïd** :

```bash
./apk
```

(Sinon, ouvre cette page avec ton mobile et télech directement :
  **https://github.com/GrCOTE7/gsm/releases** - La der version, le lien **Upu.apk**)

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

* [x] Pour les updates, dans le workflow, procédure exacte pour signer le fichier APK généré →  GgleStore
      de toujours la même signature

Pour savoir quel Py est utilisé par uv

```bash
 uv run python -c "import sys; print(sys.executable)"
```

For more details on running the app, refer to the [Getting Started Guide](https://flet.dev/docs/getting-started/).

## 🏗️ Build the app ONLY from C:\

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

## 🎯 Actuels goals prioritaires

* [ ] Finir docs de base (Git, VSC, Py) + Add autres docs initiatiques
* [ ] Mettre en place dans le WorkFlow, le build pour IPhone (→ $Thera...)
* [ ] Problème de fin du process d'upgrade
* [x] Dernier reset complet du n° de V
