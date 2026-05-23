from pathlib import Path
import sys

if __package__ in {None, ""}:
    # Allow direct execution: python src/upu/scripts/check_latest.py
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from upu.config import get_latest_release_info
from upu.services.state_repository import get_cached_release_info, get_last_check_at

# 🧪 7) Usage dans un service non‑UI


def main() -> None:
    latest_release = get_latest_release_info()
    cached_release = get_cached_release_info() or latest_release
    latest = str(cached_release.get("version") or "").strip()
    last_check_at = get_last_check_at()
    print("Latest:", latest)
    print("Last check:", last_check_at)


if __name__ == "__main__":
    main()
