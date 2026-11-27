#!/usr/bin/env python3
"""Top 10 des dépôts personnels de GrCOTE7 par nombre de commits.

Les forks sont exclus par défaut (option --include-forks pour les inclure).
Le token GitHub est lu depuis l'environnement (GH_TOKEN ou GITHUB_TOKEN) ou,
à défaut, depuis le fichier .env à la racine du dépôt.
"""

import argparse
import os
import re
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

# Chemin explicite : `load_dotenv()` sans argument appelle `find_dotenv()`, qui
# remonte la pile d'appels (AssertionError dans un build Android).
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

USER = "GrCOTE7"
TOKEN = (os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or "").strip()

HEADERS = {
    "User-Agent": "top-repos-script",
    "Accept": "application/vnd.github+json",
}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def get_commit_count(repo: str) -> int:
    """Nombre de commits d'un repo via le header Link (per_page=1)."""
    url = f"https://api.github.com/repos/{USER}/{repo}/commits?per_page=1"
    try:
        r = requests.head(url, headers=HEADERS, timeout=10, allow_redirects=True)
        if r.status_code == 409:  # repo vide
            return 0
        if r.status_code != 200:
            return 0
        link = r.headers.get("Link", "")
        # Segment du type : <.../commits?per_page=1&page=762>; rel="last"
        for part in link.split(","):
            if 'rel="last"' not in part:
                continue
            match = re.search(r"[?&]page=(\d+)", part)
            if match:
                return int(match.group(1))
        return 1
    except Exception as e:
        print(f"  ! erreur sur {repo}: {e}", file=sys.stderr)
        return 0


def list_repos() -> list[dict]:
    """Liste tous les repos du user (pagination)."""
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{USER}/repos?per_page=100&page={page}"
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            print(f"Erreur API: {r.status_code} {r.text}", file=sys.stderr)
            break
        data = r.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Top 10 des dépôts personnels par nombre de commits "
        "(forks exclus par défaut)."
    )
    parser.add_argument(
        "--include-forks",
        action="store_true",
        help="inclure aussi les dépôts forqués",
    )
    args = parser.parse_args()

    if TOKEN:
        print(
            f"Utilisateur GitHub : {USER} (token chargé, authentifié)\n",
            file=sys.stderr,
        )
    else:
        print(
            "⚠️  Pas de GITHUB_TOKEN (env ou .env) → rate limit 60 req/h\n",
            file=sys.stderr,
        )

    print(f"Récupération des repos de {USER}...", file=sys.stderr)
    all_repos = list_repos()
    if args.include_forks:
        repos = all_repos
    else:
        repos = [r for r in all_repos if not r.get("fork")]
    excluded = len(all_repos) - len(repos)
    detail = f" ({excluded} fork(s) exclu(s))" if excluded else ""
    print(f"  {len(repos)} dépôts trouvés{detail}\n", file=sys.stderr)

    print("Calcul des commits par dépôt (patience)...", file=sys.stderr)
    results = []
    for i, r in enumerate(repos, 1):
        name = r["name"]
        print(f"  [{i}/{len(repos)}] {name}", file=sys.stderr)
        results.append(
            {
                "repo": name,
                "commits": get_commit_count(name),
                "url": r["html_url"],
            }
        )

    # Tri décroissant par nombre de commits
    results.sort(key=lambda x: x["commits"], reverse=True)

    # Affichage du tableau complet
    scope = "tous dépôts (forks inclus)" if args.include_forks else "hors forks"
    print(f"\nDépôts — {scope}")
    print(f"{'Repo':<40} {'Commits':>8}  URL")
    print("-" * 100)
    for row in results:
        print(f"{row['repo']:<40} {row['commits']:>8}  {row['url']}")
    print("-" * 100)

    # Synthèse
    top10_sum = sum(r["commits"] for r in results[:10])
    total_sum = sum(r["commits"] for r in results)

    print(f"{'Nombre de commits du top 10':<40} {top10_sum:>8}")
    print(f"{'Nombre total de tous les dépôts':<40} {total_sum:>8}")


if __name__ == "__main__":
    main()
