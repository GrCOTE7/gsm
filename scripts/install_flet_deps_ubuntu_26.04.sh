#!/bin/bash
# Script d'installation des dépendances Flet Desktop pour Ubuntu 26.04
# Nom : install_flet_deps_ubuntu_26.04.sf

set -e

echo "=== Installation des dépendances Flet Desktop pour Ubuntu 26.04 ==="
echo

echo "[1/4] Mise à jour des paquets..."
sudo apt update

echo
echo "[2/4] Installation des bibliothèques nécessaires..."

sudo apt install -y \
    libsecret-1-0 \
    libsecret-1-dev \
    libgtk-3-0 \
    libwebkit2gtk-4.1-0 \
    libglib2.0-0 \
    libgdk-pixbuf-2.0-0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libatk1.0-0 \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libatk-bridge2.0-0 \
    libnss3 \
    libxss1 \
    libasound2t64

echo
echo "[3/4] Nettoyage du client Flet local..."
rm -rf ~/.flet/client || true

echo
echo "[4/4] Vérification des bibliothèques manquantes..."
FLET_BIN=$(find ~/.flet -type f -name "flet" | head -n 1)

if [ -z "$FLET_BIN" ]; then
    echo "Le client Flet n'est pas encore installé. Il sera téléchargé au prochain lancement."
else
    echo "Analyse de : $FLET_BIN"
    ldd "$FLET_BIN" | grep "not found" || echo "Toutes les dépendances sont présentes."
fi

echo
echo "=== Installation terminée ==="
echo "Vous pouvez maintenant lancer Flet Desktop."
