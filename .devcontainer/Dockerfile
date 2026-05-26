FROM mcr.microsoft.com/devcontainers/python:3.11

# Installer des dépendances système
RUN apt-get update && apt-get install -y \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

# Installer des libs Python
RUN pip install pytest flet
