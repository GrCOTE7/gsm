"""Collecte d'informations de diagnostic (pur Python, zéro Flet).

Trois fonctions indépendantes, chacune retournant un dict structuré,
prêt à être affiché par les cards de components/diagnostic/.
"""

import json
import os, platform, socket, sys
from importlib.metadata import PackageNotFoundError, version as pkg_version
from pathlib import Path

# --- Utilitaires internes ---------------------------------------------------


def _safe_version(pkg: str) -> str:
    """Retourne la version d'un paquet ou '—' si absent."""
    try:
        return pkg_version(pkg)
    except PackageNotFoundError:
        return "—"


# app_build.json est la source de vérité du projet : c'est lui que le workflow
# de release met à jour, et lui que l'APK embarque. Les métadonnées du paquet
# `GSM`, elles, viennent du pyproject.toml installé à la construction de
# l'image — donc de la version *précédente* au moment du déploiement.
_APP_BUILD_PATH = Path(__file__).resolve().parents[1] / "app_data" / "app_build.json"


def _app_version() -> str:
    """Version de l'app depuis app_build.json, sinon métadonnées du paquet."""
    try:
        payload = json.loads(_APP_BUILD_PATH.read_text(encoding="utf-8"))
        version = str(payload.get("version") or "").strip()
        if version:
            return version
    except (OSError, ValueError, TypeError):
        pass
    return _safe_version("GSM")


def _in_docker() -> bool:
    """Détecte une exécution dans un conteneur Docker."""
    return Path("/.dockerenv").exists() or os.environ.get("RUNNING_IN_DOCKER") == "1"


# --- Fonctions publiques ----------------------------------------------------


def collect_versions() -> dict:
    """Versions Python, Flet et paquets Flet associés."""
    return {
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "venv_active": sys.prefix != sys.base_prefix,
            "executable": sys.executable,
        },
        "flet": {
            "flet": _safe_version("flet"),
            "flet-cli": _safe_version("flet-cli"),
            "flet-desktop": _safe_version("flet-desktop"),
            "flet-web": _safe_version("flet-web"),
        },
        "app": {
            "name": "GSM",
            "version": _app_version(),
        },
    }


def collect_system() -> dict:
    """Système d'exploitation, architecture, contexte Docker, PID."""
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "docker": _in_docker(),
        "hostname": socket.gethostname(),
        "pid": os.getpid(),
        "cwd": os.getcwd(),
    }


def collect_network() -> dict:
    """À venir : IP locale, interfaces, connectivité."""
    return {}
