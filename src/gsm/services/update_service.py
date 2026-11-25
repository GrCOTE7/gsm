"""Détection des mises à jour GitHub pour l'application GSM.

L'app compare la version embarquée dans son bundle
(`gsm/app_data/app_build.json`, réécrite par le workflow de release) à la
dernière release stable publiée sur GitHub.

Le résultat est mémorisé pour la durée du processus : un seul appel réseau par
lancement, quel que soit le nombre de rendus de la page d'accueil.
"""

import json
import re
from pathlib import Path
from typing import Any

from upu.config import GITHUB_LATEST_RELEASE_PAGE, get_latest_release_info

_APP_BUILD_PATH = Path(__file__).resolve().parents[1] / "app_data" / "app_build.json"
_DEFAULT_TIMEOUT_SECONDS = 2

_cached_info: dict[str, Any] | None = None


def local_version() -> str:
    """Version embarquée dans cet APK/exécutable (source : app_build.json)."""
    try:
        payload = json.loads(_APP_BUILD_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""

    if not isinstance(payload, dict):
        return ""

    return str(payload.get("version") or "").strip()


def _version_tuple(version: str) -> tuple[int, ...]:
    parts = re.findall(r"\d+", str(version))
    return tuple(int(part) for part in parts) if parts else (0,)


def get_update_info(
    timeout_seconds: int = _DEFAULT_TIMEOUT_SECONDS,
    force: bool = False,
) -> dict[str, Any]:
    """Version locale, dernière version GitHub et état de mise à jour.

    `force=True` ignore le cache mémoire (utile aux tests et à un rafraîchissement
    explicite). Une erreur réseau ne remonte jamais : on retombe simplement sur
    « pas de mise à jour connue ».
    """
    global _cached_info

    if _cached_info is not None and not force:
        return _cached_info

    local = local_version()

    try:
        release = get_latest_release_info(
            timeout_seconds=timeout_seconds, allow_remote=True
        )
    except Exception:  # noqa: BLE001 - ne doit jamais casser l'affichage
        release = {}

    latest = str(release.get("version") or "").strip()

    info = {
        "local_version": local,
        "latest_version": latest or local,
        "html_url": str(release.get("html_url") or GITHUB_LATEST_RELEASE_PAGE).strip(),
        "download_url": str(release.get("download_url") or "").strip(),
        # Comparaison numérique (1.1.10 > 1.1.9), jamais lexicale.
        "update_available": bool(local)
        and bool(latest)
        and _version_tuple(latest) > _version_tuple(local),
    }
    _cached_info = info
    return info
