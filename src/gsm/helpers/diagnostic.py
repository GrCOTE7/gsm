"""Collecte d'informations de diagnostic (pur Python, zéro Flet).

Trois fonctions indépendantes, chacune retournant un dict structuré,
prêt à être affiché par les cards de components/diagnostic/.
"""

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
            "version": _safe_version("GSM"),
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
