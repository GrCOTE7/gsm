import json
import traceback
from pathlib import Path
from urllib.parse import urlparse
import time
import webbrowser

import flet as ft
from upu.config import CACHE_DELAY

_DATA_DIR = Path(__file__).resolve().parents[1] / "app_data"
_APP_STATE_PATH = _DATA_DIR / "app_state.json"
_LEGACY_RELEASE_STATE_PATH = _DATA_DIR / "release_state.json"
_UPDATE_LOG_PATH = _DATA_DIR / "update_flow.log"
_OPEN_RELEASE_URL_COOLDOWN_SECONDS = float(CACHE_DELAY)
_last_open_release_url_at: float | None = None


def _current_timestamp() -> float:
    return time.time()


def _log_update_event(message: str) -> None:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(_current_timestamp()))
    line = f"[{timestamp}] {message}\n"
    print(line.strip())
    try:
        _DATA_DIR.mkdir(parents=True, exist_ok=True)
        with _UPDATE_LOG_PATH.open("a", encoding="utf-8") as log_file:
            log_file.write(line)
    except OSError:
        return


def get_update_log_path() -> Path:
    return _UPDATE_LOG_PATH


def _load_state(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as state_file:
            payload = json.load(state_file)
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return {}

    if isinstance(payload, dict):
        return payload
    return {}


def _load_app_state() -> dict:
    state = _load_state(_APP_STATE_PATH)
    if state:
        return state
    return _load_state(_LEGACY_RELEASE_STATE_PATH)


def _load_last_open_release_url_at() -> float | None:
    payload = _load_app_state()

    stored_value = payload.get("last_open_release_url_at")
    if stored_value is None:
        return None

    try:
        return float(stored_value)
    except (TypeError, ValueError):
        return None


def _save_last_open_release_url_at(timestamp: float) -> None:
    state = _load_app_state()
    state["last_open_release_url_at"] = timestamp

    try:
        _DATA_DIR.mkdir(parents=True, exist_ok=True)
        with _APP_STATE_PATH.open("w", encoding="utf-8") as state_file:
            json.dump(state, state_file)
    except OSError:
        return


def _can_open_release_url(now: float | None = None) -> bool:
    global _last_open_release_url_at

    current_time = _current_timestamp() if now is None else now

    if _last_open_release_url_at is None:
        _last_open_release_url_at = _load_last_open_release_url_at()

    if _last_open_release_url_at is None:
        return True

    return current_time - _last_open_release_url_at > _OPEN_RELEASE_URL_COOLDOWN_SECONDS


def _is_mobile_platform(page: ft.Page | None) -> bool:
    """Detecte si la plateforme est Android ou iOS."""
    if page is None:
        return False

    platform = getattr(page, "platform", None)
    if platform is None:
        return False

    is_mobile = getattr(platform, "is_mobile", None)
    if callable(is_mobile):
        return bool(is_mobile())

    platform_name = getattr(platform, "name", str(platform)).lower()
    return platform_name in {"android", "ios"}


def _transform_url_to_android_install_intent(url: str) -> str:
    """
    Transforme une URL HTTP vers APK en intent:// qui force PackageInstaller.
    Format: intent://https/github.com/...#Intent;scheme=https;action=android.intent.action.VIEW;type=application/vnd.android.package-archive;end
    Retourne l'URL inchangée si elle n'est pas un APK.
    """
    if not url.startswith("http"):
        return url

    # Vérifier que c'est un APK
    if not url.lower().endswith(".apk"):
        return url

    # Enlever le scheme http(s)://
    url_without_scheme = url.replace("https://", "").replace("http://", "")

    return f"intent://{url_without_scheme}#Intent;scheme=https;action=android.intent.action.VIEW;type=application/vnd.android.package-archive;end"


def _normalize_desktop_release_url(url: str) -> str:
    """Convertit un lien GitHub releases/download vers releases/tag sur desktop."""
    try:
        parsed = urlparse(url)
    except Exception:
        return url

    host = (parsed.netloc or "").lower()
    path = parsed.path or ""
    if host not in {"github.com", "www.github.com"}:
        return url

    marker = "/releases/download/"
    if marker not in path:
        return url

    prefix, tail = path.split(marker, 1)
    version = tail.split("/", 1)[0].strip()
    if not version:
        return url

    return f"https://github.com{prefix}/releases/tag/{version}"


def open_release_url(page: ft.Page | None, url: str, *, force: bool = False) -> bool:
    global _last_open_release_url_at

    if not url:
        _log_update_event("open_release_url: URL vide, abandon")
        return False

    if not force and not _can_open_release_url():
        _log_update_event("open_release_url: bloque par cooldown")
        return False

    _last_open_release_url_at = _current_timestamp()
    _save_last_open_release_url_at(_last_open_release_url_at)
    _log_update_event(
        f"open_release_url: start url={url}, force={force}, mobile={_is_mobile_platform(page)}"
    )

    is_mobile = _is_mobile_platform(page)

    # Sur desktop, l'ouverture directe via navigateur systeme est la plus fiable.
    if not is_mobile:
        desktop_url = _normalize_desktop_release_url(url)
        if desktop_url != url:
            _log_update_event(
                f"open_release_url: desktop normalized url={desktop_url} from={url}"
            )

        _log_update_event("open_release_url: desktop usage webbrowser.open")
        try:
            opened = webbrowser.open(desktop_url)
            _log_update_event(
                f"open_release_url: webbrowser.open retourne {opened} target={desktop_url}"
            )
            if opened:
                return True

            if desktop_url != url:
                _log_update_event(
                    f"open_release_url: desktop fallback original url={url}"
                )
                fallback_opened = webbrowser.open(url)
                _log_update_event(
                    "open_release_url: webbrowser.open fallback "
                    f"retourne {fallback_opened} target={url}"
                )
                if fallback_opened:
                    return True
        except Exception as exc:
            _log_update_event(
                f"open_release_url: webbrowser.open echec error={exc.__class__.__name__}: {exc}"
            )
            _log_update_event(traceback.format_exc())

        if page is not None and hasattr(page, "launch_url"):

            async def _open_desktop_url() -> None:
                try:
                    _log_update_event(
                        f"launch_url: desktop tentative target={desktop_url}"
                    )
                    await page.launch_url(desktop_url)
                    _log_update_event("launch_url: desktop tentative OK")
                    return
                except Exception as exc:
                    _log_update_event(
                        "launch_url: desktop echec "
                        f"target={desktop_url}, error={exc.__class__.__name__}: {exc}"
                    )
                    _log_update_event(traceback.format_exc())

                if desktop_url != url:
                    try:
                        _log_update_event(f"launch_url: desktop fallback url={url}")
                        await page.launch_url(url)
                        _log_update_event("launch_url: desktop fallback OK")
                        return
                    except Exception as exc:
                        _log_update_event(
                            "launch_url: desktop fallback echec "
                            f"error={exc.__class__.__name__}: {exc}"
                        )
                        _log_update_event(traceback.format_exc())

            try:
                _log_update_event("open_release_url: desktop run_task(launch_url)")
                page.run_task(_open_desktop_url)
                return True
            except Exception as exc:
                _log_update_event(
                    f"open_release_url: desktop run_task echec error={exc.__class__.__name__}: {exc}"
                )
                _log_update_event(traceback.format_exc())

        return False

    if page is not None:
        if hasattr(page, "launch_url") and is_mobile:

            async def _open_with_launch_url() -> None:
                # Sur Android/iOS, forcer l'ouverture d'un app non-browser pour APK
                # plutôt que le navigateur qui déclencherait un téléchargement
                target_url = url
                try:
                    _log_update_event(f"launch_url: tentative target={target_url}")
                    await page.launch_url(target_url)
                    _log_update_event("launch_url: tentative OK")
                    return
                except Exception as exc:
                    _log_update_event(
                        f"launch_url: echec target={target_url}, error={exc.__class__.__name__}: {exc}"
                    )
                    _log_update_event(traceback.format_exc())

                if is_mobile and url.lower().endswith(".apk"):
                    # Fallback Android: transformer en intent qui force PackageInstaller.
                    intent_target = _transform_url_to_android_install_intent(url)
                    try:
                        _log_update_event(
                            f"launch_url: fallback intent target={intent_target}"
                        )
                        await page.launch_url(intent_target)
                        _log_update_event("launch_url: fallback intent OK")
                        return
                    except Exception as exc:
                        _log_update_event(
                            "launch_url: fallback intent echec "
                            f"error={exc.__class__.__name__}: {exc}"
                        )
                        _log_update_event(traceback.format_exc())

                _log_update_event("launch_url: aucun fallback disponible")

            try:
                _log_update_event("open_release_url: run_task(launch_url) mobile")
                page.run_task(_open_with_launch_url)
                return True
            except Exception as exc:
                _log_update_event(
                    f"open_release_url: run_task echec error={exc.__class__.__name__}: {exc}"
                )
                _log_update_event(traceback.format_exc())

    _log_update_event("open_release_url: usage webbrowser.open")
    try:
        opened = webbrowser.open(url)
        _log_update_event(f"open_release_url: webbrowser.open retourne {opened}")
        return bool(opened)
    except Exception as exc:
        _log_update_event(
            f"open_release_url: webbrowser.open echec error={exc.__class__.__name__}: {exc}"
        )
        _log_update_event(traceback.format_exc())
        return False
