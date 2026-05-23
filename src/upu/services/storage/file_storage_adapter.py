import json
from pathlib import Path
from .storage_base import Storage

_DATA_DIR = Path(__file__).resolve().parents[2] / "app_data"
_APP_STATE_PATH = _DATA_DIR / "app_state.json"


class FileStorageAdapter(Storage):
    """🟩 3) file_storage_adapter.py"""

    def __init__(self, filename: str | Path | None = None):
        self.filename = Path(filename) if filename is not None else _APP_STATE_PATH
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        if not self.filename.exists():
            self.filename.write_text("{}", encoding="utf-8")

    def _load(self):
        with self.filename.open(encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data):
        with self.filename.open("w", encoding="utf-8") as f:
            json.dump(data, f)

    def get(self, key):
        return self._load().get(key)

    def set(self, key, value):
        data = self._load()
        data[key] = value
        self._save(data)
