# <img src="src/assets/icon.png" alt="Aegis Stack" width="25"> GSM

<h3><div align='right'><span style="text-decoration:none;"><a href="./doc/0001_TOC.md" title="Table Of Content">TOC</a></span></div></h3>

---

<!-- [![CI](https://github.com/grcote7/gsm/workflows/CI/badge.svg)](https://github.com/grcote7/gsm//actions/workflows/ci.yml)
[![Documentation](https://github.com/grcote7/gsm/workflows/Deploy%20Documentation/badge.svg)](https://github.com/grcote7/gsm/actions/workflows/docs.yml) -->
[![GitHub Release](https://img.shields.io/github/v/release/GrCOTE7/gsm)](https://github.com/GrCOTE7/gsm)
[![built with Python 3.13+](https://img.shields.io/badge/built%20with-python%203.13+-blue.svg)](https://www.python.org/downloads/)
[![Built with Flet](https://img.shields.io/badge/Flet%200.85-00B0FF?style=flat-square)](https://flet.dev/)
[![Commits per Month](https://img.shields.io/github/commit-activity/m/grcote7/gsm)](https://github.com/grcote7/gsm/commits)
[![Total Commits](https://img.shields.io/github/commit-activity/t/grcote7/gsm)](https://github.com/grcote7/gsm/commits)
[![Last Commit](https://img.shields.io/github/last-commit/grcote7/gsm)](https://github.com/grcote7/gsm/commits)

![Windows](https://img.shields.io/badge/OS-Windows-0078D6?style=flat-square&logo=windows11&logoColor=white")
![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)
![Android](https://img.shields.io/badge/Android-3ddc84?logo=android&logoColor=white)
<a href="https://codespaces.new/GrCOTE7/gsm" title="Open YOUR CodeSpace Now... Click HERE!">
    <img src="https://img.shields.io/badge/GSM%20Github%20Codespace%20Ready-green.svg" alt="CodeSpace link" />
  </a>

---

<div align="center">
  <a href = "https://discord.com/channels/1056923339546968127/1507316257580519445" title="Lance la comm. et reste branché !
À un moment, quelqu'un y répondra :-) !" target="_blank">

Tu ❤️ Python...? Rejoins le chat en LIVE !

[![Discord](https://img.shields.io/discord/1056923339546968127)](https://discord.com/channels/1056923339546968127/1507316257580519445)
    </a>
</div>

---

## 🤝 Collaboration et particulièrement **adapté aux débutants**

Pour **contribuer** au dev de ce projet (Et **en connaître tous les rouages et secrets**) :

<h2 align='center'><span style="text-decoration:none;">👉 <a href="./THERA.md" title="The Doc de base"><bold>  Lire THERADOC</bold></a></span></h2>

## 🐳 → A rapid look

### 👉 Sur un Appareil Androïd (Phone ou tablette)

<div align="center">
  <a href="./doc/imgs/qr_latest.png" target="_blank">
    <img src="./doc/imgs/qr_latest.png" width='100'>
  </a>
</div>

### → [Cliquer ICI si vous êtes sur un appareil Android, mais ne pouvez pas 'flasher' ce QR Code](https://github.com/GrCOTE7/gsm/releases/download/v1.0.36/UpU.apk)

### 👉 Direct en ligne : [http://GSM.COTE7.com](http://gsm.Cote7.com)

---

## 🚀 → A rapid dev env

### 👉 En local (macOS/Linux/Windows) après le *[fork](doc/0101_GIT_FORK.md)*

Dans la *CLI* (***C***ommand ***L***ine ***I***nterface = Console), dans le dossier du projet :

```bash
./go
```

#### → C'est aussi le mode idéal pour coder avec le projet (HotReload et positionnement AUTOs de l'App)

---

### 👉 Et encore + simple et sans rien installer : Codespace → <a href="https://codespaces.new/GrCOTE7/gsm" title="Open YOUR CodeSpace Now... CTRL + Click HERE!"><img src="https://img.shields.io/badge/Dev%20GSM%20directement%20en%20ligne%20sur%20Github%20!-blue.svg" alt="CodeSpace link" /></a>

( Le clic sur ce bouton = Dans le page du dépôt ***GH*** (***G***it***H***ub) original, ou celle de votre fork, appuyer sur ' , ' - Touche virgule - pour générer ainsi un codespace) → Confirmer

Dans le terminal qui apparaîtra puis se stabilisera enfin à un moment , faire 'quasi' comme en local 😉 (Juste un 'w' en +)

```bash
./go w
```

NB : Dans un codespaces, seule la version Flet **W**eb fonctionne (D'où **cette option 'w'**), mais vous y avez tout de même non seulement hotreload opérationnel, mais aussi toutes les extensions VSCode recommandées dans GSM (Git Graph, ToDo Tree customisé, etc...)

Bref, vous pouvez ainsi simplement et "rapidement", depuis la branche de votre choix, partager son rendu 'frais' (Le + optimal et récent), y éditer du code, éventuellement coder / modifier quelque chose dedans...  Et surtout, même y faire une [P.R.](doc/0110_GIT_PR.md) !!! 😁

## 🐳 App in Docker (local)

Si Docker Desktop est installé, lancer l'app localement avec :

```bash
docker compose up -d --build
```

Le mode auto-reload est aussi actif en local Docker (watchfiles sur `src/`).
Quand tu modifies une vue Python, le process redémarre automatiquement.
Si le navigateur ne se reconnecte pas tout de suite, fais un refresh de la page.

Puis ouvrir :

```text
http://localhost:8000
```

Suivre les logs :

```bash
docker compose logs -f
```

Arrêter :

```bash
docker compose down
```

### Healthcheck

#### Fixer la page d'accueil

```bash
C:\gsm\src\gsm\config.py
# DEFAULT_ROUTE = ...
```


Vérifier l'état global du service :

```bash
docker compose ps
```

Lire le statut de santé exact du conteneur :

```bash
docker inspect gsm_app --format "health={{.State.Health.Status}}"
```

Voir le détail des derniers checks (code retour, message, date) :

```bash
docker inspect gsm_app --format "{{json .State.Health}}"
```

---

## 🏗️ Construire une app pour votre mobile GSM

Lancer le build APK pour construire l'app pour ton mobile ou tablette **Androïd** :

```bash
./apk
```

(Sinon, ouvre cette page avec ton appareil mobile et télech directement :
  **https://github.com/GrCOTE7/gsm/releases** - La der version, le lien **gsm.apk**)

## 🐍 Lancer un script Python avec HOT-RELOAD

Depuis la racine :

Exemple: \scripts\Nom_Thomas.py

### 1 - Local (Win)

```bash
uv --version
# Si échoue (Et sûr qu'uv est installé) :

$env:Path = "C:\Users\utilisateur\.local\bin;$env:Path"
uv run flet run scripts/Nom_Thomas.py

# OU (Si votre script est dans l'app ( src/ ) et python s'appelle py) :
uvx watchfiles "flet run quick_test.py" . 2>nul

# OU sans flet, simple script
uvx watchfiles "py quick_test.py" . 2>nul

```

### 2 - Distant, sans aucune installation

Juste on démarre un CodeSpace (Sur la page GH de ton fork : ' , ' (Virgule) + Create new codespace + F9

### ❌vérif si F9 OK dans un codespace pour la commande ci-dessous

Et dans la CLI (Console - Terminal) qui apparaît :

```bash
uvx watchfiles "python quick_test.py" . 2>nul
```

NB: CTRL + C dans la CLI pour arrêter le process

Si **uv** bug :

```bash
# Vérifier si uv est disponible
uv --version

# Si uv n'est pas trouvé :
curl -LsSf https://astral.sh/uv/install.sh | sh
# Ajouter uv au PATH pour la session courante
export PATH="$HOME/.local/bin:$PATH"
```

### uv - Alternative à pip + env + flet run

Outil **ultra‑rapide** et minimaliste pour installer, exécuter et gérer des environnements.

Run as a desktop app:

```bash
uv run flet run
```

Run as a web app:

Option 2 — Application Flet sur le téléphone (rendu natif identique à l'APK) ★
( Installez l'application Flet depuis le Play Store. Puis lancez en local )

```bash
uv run flet run --web -r
OU MIEUX si App flet installée dans Phone :
uv run flet run src/main.py --android
```

Avantages: rendu 100% fidèle à l'APK, hot reload, aucun build
Limite: l'app Flet doit être installée une fois sur le téléphone

Option -r => Phone: http://<IP-de-votre-PC>:8550
(Voir avec ipconfig → Carte réseau sans fil Wi-Fi : IPv4)

---

```bash
uv run flet run --web --host 0.0.0.0 --port 8550 -r
# ipconfig → IPv4 :
uv run flet run --web --host 172.21.0.1 --port 8550 -r
```

---

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
& "C:\Program Files\Java\jdk-21\bin\keytool.exe" -genkeypair -v -keystore gsm-release.keystore -alias gsm-key -keyalg RSA -keysize 2048 -validity 10000

```

ou

```bash
keytool -genkey -v -keystore gsm-release.keystore \ -alias gsm-key -keyalg RSA -keysize 2048 -validity 10000
```

ou

```bash
keytool -genkeypair -v \
  -keystore gsm-release.keystore \
  -alias gsm \
  -keyalg RSA -keysize 2048 -validity 10000
```

* 2 Encoder en base64 :

## Linux / macOS

```bash
base64 -w 0 gsm-release.keystore
```

## Windows PowerShell

```bash
[Convert]::ToBase64String([IO.File]::ReadAllBytes("gsm-release.keystore"))
```

Chemin complet car _ laisse croire à un scope

```bash
[Convert]::ToBase64String([IO.File]::ReadAllBytes("D:\_gc\aGC7\Teck\gsm-release.keystore")) > D:\_gc\aGC7\Teck\keystore.b64.txt
```

```bash
PS D:\_gc\aGC7\Teck> Get-ChildItem -Path D:\_gc -Filter gsm-release.keystore -Recurse

    Directory: D:\_gc\aGC7\Teck

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          13/05/2026    16:27           2730 gsm-release.keystore

PS D:\_gc\aGC7\Teck> 
```

* 3 Ajouter les 4 secrets dans Settings → Secrets and variables → Actions du repo

Secret                  Valeur
ANDROID_KEYSTORE_B64    le base64 du .keystore
ANDROID_STORE_PASSWORD  mot de passe du keystore
ANDROID_KEY_ALIAS       ex. gsm-key
ANDROID_KEY_PASSWORD    mot de passe de la clé (Svt mme que STORE_PW)

* [ ] Vérif la signature

C:\Users\utilisateur\AppData\Local\Android\Sdk\build-tools\34.0.0\apksigner.bat verify --print-certs gsm.apk

---

## Version utilisée

```bash
uv run python -c "import flet; print(flet.__version__)"
```

---

## Pour logs du mobile dans PC

### Debug / Iphone

.\adb logcat | Select-String "com.mycompany.gsm"

.\adb logcat | Select-String "python" | Select-String "com.mycompany.gsm"

### Debug android / PC → Android Studio

| Action                                    | Rebuild APK ? |
|-------------------------------------------|---------------|
| Modifier du Python                        | ❌ Non        |
| Modifier du Flet                          | ❌ Non        |
| Modifier la logique d’update              | ❌ Non        |
| Modifier comment tu télécharges l’APK     | ❌ Non        |
| Modifier comment tu lances l’installation | ❌ Non        |
| Ajouter un appel Android natif            | ✔️ Oui        |
| Modifier le manifest Android              | ✔️ Oui        |
| Ajouter un service Android                | ✔️ Oui        |
| Modifier le template Android de Flet      | ✔️ Oui        |

---

## .🎯 Actuels goals prioritaires

* [ ] Transformer tout le projet en mode reactif (Flutter & React-like)
* [ ] → Passage branche declarative / branche main
* [ ] Finir docs de base (✅ Git, ✅ VSC, Py, Libs, IA) + Add autres docs initiatiques
* [ ] Mettre en place dans le WorkFlow, le build pour IPhone (→ $Thera...)
* [ ] Problème de fin du process d'upgrade / mobile
* [ ] Écrire tout le projet en Anglais (Doc & commentaires)
* [x] Dernier reset complet du n° de V
