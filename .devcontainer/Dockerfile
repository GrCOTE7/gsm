FROM mcr.microsoft.com/devcontainers/python:3.11

# Install curl first (if not already present)
RUN apt-get update && apt-get install -y \
    curl \
    libsecret-1-0 \
    libgtk-3-0 \
    libwebkit2gtk-4.1-0 \
    && rm -rf /var/lib/apt/lists/*

# Install uv (official installer)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

USER vscode
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/home/vscode/.local/bin:${PATH}"
USER root

# Upgrade pip (optional but clean)
RUN pip install --upgrade pip
