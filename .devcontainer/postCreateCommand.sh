#!/bin/bash
set -e

# Installer uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Recharger le PATH
if [ -f "$HOME/.profile" ]; then
    source "$HOME/.profile"
fi

# Vérifier que uv est bien installé
if ! command -v uv >/dev/null 2>&1; then
    echo "❌ uv n'est pas disponible dans le PATH"
    exit 1
fi

# Installer les dépendances Python
uv sync


# Installer ripgrep si absent
if ! command -v rg >/dev/null 2>&1; then
    if [ "$(id -u)" -eq 0 ]; then
        apt-get update
        apt-get install -y ripgrep
    else
        sudo apt-get update
        sudo apt-get install -y ripgrep
    fi
fi

# Créer un lien vers vscode-ripgrep pour Todo Tree
if [ -x "/usr/bin/rg" ] && [ ! -e "/usr/bin/vscode-ripgrep" ]; then
    if [ "$(id -u)" -eq 0 ]; then
        ln -sf /usr/bin/rg /usr/bin/vscode-ripgrep
    else
        sudo ln -sf /usr/bin/rg /usr/bin/vscode-ripgrep
    fi
fi
# Installer ripgrep si absent
if ! command -v rg >/dev/null 2>&1; then
    if [ "$(id -u)" -eq 0 ]; then
        apt-get update
        apt-get install -y ripgrep
    else
        sudo apt-get update
        sudo apt-get install -y ripgrep
    fi
fi

# Créer un lien vers vscode-ripgrep pour Todo Tree
if [ -x "/usr/bin/rg" ] && [ ! -e "/usr/bin/vscode-ripgrep" ]; then
    if [ "$(id -u)" -eq 0 ]; then
        ln -sf /usr/bin/rg /usr/bin/vscode-ripgrep
    else
        sudo ln -sf /usr/bin/rg /usr/bin/vscode-ripgrep
    fi
fi

# # Télécharger flet-desktop-light dans le codespace
# echo "📦 Téléchargement de flet-desktop-light..."
# curl -LO https://github.com/flet-dev/flet/releases/latest/download/flet-desktop-light.zip

# # curl -L -o flet-desktop-light.zip https://github.com/flet-dev/flet/releases/download/v0.21.0/flet-desktop-light.zip
# curl -L -o flet-desktop-light.zip https://github.com/flet-dev/flet/releases/download/v0.21.0/flet-desktop-light.zip


# # Extraire dans un dossier local
# unzip -o flet-desktop-light.zip -d flet-desktop-light

# # Rendre exécutable
# chmod +x flet-desktop-light/fletd

# echo "✅ flet-desktop-light installé localement dans ./flet-desktop-light/"
# echo "➡️ Lance ton app avec : ./flet-desktop-light/fletd app.py"
