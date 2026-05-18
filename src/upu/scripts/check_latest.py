from upu.services.storage.storage_factory import create_storage
from upu.services.update_service import UpdateService

# 🧪 7) Usage dans un service non‑UI


def main() -> None:
    storage = create_storage()
    service = UpdateService(storage)
    latest = service.check_latest()
    last_check_at = service.get_last_check_at()
    print("Latest:", latest)
    print("Last check:", last_check_at)


if __name__ == "__main__":
    main()
