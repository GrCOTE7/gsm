"""Service d'ouverture du lien de mise à jour (page GitHub Release).

Contrat défini par tests/test_release_service.py :
- throttle d'une ouverture par heure, persistant entre redémarrages,
- normalisation desktop : URL "download" -> page "tag" du release,
- mobile Android : URL .apk -> intent:// PackageInstaller,
- ordre d'ouverture : page.launch_url(...) -> page.open(ft.Url(...))
  -> webbrowser.open(...), avec journalisation dans update_flow.log.
"""

import json
import re
import time
import webbrowser
from pathlib import Path
from urllib.parse import urlparse

_DATA_DIR = Path(__file__).resolve().parents[1] / "app_data"
_APP_STATE_PATH = _DATA_DIR / "app_state.json"
_UPDATE_LOG_PATH = _DATA_DIR / "update_flow.log"

_COOLDOWN_SECONDS = 3600.0
_last_open_release_url_at: float | None = None


def _current_timestamp() -> float:
    """Horloge (mockable) — time.time() en production."""
    return time.time()


# ---------------------------------------------------------------------------
# Journalisation
# ---------------------------------------------------------------------------


def _log(message: str) -> None:
    try:
        _UPDATE_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(_UPDATE_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"{_current_timestamp():.0f} {message}\n")
    except OSError:
        pass


# ---------------------------------------------------------------------------
# État persistant (throttle entre redémarrages)
# ---------------------------------------------------------------------------


def _load_last_open() -> float | None:
    try:
        data = json.loads(_APP_STATE_PATH.read_text(encoding="utf-8"))
        return float(data["last_open_release_url_at"])
    except Exception:
        return None


def _save_last_open(timestamp: float) -> None:
    try:
        _APP_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        _APP_STATE_PATH.write_text(
            json.dumps({"last_open_release_url_at": timestamp}), encoding="utf-8"
        )
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Normalisations d'URL
# ---------------------------------------------------------------------------


def _normalize_desktop_release_url(url: str) -> str:
    """Desktop : l'URL "download" redirige vers la page "tag" du release."""
    match = re.match(r"^(https?://[^/]+/.+?/releases)/download/([^/]+)/", url)
    if match:
        return f"{match.group(1)}/tag/{match.group(2)}"
    return url


def _transform_url_to_android_install_intent(url: str) -> str:
    """Mobile Android : URL .apk -> intent:// pour forcer PackageInstaller."""
    parsed = urlparse(url)
    if not parsed.path.lower().endswith(".apk"):
        return url
    host_path = f"{parsed.netloc}{parsed.path}"
    if parsed.query:
        host_path += f"?{parsed.query}"
    return (
        f"intent://{host_path}#Intent;"
        f"scheme={parsed.scheme or 'https'};"
        f"type=application/vnd.android.package-archive;"
        f"end"
    )


# ---------------------------------------------------------------------------
# Ouverture effective
# ---------------------------------------------------------------------------


def _is_mobile_page(page) -> bool:
    platform = getattr(page, "platform", None)
    if platform is None:
        return False
    is_mobile = getattr(platform, "is_mobile", None)
    if callable(is_mobile):
        return bool(is_mobile())
    return getattr(platform, "name", str(platform)).lower() in ("android", "ios")


def _url_control(url: str):
    """Contrôle Flet ft.Url (fallback page.open) — importé paresseusement."""
    import flet as ft

    return ft.Url(url)


def open_release_url(page, url, force: bool = False) -> bool:
    """Ouvre l'URL de release, au plus une fois par heure (sauf force=True).

    Ordre d'ouverture :
    1. page.run_task(page.launch_url(...)) si disponible (desktop/mobile),
    2. page.open(ft.Url(...)),
    3. webbrowser.open(...) en dernier recours.
    """
    global _last_open_release_url_at

    now = _current_timestamp()

    # Throttle : 1 ouverture / heure, persistant entre redémarrages.
    if not force:
        if _last_open_release_url_at is None:
            _last_open_release_url_at = _load_last_open()
        if (
            _last_open_release_url_at is not None
            and now - _last_open_release_url_at < _COOLDOWN_SECONDS
        ):
            _log(f"open_release_url cooldown {url}")
            return False

    target = _normalize_desktop_release_url(url)
    if _is_mobile_page(page) and target.lower().endswith(".apk"):
        target = _transform_url_to_android_install_intent(target)

    try:
        if page is not None and hasattr(page, "run_task") and hasattr(page, "launch_url"):
            page.run_task(page.launch_url(target))
        elif page is not None and hasattr(page, "open"):
            page.open(_url_control(target))
        else:
            webbrowser.open(target)
    except Exception as exc:  # noqa: BLE001
        _log(f"open_release_url error {url}: {exc}")
        return False

    _last_open_release_url_at = now
    _save_last_open(now)
    _log(f"open_release_url ok {target}")
    return True
