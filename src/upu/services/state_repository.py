import json
from pathlib import Path

APP_DATA_DIR = Path(__file__).resolve().parents[1] / "app_data"
APP_BUILD_PATH = APP_DATA_DIR / "app_build.json"
APP_STATE_PATH = APP_DATA_DIR / "app_state.json"

DEFAULT_LAST_CHECK_AT = "2000-01-01 00:00"


def _load_json(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as handle:
            payload = json.load(handle)
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return {}

    if isinstance(payload, dict):
        return payload
    return {}


def _save_json(path: Path, payload: dict) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle)
    except OSError:
        return


def get_local_build_info() -> dict:
    return _load_json(APP_BUILD_PATH)


def _load_app_state() -> dict:
    return _load_json(APP_STATE_PATH)


def _save_app_state(payload: dict) -> None:
    _save_json(APP_STATE_PATH, payload)


def get_cached_release_info() -> dict[str, str | bool] | None:
    state = _load_app_state()
    payload = state.get("update.latest_release_info")
    if not isinstance(payload, dict):
        return None

    version = str(payload.get("version") or "").strip()
    if not version:
        return None

    return {
        "version": version,
        "html_url": str(payload.get("html_url") or "").strip(),
        "download_url": str(
            payload.get("download_url") or payload.get("html_url") or ""
        ).strip(),
        "published_at": str(payload.get("published_at") or "").strip(),
        "name": str(payload.get("name") or "").strip(),
        "draft": bool(payload.get("draft", False)),
        "prerelease": bool(payload.get("prerelease", False)),
    }


def save_cached_release_info(payload: dict[str, str | bool]) -> None:
    state = _load_app_state()
    state["update.latest_release_info"] = payload
    _save_app_state(state)


def get_last_check_at(default: str = DEFAULT_LAST_CHECK_AT) -> str:
    state = _load_app_state()
    value = str(state.get("latest_check_at") or "").strip()
    return value or default


def save_last_check_at(value: str) -> None:
    state = _load_app_state()
    state["latest_check_at"] = value
    _save_app_state(state)


def get_app_state_value(key: str):
    state = _load_app_state()
    return state.get(key)


def set_app_state_value(key: str, value) -> None:
    state = _load_app_state()
    state[key] = value
    _save_app_state(state)
