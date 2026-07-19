from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from upu.services import release_service


def test_open_release_url_throttles_for_one_hour(monkeypatch, tmp_path: Path) -> None:
    opened_urls: list[str] = []
    current_time = 1000.0

    monkeypatch.setattr(release_service, "_DATA_DIR", tmp_path)
    monkeypatch.setattr(
        release_service,
        "_APP_STATE_PATH",
        tmp_path / "app_state.json",
    )
    monkeypatch.setattr(
        release_service,
        "_UPDATE_LOG_PATH",
        tmp_path / "update_flow.log",
    )
    monkeypatch.setattr(release_service, "_last_open_release_url_at", None)
    monkeypatch.setattr(release_service, "_current_timestamp", lambda: current_time)
    monkeypatch.setattr(
        release_service.webbrowser,
        "open",
        lambda url, *args, **kwargs: opened_urls.append(url) or True,
    )

    release_service.open_release_url(None, "https://example.com/release")
    release_service.open_release_url(None, "https://example.com/release")

    current_time += 3601.0
    release_service.open_release_url(None, "https://example.com/release")

    assert opened_urls == [
        "https://example.com/release",
        "https://example.com/release",
    ]


def test_open_release_url_throttles_across_restart(monkeypatch, tmp_path: Path) -> None:
    opened_urls: list[str] = []
    current_time = 5000.0

    monkeypatch.setattr(release_service, "_DATA_DIR", tmp_path)
    monkeypatch.setattr(
        release_service,
        "_APP_STATE_PATH",
        tmp_path / "app_state.json",
    )
    monkeypatch.setattr(
        release_service,
        "_UPDATE_LOG_PATH",
        tmp_path / "update_flow.log",
    )
    monkeypatch.setattr(release_service, "_last_open_release_url_at", None)
    monkeypatch.setattr(release_service, "_current_timestamp", lambda: current_time)
    monkeypatch.setattr(
        release_service.webbrowser,
        "open",
        lambda url, *args, **kwargs: opened_urls.append(url) or True,
    )

    release_service.open_release_url(None, "https://example.com/release")

    monkeypatch.setattr(release_service, "_last_open_release_url_at", None)
    release_service.open_release_url(None, "https://example.com/release")

    current_time += 3601.0
    monkeypatch.setattr(release_service, "_last_open_release_url_at", None)
    release_service.open_release_url(None, "https://example.com/release")

    assert opened_urls == [
        "https://example.com/release",
        "https://example.com/release",
    ]


def test_transform_url_to_android_install_intent() -> None:
    """Test que les URLs APK sont transformées en intent:// pour forcer PackageInstaller."""
    apk_url = (
        "https://github.com/GrCOTE7/gsm/releases/download/v1.0.5/UpU-arm64-v8a.apk"
    )
    transformed = release_service._transform_url_to_android_install_intent(apk_url)

    # Vérifier que c'est un intent://
    assert transformed.startswith("intent://")
    # Vérifier que le scheme est préservé
    assert "scheme=https" in transformed
    # Vérifier que c'est pour PackageInstaller (mime type d'APK)
    assert "type=application/vnd.android.package-archive" in transformed
    # Vérifier qu'on a bien l'URL sans le scheme
    assert (
        "github.com/GrCOTE7/gsm/releases/download/v1.0.5/UpU-arm64-v8a.apk"
        in transformed
    )

    # URLs non-APK doivent rester inchangées
    non_apk_url = "https://example.com/file.txt"
    assert (
        release_service._transform_url_to_android_install_intent(non_apk_url)
        == non_apk_url
    )


def test_open_release_url_force_bypasses_cooldown(monkeypatch, tmp_path: Path) -> None:
    opened_urls: list[str] = []
    current_time = 7000.0

    monkeypatch.setattr(release_service, "_DATA_DIR", tmp_path)
    monkeypatch.setattr(
        release_service,
        "_APP_STATE_PATH",
        tmp_path / "app_state.json",
    )
    monkeypatch.setattr(
        release_service,
        "_UPDATE_LOG_PATH",
        tmp_path / "update_flow.log",
    )
    monkeypatch.setattr(release_service, "_last_open_release_url_at", None)
    monkeypatch.setattr(release_service, "_current_timestamp", lambda: current_time)
    monkeypatch.setattr(
        release_service.webbrowser,
        "open",
        lambda url, *args, **kwargs: opened_urls.append(url) or True,
    )

    # Premier clic normal: ouvre le lien
    assert release_service.open_release_url(None, "https://example.com/release")
    # Deuxieme clic immediat force: doit ouvrir malgre le cooldown
    assert release_service.open_release_url(
        None, "https://example.com/release", force=True
    )

    assert opened_urls == [
        "https://example.com/release",
        "https://example.com/release",
    ]


def test_normalize_desktop_release_url_download_to_tag() -> None:
    url = "https://github.com/GrCOTE7/gsm/releases/download/v1.2.3/UpU.apk"
    assert (
        release_service._normalize_desktop_release_url(url)
        == "https://github.com/GrCOTE7/gsm/releases/tag/v1.2.3"
    )


def test_open_release_url_desktop_prefers_release_page(
    monkeypatch, tmp_path: Path
) -> None:
    opened_urls: list[str] = []

    monkeypatch.setattr(release_service, "_DATA_DIR", tmp_path)
    monkeypatch.setattr(release_service, "_APP_STATE_PATH", tmp_path / "app_state.json")
    monkeypatch.setattr(
        release_service, "_UPDATE_LOG_PATH", tmp_path / "update_flow.log"
    )
    monkeypatch.setattr(release_service, "_last_open_release_url_at", None)
    monkeypatch.setattr(release_service, "_current_timestamp", lambda: 8000.0)
    monkeypatch.setattr(
        release_service.webbrowser,
        "open",
        lambda url, *args, **kwargs: opened_urls.append(url) or True,
    )

    assert release_service.open_release_url(
        None,
        "https://github.com/GrCOTE7/gsm/releases/download/v1.2.3/UpU.apk",
        force=True,
    )

    assert opened_urls == ["https://github.com/GrCOTE7/gsm/releases/tag/v1.2.3"]


def test_open_release_url_desktop_uses_page_launch_url(
    monkeypatch, tmp_path: Path
) -> None:
    opened_urls: list[str] = []
    run_task_called = {"called": False}

    class _Platform:
        name = "windows"

        @staticmethod
        def is_mobile() -> bool:
            return False

    class _Page:
        platform = _Platform()

        async def launch_url(self, target: str) -> None:
            opened_urls.append(target)

        def run_task(self, task) -> None:
            run_task_called["called"] = True

    monkeypatch.setattr(release_service, "_DATA_DIR", tmp_path)
    monkeypatch.setattr(release_service, "_APP_STATE_PATH", tmp_path / "app_state.json")
    monkeypatch.setattr(
        release_service, "_UPDATE_LOG_PATH", tmp_path / "update_flow.log"
    )
    monkeypatch.setattr(release_service, "_last_open_release_url_at", None)
    monkeypatch.setattr(release_service, "_current_timestamp", lambda: 9000.0)

    # Ne doit pas etre appele si run_task est disponible.
    monkeypatch.setattr(
        release_service.webbrowser,
        "open",
        lambda url, *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("unexpected")
        ),
    )

    page = _Page()
    assert release_service.open_release_url(
        page, #type: ignore
        "https://github.com/GrCOTE7/gsm/releases/tag/v1.2.3",
        force=True,
    )

    assert run_task_called["called"] is True
    assert opened_urls == []
