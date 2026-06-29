#!/usr/bin/env python3
"""Poll GitHub latest release every 10s for up to 20 minutes."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

API_URL = "https://api.github.com/repos/GrCOTE7/gsm/releases/latest"
POLL_SECONDS = 10
MAX_MINUTES = 20
ANSI_RESET = "\033[0m"
ANSI_WHITE = "\033[37m"
ANSI_GREEN = "\033[32m"

# Note: Sans token (requêtes anonymes) : 60 requêtes par heure, par IP.
# → Avec token perso (PAT) : 5000 requêtes par heure, par utilisateur/token.
# Il existe aussi une limite secondaire (anti-abus) qui peut renvoyer 403 même avant la limite horaire.
# Solution à terme:
# V2 propre avec update.json statique et un flow “publication atomique” côté CI, ce qui te supprimera:

# la dépendance au rate-limit GitHub côté clients,
# le besoin de token dans l’app,
# les faux positifs pendant la fenêtre de build.

def load_github_token() -> str:
    token = (os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or "").strip()
    if token:
        return token

    env_file = Path(__file__).resolve().parents[1] / ".env"
    if not env_file.exists():
        return ""

    try:
        for raw_line in env_file.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            if key not in {"GH_TOKEN", "GITHUB_TOKEN"}:
                continue
            return value.strip().strip('"').strip("'")
    except OSError:
        return ""

    return ""


def format_reset(reset_epoch: str) -> str:
    if not reset_epoch:
        return "<none>"
    try:
        return datetime.fromtimestamp(int(reset_epoch)).strftime("%H:%M:%S")
    except (ValueError, OSError):
        return reset_epoch


def fetch_latest(token: str) -> tuple[dict, str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "gsm-latest-watcher",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(
        API_URL,
        headers=headers,
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))
        remaining = response.headers.get("X-RateLimit-Remaining", "<none>")
        reset = format_reset(response.headers.get("X-RateLimit-Reset", ""))
        return data, remaining, reset


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def color_line(message: str, green: bool) -> str:
    color = ANSI_GREEN if green else ANSI_WHITE
    return f"{color}{message}{ANSI_RESET}"


def main() -> int:
    max_loops = (MAX_MINUTES * 60) // POLL_SECONDS
    token = load_github_token()
    print(f"Watching latest release for {MAX_MINUTES} minutes ({max_loops} checks)...")
    print(f"Source: {API_URL}")
    print(f"Auth token: {'yes' if token else 'no'}")
    previous_key: str | None = None
    green_on_change = False

    for i in range(1, max_loops + 1):
        try:
            data, remaining, reset = fetch_latest(token)
            tag = data.get("tag_name", "<none>")
            name = data.get("name", "<none>")
            published = data.get("published_at", "<none>")
            draft = data.get("draft", False)
            prerelease = data.get("prerelease", False)
            key = str(data.get("id") or f"{tag}|{published}")
            changed = previous_key is not None and key != previous_key
            if changed:
                green_on_change = not green_on_change
            previous_key = key

            line = (
                f"[{now_iso()}] #{i:03d} tag={tag} name={name} "
                f"published_at={published} draft={draft} prerelease={prerelease} "
                f"remaining={remaining} reset={reset}"
            )
            print(color_line(line, green_on_change))
        except urllib.error.HTTPError as exc:
            remaining = exc.headers.get("X-RateLimit-Remaining", "<none>")
            reset = format_reset(exc.headers.get("X-RateLimit-Reset", ""))
            print(
                color_line(
                    f"[{now_iso()}] #{i:03d} HTTP error: {exc.code} {exc.reason} "
                    f"remaining={remaining} reset={reset}",
                    False,
                )
            )
        except urllib.error.URLError as exc:
            print(
                color_line(f"[{now_iso()}] #{i:03d} Network error: {exc.reason}", False)
            )
        except Exception as exc:  # pragma: no cover
            print(color_line(f"[{now_iso()}] #{i:03d} Unexpected error: {exc}", False))

        if i < max_loops:
            time.sleep(POLL_SECONDS)

    print("Done.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
