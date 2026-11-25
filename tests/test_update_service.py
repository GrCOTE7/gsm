import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest

from gsm.services import update_service

APP_BUILD_PATH = (
    Path(__file__).resolve().parents[1] / "src" / "gsm" / "app_data" / "app_build.json"
)


def _fake_release(version: str, url: str = "https://example.test/tag/v9.9.9") -> dict:
    return {
        "version": version,
        "html_url": url,
        "download_url": url,
        "published_at": "2026-11-25 10:00",
        "name": f"v{version}",
        "draft": False,
        "prerelease": False,
    }


@pytest.fixture(autouse=True)
def _clear_cache(monkeypatch):
    monkeypatch.setattr(update_service, "_cached_info", None, raising=False)


def test_local_version_comes_from_the_gsm_build_file():
    expected = json.loads(APP_BUILD_PATH.read_text(encoding="utf-8"))["version"]
    assert update_service.local_version() == expected


def test_update_available_when_github_release_is_newer(monkeypatch):
    monkeypatch.setattr(update_service, "local_version", lambda: "1.1.4")
    monkeypatch.setattr(
        update_service,
        "get_latest_release_info",
        lambda **_: _fake_release("1.1.5"),
    )

    info = update_service.get_update_info()

    assert info["update_available"] is True
    assert info["local_version"] == "1.1.4"
    assert info["latest_version"] == "1.1.5"
    assert info["html_url"] == "https://example.test/tag/v9.9.9"


@pytest.mark.parametrize("latest", ["1.1.4", "1.1.3", "1.0.99"])
def test_no_update_when_release_is_equal_or_older(monkeypatch, latest):
    monkeypatch.setattr(update_service, "local_version", lambda: "1.1.4")
    monkeypatch.setattr(
        update_service,
        "get_latest_release_info",
        lambda **_: _fake_release(latest),
    )

    assert update_service.get_update_info()["update_available"] is False


def test_version_comparison_is_numeric_not_lexical(monkeypatch):
    monkeypatch.setattr(update_service, "local_version", lambda: "1.1.9")
    monkeypatch.setattr(
        update_service,
        "get_latest_release_info",
        lambda **_: _fake_release("1.1.10"),
    )

    assert update_service.get_update_info()["update_available"] is True


def test_update_info_is_cached_for_the_process(monkeypatch):
    calls: list[int] = []

    def fake_release_info(**_kwargs):
        calls.append(1)
        return _fake_release("1.1.5")

    monkeypatch.setattr(update_service, "local_version", lambda: "1.1.4")
    monkeypatch.setattr(update_service, "get_latest_release_info", fake_release_info)

    update_service.get_update_info()
    update_service.get_update_info()
    assert len(calls) == 1

    update_service.get_update_info(force=True)
    assert len(calls) == 2


def test_network_failure_never_raises_and_reports_no_update(monkeypatch):
    def boom(**_kwargs):
        raise RuntimeError("offline")

    monkeypatch.setattr(update_service, "local_version", lambda: "1.1.4")
    monkeypatch.setattr(update_service, "get_latest_release_info", boom)

    info = update_service.get_update_info()

    assert info["update_available"] is False
    assert info["local_version"] == "1.1.4"
