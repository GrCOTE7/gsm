from datetime import datetime

from upu.config import get_app_build_latest_check_at, get_latest_release_info

KEY_UPDATE_LAST_CHECK_AT = "update.last_check_at"
KEY_UPDATE_LATEST_VERSION = "update.latest_version"
LEGACY_KEY_LAST_CHECK = "last_check"
LEGACY_KEY_LATEST_VERSION = "latest_version"


class UpdateService:
    """🔧 5) update_service.py"""

    def __init__(self, storage):
        self.storage = storage

    def get_last_check_at(self):
        value = self.storage.get(KEY_UPDATE_LAST_CHECK_AT)
        if value is not None:
            return value
        return self.storage.get(LEGACY_KEY_LAST_CHECK)

    def get_latest_version(self):
        value = self.storage.get(KEY_UPDATE_LATEST_VERSION)
        if value is not None:
            return value
        return self.storage.get(LEGACY_KEY_LATEST_VERSION)

    def check_latest(self):
        latest_release = get_latest_release_info()
        latest = str(latest_release.get("version") or "").strip()
        if not latest:
            raise RuntimeError("Latest version is missing from release payload")

        checked_at = get_app_build_latest_check_at() or datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )

        self.storage.set(KEY_UPDATE_LAST_CHECK_AT, checked_at)
        self.storage.set(KEY_UPDATE_LATEST_VERSION, latest)

        # Retrocompatibilite temporaire des anciennes cles.
        self.storage.set(LEGACY_KEY_LAST_CHECK, checked_at)
        self.storage.set(LEGACY_KEY_LATEST_VERSION, latest)

        return latest
