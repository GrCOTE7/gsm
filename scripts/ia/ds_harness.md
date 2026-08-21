# DeepSeek Harness

## Install

Prérequis pnpm (Si pas installé) :

```bash
node --version
pnpm --version # Si absent : npm install -g pnpm
```

### Installation (base & deps)

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
