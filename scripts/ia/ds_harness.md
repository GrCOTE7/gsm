# DeepSeek Harness

## Run

```bash
pnpm dsh web

# Si pas besoin du browse :
pnpm dsh web --no-open
```

## Install

Prérequis pnpm (Si pas installé) :

```bash
node --version
pnpm --version # Si absent : npm install -g pnpm
```

### Installation (base & deps)

⚠️ Problème perso : D: (FAT 32) et E: (foutu) incompatibles.

Attention: Si nécessité d'alléger le C: voir ci-après.

```bash
D:
# mkdir ai   # seulement s'il n'existe pas
cd ai
git clone https://github.com/GrCOTE7/deepseek-harness.git dsh
cd dsh
pnpm install
# ou npm install
```

### Configuration

#### Crée un fichier .env à la racine (ou utilise la méthode indiquée dans le README)

```env
DEEPSEEK_API_KEY=sk-...
DEEPSEEK_BASE_URL=http://localhost:3000/v1 # Usage du proxy (→ Thinkless)
```

## RUN

```bash
pnpm run example
# OU
node examples/basic-agent.js
```

Looker dans : node examples/basic-agent.js

## Usage du D: de préférence (Économie du C:)

Confirmation de l'empl actuel :

```bash
pnpm store path
```

### Déplacement du store et du cache

```bash
pnpm config set store-dir D:\node\pnpm-store
npm config set cache D:\node\npm-cache
```

Sur C:

| Outil | Cache / Store           | Emplacement                                  |
| ----- | ----------------------- | -------------------------------------------- |
| npm   | cache HTTP + paquets    | %LocalAppData%\npm-cache                     |
| pnpm  | store global de paquets | %LocalAppData%\pnpm\store (ou ~/.pnpm-store) |

→ Nettoyage

```bash
Remove-Item -Recurse -Force "C:\Users\utilisateur\AppData\Local\pnpm\store"
npm cache clean --force
```

> ⚠️ Les anciens projets nécessiteront `pnpm install`

---

TIPS :


node --import tsx/esm --expose-internals apps/cli/src/bin.ts --profile headless "say hello and report that your tool ran"
→ OK

pnpm dsh --profile headless "say hello and report that your tool ran" 
→ OK

---

.\run-demo.bat :


@echo off
rem Demo: run the headless one-shot agent against the local mock LLM (source mode).
set DEEPSEEK_API_KEY=demo-key
set DEEPSEEK_BASE_URL=http://127.0.0.1:3080/v1
call pnpm.cmd dsh --profile headless "say hello and report that your tool ran"
echo EXITCODE=%ERRORLEVEL%

---

effectuer un bilan de santé complet de votre environnement dsh :
npx github:ciceroyang/dsh-doctor

---

afficher sa configuration finale, qui est le résultat de l'application de tous vos profils, patches et variables d'environnement :

dsh --profile headless --dump-config

echo $DEEPSEEK_BASE_URL
echo $DEEPSEEK_API_KEY