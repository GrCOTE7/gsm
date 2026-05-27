FROM mcr.microsoft.com/devcontainers/python:3.11

# Installer les dépendances système nécessaires à Flet Desktop/Web
RUN apt-get update && apt-get install -y \
    libsecret-1-0 \
    libgtk-3-0 \
    libwebkit2gtk-4.0-37 \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python globales (optionnel)
RUN pip install --upgrade pip
