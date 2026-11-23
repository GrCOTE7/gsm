#!/usr/bin/env bash

# IMPORTANT : Sous Linux Ubuntu 26.04, exécutez au début, une fois ce script
# d'installation des dépendances :
#   sh scripts/install_flet_deps_ubuntu_26.04.sh

# Délègue tout au launcher Python (mêmes options que go.ps1 : '', w, u, gu, debug).
uv run python "$(dirname "$0")/scripts/app_window/main.py" "$@"
