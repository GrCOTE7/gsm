import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Charge .env si present (local). En CI, les variables sont injectees directement.
load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


def load_credentials() -> Credentials:
    return Credentials(
        token=None,
        refresh_token=require_env("GDRIVE_REFRESH_TOKEN"),
        client_id=require_env("GDRIVE_CLIENT_ID"),
        client_secret=require_env("GDRIVE_CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/drive"],
    )


def main() -> int:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/upload_drive.py <path-to-apk>")

    folder_id = require_env("GDRIVE_FOLDER_ID")
    creds = load_credentials()
    service = build("drive", "v3", credentials=creds)

    apk_path = sys.argv[1]
    if not os.path.isfile(apk_path):
        raise FileNotFoundError(f"APK not found: {apk_path}")

    file_name = os.path.basename(apk_path)
    media = MediaFileUpload(
        apk_path, mimetype="application/vnd.android.package-archive"
    )

    try:
        folder = (
            service.files()
            .get(fileId=folder_id, fields="id,name,driveId", supportsAllDrives=True)
            .execute()
        )
        print(
            "Folder access OK:",
            folder.get("name"),
            "driveId=",
            folder.get("driveId", "my-drive"),
        )

        uploaded_file = (
            service.files()
            .create(
                body={"name": file_name, "parents": [folder_id]},
                media_body=media,
                fields="id,name,webViewLink",
                supportsAllDrives=True,
            )
            .execute()
        )
    except HttpError as exc:
        raise RuntimeError(f"Google Drive upload failed: {exc}") from exc

    print("Upload OK! File ID:", uploaded_file.get("id"))
    print("View:", uploaded_file.get("webViewLink"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
