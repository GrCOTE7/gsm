FROM mcr.microsoft.com/devcontainers/python:3.11

# Dépendances système pour Flet Web
RUN apt-get update && apt-get install -y \
    libsecret-1-0 \
    libgtk-3-0 \
    libwebkit2gtk-4.1-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installer uv (outil système)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Mettre pip à jour
RUN pip install --upgrade pip
