import json
import os
import re
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

# Charger les variables d'environnement du fichier .env
load_dotenv()

APP_DATA_DIR = Path(__file__).resolve().parent / "app_data"
APP_BUILD_PATH = APP_DATA_DIR / "app_build.json"
APP_STATE_PATH = APP_DATA_DIR / "app_state.json"
_CHECK_TIME_FORMAT = "%Y-%m-%d %H:%M"

# print("config.py importé")


def _load_app_build() -> dict:
    try:
        with APP_BUILD_PATH.open(encoding="utf-8") as build_file:
            payload = json.load(build_file)
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return {}

    if isinstance(payload, dict):
        return payload
    return {}


def _required_str(payload: dict, key: str) -> str:
    value = str(payload.get(key) or "").strip()
    if not value:
        raise RuntimeError(f"Missing required key '{key}' in {APP_BUILD_PATH}")
    return value


def _required_positive_int(payload: dict, key: str) -> int:
    raw_value = payload.get(key)
    if raw_value is None:
        raise RuntimeError(f"Missing required key '{key}' in {APP_BUILD_PATH}")

    try:
        value = int(str(raw_value).strip())
    except (TypeError, ValueError):
        raise RuntimeError(f"Invalid required key '{key}' in {APP_BUILD_PATH}")

    if value <= 0:
        raise RuntimeError(f"Required key '{key}' must be > 0 in {APP_BUILD_PATH}")

    return value


APP_BUILD = _load_app_build()

# Build source of truth values.
VERSION = _required_str(APP_BUILD, "version")
LATEST_CHECK_AT = "2000-01-01 00:00"  # fallback: force check au premier lancement
CACHE_DELAY = _required_positive_int(APP_BUILD, "cache_delay")


def save_app_build_latest_check_at(value: str) -> None:
    state = _load_app_state()
    state["latest_check_at"] = value
    _save_app_state(state)


def _load_app_state() -> dict:
    try:
        with APP_STATE_PATH.open(encoding="utf-8") as state_file:
            payload = json.load(state_file)
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return {}

    if isinstance(payload, dict):
        return payload
    return {}


def _save_app_state(payload: dict) -> None:
    try:
        APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
        with APP_STATE_PATH.open("w", encoding="utf-8") as state_file:
            json.dump(payload, state_file)
    except OSError:
        return


def _current_check_time() -> str:
    return datetime.now().strftime(_CHECK_TIME_FORMAT)


def _parse_check_time(value: str) -> datetime | None:
    try:
        return datetime.strptime(value, _CHECK_TIME_FORMAT)
    except ValueError:
        return None


def _latest_check_at_from_build() -> str:
    state = _load_app_state()
    value = str(state.get("latest_check_at") or "").strip()
    return value or LATEST_CHECK_AT


def _cache_delay_from_build() -> int:
    payload = _load_app_build()
    raw_value = payload.get("cache_delay")
    if raw_value is None:
        return CACHE_DELAY

    try:
        value = int(str(raw_value).strip())
    except (TypeError, ValueError):
        return CACHE_DELAY

    return value if value > 0 else CACHE_DELAY


def get_app_build_latest_check_at() -> str:
    return _latest_check_at_from_build()


def _cached_release_info_from_state() -> dict[str, str | bool] | None:
    state = _load_app_state()
    payload = state.get("update.latest_release_info")
    if not isinstance(payload, dict):
        return None

    version = str(payload.get("version") or "").strip()
    if not version:
        return None

    return {
        "version": version,
        "html_url": str(payload.get("html_url") or GITHUB_LATEST_RELEASE_PAGE).strip(),
        "download_url": str(
            payload.get("download_url")
            or payload.get("html_url")
            or GITHUB_LATEST_RELEASE_PAGE
        ).strip(),
        "published_at": str(payload.get("published_at") or "").strip(),
        "name": str(payload.get("name") or "").strip(),
        "draft": bool(payload.get("draft", False)),
        "prerelease": bool(payload.get("prerelease", False)),
    }


def _save_cached_release_info(payload: dict[str, str | bool]) -> None:
    state = _load_app_state()
    state["update.latest_release_info"] = payload
    _save_app_state(state)


def _fallback_release_info() -> dict[str, str | bool]:
    return {
        "version": VERSION,
        "html_url": GITHUB_LATEST_RELEASE_PAGE,
        "download_url": GITHUB_LATEST_RELEASE_PAGE,
        "published_at": "",
        "name": "",
        "draft": False,
        "prerelease": False,
    }


def _should_use_cached_release(cached: dict[str, str | bool] | None) -> bool:
    if cached is None:
        return False

    last_check = _parse_check_time(_latest_check_at_from_build())
    if last_check is None:
        return False

    elapsed_seconds = (datetime.now() - last_check).total_seconds()
    return elapsed_seconds < _cache_delay_from_build()


def _env_int(name: str, default: int = 0) -> int:
    raw = str(os.getenv(name, str(default)) or "").strip()
    if not raw:
        return default

    # Tolere les valeurs de type "1526 # commentaire" dans .env.
    raw = raw.split("#", 1)[0].strip()
    match = re.search(r"[-+]?\d+", raw)
    if not match:
        return default

    try:
        return int(match.group(0))
    except (TypeError, ValueError):
        return default


APP_NAME = "Up You!"
DEFAULT_ROUTE = "/tests"
WINDOW_LEFT = _env_int("UPU_WINDOW_LEFT", 0)  # 1526 - 1912
print(f"{WINDOW_LEFT=}")
GITHUB_OWNER = "GrCOTE7"
GITHUB_REPO = "gsm"
GITHUB_LATEST_RELEASE_API = (
    f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
)
GITHUB_LATEST_RELEASE_PAGE = (
    f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
)


def _normalize_version(version: str) -> str:
    return version.strip().removeprefix("v").removeprefix("V")


def _pick_apk_download_url(assets: list[dict]) -> str:
    apk_assets = [
        asset for asset in assets if str(asset.get("name", "")).endswith(".apk")
    ]
    if not apk_assets:
        return ""

    preferred_patterns = ("arm64-v8a", "universal")
    for pattern in preferred_patterns:
        for asset in apk_assets:
            name = str(asset.get("name") or "").lower()
            if pattern in name:
                return str(asset.get("browser_download_url") or "").strip()

    return str(apk_assets[0].get("browser_download_url") or "").strip()


def get_latest_release_info(
    timeout_seconds: int = 5, allow_remote: bool = True
) -> dict[str, str | bool]:
    """Return latest GitHub release metadata with persistent cache throttling."""
    cached_release = _cached_release_info_from_state()
    if cached_release is not None and _should_use_cached_release(cached_release):
        return cached_release

    if not allow_remote:
        if cached_release is not None:
            return cached_release
        return _fallback_release_info()

    request = Request(
        GITHUB_LATEST_RELEASE_API,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "upu-version-check",
        },
    )

    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        save_app_build_latest_check_at(_current_check_time())
        release_info = cached_release or _fallback_release_info()
        _save_cached_release_info(release_info)
        return release_info

    tag = str(payload.get("tag_name") or "").strip()
    if not tag:
        save_app_build_latest_check_at(_current_check_time())
        release_info = cached_release or _fallback_release_info()
        _save_cached_release_info(release_info)
        return release_info

    html_url = str(payload.get("html_url") or GITHUB_LATEST_RELEASE_PAGE).strip()
    assets = payload.get("assets") or []
    download_url = _pick_apk_download_url(assets if isinstance(assets, list) else [])

    release_info = {
        "version": _normalize_version(tag),
        "html_url": html_url,
        "download_url": download_url or html_url,
        "published_at": str(payload.get("published_at") or "").strip(),
        "name": str(payload.get("name") or "").strip(),
        "draft": bool(payload.get("draft", False)),
        "prerelease": bool(payload.get("prerelease", False)),
    }

    _save_cached_release_info(release_info)
    save_app_build_latest_check_at(_current_check_time())
    return release_info


def get_latest_stable_version(
    timeout_seconds: int = 5, allow_remote: bool = True
) -> str:
    """Return latest stable version from GitHub Releases, fallback to local VERSION."""
    return str(
        get_latest_release_info(timeout_seconds, allow_remote=allow_remote).get(
            "version"
        )
        or VERSION
    )


def _version_tuple(version: str) -> tuple[int, ...]:
    cleaned = _normalize_version(version)
    parts = re.findall(r"\d+", cleaned)
    return tuple(int(p) for p in parts) if parts else (0,)


def is_update_available(
    current_version: str = VERSION, allow_remote: bool = True
) -> bool:
    """True when a newer stable GitHub release exists."""
    latest = str(
        get_latest_release_info(allow_remote=allow_remote).get("version") or VERSION
    )
    return _version_tuple(latest) > _version_tuple(current_version)
