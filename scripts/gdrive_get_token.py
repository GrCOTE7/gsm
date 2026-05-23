"""
Run ONCE locally to obtain a Google OAuth refresh token.

Prerequisites:
  1. Google Cloud Console → APIs & Services → Credentials
     → Create credentials → OAuth 2.0 client ID → Desktop app
  2. Download the JSON and set GDRIVE_CLIENT_ID / GDRIVE_CLIENT_SECRET in .env
     (or pass them as env vars)

Usage:
    python scripts/gdrive_get_token.py

Output: prints GDRIVE_REFRESH_TOKEN — paste it into .env and GitHub secrets.
"""

import os
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

CLIENT_ID = os.environ["GDRIVE_CLIENT_ID"]
CLIENT_SECRET = os.environ["GDRIVE_CLIENT_SECRET"]

client_config = {
    "installed": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
    }
}

SCOPES = ["https://www.googleapis.com/auth/drive"]

flow = InstalledAppFlow.from_client_config(client_config, scopes=SCOPES)
creds = flow.run_local_server(port=0)

print("\n=== Copie ces valeurs dans .env et dans les secrets GitHub ===")
print(f"GDRIVE_REFRESH_TOKEN={creds.refresh_token}")
print(f"GDRIVE_CLIENT_ID={CLIENT_ID}")
print(f"GDRIVE_CLIENT_SECRET={CLIENT_SECRET}")
