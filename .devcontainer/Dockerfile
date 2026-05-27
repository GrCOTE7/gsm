FROM mcr.microsoft.com/devcontainers/python:3.11

RUN apt-get update && apt-get install -y \
    libsecret-1-0 \
    libgtk-3-0 \
    libwebkit2gtk-4.1-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
