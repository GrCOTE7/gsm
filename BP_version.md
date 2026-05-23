# 📋 Full Action Plan to Automate Versioning

With Tests + APK Build + Google Drive upload

## 🎯 Tools Used

* **Conventional Commits**
* **commitlint**
* **Husky** (Git hooks)
* **Semantic Release** (or *standard-version*)
* **CI/CD** (GitHub Actions or GitLab CI)
* **Gradle** (APK build)
* **Google Drive API**

---

## 🧩 1. Set Up Commit Conventions

* [x] Install and adopt **Conventional Commits**
  (`feat!:` ou `fix!:`, `feat:`, `fix:` ↑ respectively Major, Minor, Patch)
* [x] npm install --save-dev @commitlint/config-conventional @commitlint/cli
  * [x] Ensures commit messages follow a predictable structure.
  * [x] Enables automated versioning based on commit type.
  * [x] Validates commit messages before they are accepted.

* [x] Configure commitlint rules
  * [x] Create `commitlint.config.js` at project root:
  
  ```js
    module.exports = { extends: ['@commitlint/config-conventional'] };
  ```

  * [x] Rejects commits that do not follow the Conventional Commits format.
  * [x] Ensures consistency across the entire project history.

---

## 🪝 2. Block Commit/Push When Tests Fail

* [x] Install **Husky**: to manage Git hooks - npm install husky --save-dev
* [x] Active **Husky**: In package.json
  "scripts": {
    "prepare": "husky"
  }

  * [x] Allows running scripts automatically before commit or push.

* [x] Create file `.husky/_/commit-msg`
  * [ ] Add commitlint invocation:

    ```sh
    #!/usr/bin/env sh
    . "$(dirname "$0")/h"
    npx --no -- commitlint --edit "$1"
    ```

* [x] Create file `.husky/pre-commit`
* [x] Add:

    ```sh
  #!/usr/bin/env sh
  . "$(dirname -- "$0")/_/h"

  pytest -q
    ```

  * [x] Abort the commit if any test fails.
  * [x] Prevents broken code from entering the repository.

* [x] Create a `pre-push` hook:
  * [x] Create file `.husky/_/pre-push`
  * [x] Add:

    ```sh
    #!/bin/sh
    . "$(dirname "$0")/_/husky.sh"
    pytest
    ```

  * [x] Block the push if tests fail.
  * [x] Ensures only validated code reaches the remote repository.

---

## 🔢 3. Automate Version Number Bumping

### Option A (recommended): Semantic Release

* [x] Install **semantic-release** and required plugins:

  ```sh
  npm install --save-dev semantic-release \
    @semantic-release/commit-analyzer \
    @semantic-release/release-notes-generator \
    @semantic-release/changelog \
    @semantic-release/git
  ```

  * `fix:` → **patch** · `feat:` → **minor** · `feat!:` → **major**

* [x] Create `.releaserc.json` at project root:

  ```json
  {
    "branches": ["main"],
    "plugins": [
      "@semantic-release/commit-analyzer",
      "@semantic-release/release-notes-generator",
      ["@semantic-release/changelog", { "changelogFile": "CHANGELOG.md" }],
      ["@semantic-release/git", { "assets": ["CHANGELOG.md"], "message": "chore(release): ${nextRelease.version} [skip ci]" }]
    ]
  }
  ```

* [x] Add `release` script in `package.json`:

  ```json
  "scripts": {
    "prepare": "husky",
    "release": "semantic-release"
  }
  ```

* [x] Test dry-run locally (requires `GITHUB_TOKEN` env var set in shell):

  ```sh
  $env:GH_TOKEN = (Get-Content .env | Select-String "GH_TOKEN").ToString().Split("=")[1]
  npx semantic-release --dry-run
  ```

---

## 🔄 4. Automate Workflow with CI/CD

### GitHub Actions

* [x] Create directory:

  ```sh
  mkdir -p .github/workflows
  ```

* [x] Create `.github/workflows/release.yml`:

  ```yaml
  name: Release

  on:
    push:
      branches: [main]

  jobs:
    release:
      runs-on: ubuntu-latest
      permissions:
        contents: write
      steps:
        - uses: actions/checkout@v4
          with:
            fetch-depth: 0

        - name: Set up Python
          uses: actions/setup-python@v5
          with:
            python-version: "3.12"

        - name: Install Python dependencies
          run: pip install -r requirements.txt

        - name: Run tests
          run: pytest

        - name: Set up Node.js
          uses: actions/setup-node@v4
          with:
            node-version: "20"

        - name: Install Node dependencies
          run: npm ci

        - name: Run semantic-release
          env:
            GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          run: npx semantic-release

        - name: Set up Java
          uses: actions/setup-java@v4
          with:
            distribution: temurin
            java-version: "17"

        - name: Build APK
          working-directory: build/flutter/android
          run: ./gradlew assembleRelease

        - name: Upload APK to Google Drive
          env:
            GDRIVE_CREDENTIALS: ${{ secrets.GDRIVE_CREDENTIALS }}
          run: python src/scripts/upload_drive.py build/flutter/android/app/build/outputs/apk/release/app-release.apk
  ```

* [x] Add `GITHUB_TOKEN` is automatic — no action needed.
* [x] Add `GDRIVE_CREDENTIALS` secret: GitHub → Settings → Secrets
  → Actions → New repository secret.

---

## 🏗️ 5. Automatically Build the APK

* [ ] Verify the build locally:

  ```sh
  cd build/flutter/android
  ./gradlew assembleRelease
  ```

* [ ] Confirm output at:

  ```
  build/flutter/android/app/build/outputs/apk/release/app-release.apk
  ```

---

## ☁️ 6. Automatically Upload APK to Google Drive

* [ ] Create a **Google Cloud project** at <https://console.cloud.google.com>

* [ ] Enable the **Google Drive API**:
  APIs & Services → Enable APIs → search "Google Drive API" → Enable

* [ ] Create a **service account** + download JSON key:
  APIs & Services → Credentials → Create Credentials
  → Service Account → create key (JSON)

* [ ] Share the target GDrive/ with the service account email (Editor role).

* [ ] Add the JSON key content as CI secret `GDRIVE_CREDENTIALS`.

* [x] Create `src/scripts/upload_drive.py`:

  ```python
  import json, os, sys
  from googleapiclient.discovery import build
  from googleapiclient.http import MediaFileUpload
  from google.oauth2.service_account import Credentials

  FOLDER_ID = "YOUR_DRIVE_FOLDER_ID"  # à remplacer

  creds_info = json.loads(os.environ["GDRIVE_CREDENTIALS"])
  creds = Credentials.from_service_account_info(
      creds_info, scopes=["https://www.googleapis.com/auth/drive.file"]
  )
  service = build("drive", "v3", credentials=creds)

  apk_path = sys.argv[1]
  file_name = os.path.basename(apk_path)
  media = MediaFileUpload(apk_path, mimetype="application/vnd.android.package-archive")
  service.files().create(
      body={"name": file_name, "parents": [FOLDER_ID]},
      media_body=media,
  ).execute()
  print(f"Uploaded: {file_name}")
  ```

* [x] Install upload dependency:

  ```sh
  pip install google-api-python-client google-auth
  ```

  And add to `requirements.txt`.

* [ ] Test upload locally:

  ```sh
  export GDRIVE_CREDENTIALS=$(cat path/to/key.json)
  python src/scripts/upload_drive.py path/to/app-release.apk
  ```

---

## 🧪 7. Final Verification

* [ ] Make a conventional commit and push:

  ```sh
  git add .
  git commit -m "feat: test versioning pipeline"
  git push origin main
  ```

* [ ] Validate on GitHub Actions tab:
  * [ ] Tests pass
  * [ ] `semantic-release` increments version (minor bump expected)
  * [ ] `CHANGELOG.md` is updated and committed
  * [ ] Git tag `v*.*.*` is created
  * [ ] APK is built
  * [ ] APK is uploaded to Google Drive target folder
