import json
import os
import re
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv
from upu.services.state_repository import (
    APP_BUILD_PATH,
    DEFAULT_LAST_CHECK_AT,
    get_cached_release_info,
    get_last_check_at,
    get_local_build_info,
    save_cached_release_info,
    save_last_check_at,
)

# Charger les variables d'environnement du fichier .env
load_dotenv()

_CHECK_TIME_FORMAT = "%Y-%m-%d %H:%M"
APP_NAME = "Up You!"

#################################################
DEFAULT_ROUTE = "/archives"  # 2ar unused
DEFAULT_ROUTE = "/react"
DEFAULT_ROUTE = "/home"
DEFAULT_ROUTE = "/tests2"
DEFAULT_ROUTE = "/tests"
DEFAULT_ROUTE = "/icons"
DEFAULT_ROUTE = "/calculator"
DEFAULT_ROUTE = "/counter"
#################################################


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


APP_BUILD = get_local_build_info()

# Build source of truth values.
VERSION = _required_str(APP_BUILD, "version")
CACHE_DELAY = _required_positive_int(APP_BUILD, "cache_delay")


def _current_check_time() -> str:
    return datetime.now().strftime(_CHECK_TIME_FORMAT)


def _parse_check_time(value: str) -> datetime | None:
    try:
        return datetime.strptime(value, _CHECK_TIME_FORMAT)
    except ValueError:
        return None


def _cache_delay_from_build() -> int:
    payload = get_local_build_info()
    raw_value = payload.get("cache_delay")
    if raw_value is None:
        return CACHE_DELAY

    try:
        value = int(str(raw_value).strip())
    except (TypeError, ValueError):
        return CACHE_DELAY

    return value if value > 0 else CACHE_DELAY


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

    last_check = _parse_check_time(get_last_check_at(DEFAULT_LAST_CHECK_AT))
    if last_check is None:
        return False

    elapsed_seconds = (datetime.now() - last_check).total_seconds()
    return elapsed_seconds < _cache_delay_from_build()


def _env_int(name: str, default: int = 0) -> int:
    raw = str(os.getenv(name, str(default)) or "").strip()

    if not raw:
        return default

    # Tolère les valeurs de type "1526 # commentaire" dans .env.
    raw = raw.split("#", 1)[0].strip()
    match = re.search(r"[-+]?\d+", raw)
    if not match:
        return default

    try:
        return int(match.group(0))
    except (TypeError, ValueError):
        return default


WINDOW_LEFT = _env_int(name="UPU_WINDOW_LEFT", default=1412)  # 1526 - 1912
DEBUG_RELEASE_JSON = _env_int("UPU_DEBUG_RELEASE_JSON", 0) == 1
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
    cached_release = get_cached_release_info()
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
            raw_payload = response.read().decode("utf-8")
            payload = json.loads(raw_payload)
            if DEBUG_RELEASE_JSON:
                print("[update-debug] github latest release payload:")
                print(json.dumps(payload, indent=2))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        save_last_check_at(_current_check_time())
        release_info = cached_release or _fallback_release_info()
        save_cached_release_info(release_info)
        return release_info

    tag = str(payload.get("tag_name") or "").strip()
    if not tag:
        save_last_check_at(_current_check_time())
        release_info = cached_release or _fallback_release_info()
        save_cached_release_info(release_info)
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

    save_cached_release_info(release_info)
    save_last_check_at(_current_check_time())
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
