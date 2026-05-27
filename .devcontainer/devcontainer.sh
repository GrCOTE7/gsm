#!/bin/bash

# Installer uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Recharger le PATH
source ~/.profile

# Installer les dépendances Python
uv sync
