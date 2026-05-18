import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Charger .env
load_dotenv()


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


FOLDER_ID = require_env("GDRIVE_FOLDER_ID")
creds = load_credentials()

# Construire le client Drive
service = build("drive", "v3", credentials=creds)

# Fichier à uploader
FILE_PATH = (
    sys.argv[1]
    if len(sys.argv) > 1
    else os.getenv("GDRIVE_TEST_FILE", "C:/gsm/build/apk/UpU.apk")
)
if not os.path.isfile(FILE_PATH):
    raise FileNotFoundError(f"APK not found: {FILE_PATH}")

FILE_NAME = os.path.basename(FILE_PATH)

file_metadata = {"name": FILE_NAME, "parents": [FOLDER_ID]}

media = MediaFileUpload(FILE_PATH, mimetype="application/vnd.android.package-archive")

try:
    # Validate folder access first (works for both My Drive and Shared Drive).
    folder = (
        service.files()
        .get(fileId=FOLDER_ID, fields="id,name,driveId", supportsAllDrives=True)
        .execute()
    )
    print(
        "Folder access OK:",
        folder.get("name"),
        "driveId=",
        folder.get("driveId", "my-drive"),
    )

    # Upload
    uploaded_file = (
        service.files()
        .create(
            body=file_metadata,
            media_body=media,
            fields="id,name,webViewLink",
            supportsAllDrives=True,
        )
        .execute()
    )
except HttpError as exc:
    raise

print("Upload OK! File ID:", uploaded_file.get("id"))
print("View:", uploaded_file.get("webViewLink"))
