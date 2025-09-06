#!/usr/bin/env python3
"""
Ouvre des issues "alignement documentaire" dans chaque sous-module à partir de issues_packs.

Prérequis:
- Variable d'env GH_TOKEN avec un token GitHub ayant accès en écriture aux repos cibles.

Usage:
  python3 scripts/open_submodule_issues.py --dry-run   # n'imprime que les requêtes
  python3 scripts/open_submodule_issues.py              # crée les issues
"""
from __future__ import annotations
from pathlib import Path
import argparse
import os
import re
import sys
import json
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ecosystem.yml"
PACKS = ROOT / "issues_packs"


def load_yaml(path: Path):
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def repo_items(data: dict):
    for cat in ("submodules", "external"):
        for item in data.get(cat) or []:
            yield cat, item


def parse_repo_slug(url: str) -> tuple[str, str] | None:
    # Expect https://github.com/owner/repo
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+)$", url.strip())
    if not m:
        return None
    return m.group(1), m.group(2)


def gh_post(path: str, token: str, payload: dict, dry_run: bool = False):
    url = f"https://api.github.com{path}"
    data = json.dumps(payload).encode("utf-8")
    if dry_run:
        print("[dry-run] POST", url)
        print("[dry-run] payload:", json.dumps(payload, ensure_ascii=False))
        return None
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode("utf-8")
        print("[created]", url, resp.status)
        return json.loads(body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Ne pas créer, afficher seulement")
    args = ap.parse_args()

    token = os.environ.get("GH_TOKEN")
    if not args.dry_run and not token:
        print("Erreur: GH_TOKEN manquant dans l'environnement.", file=sys.stderr)
        sys.exit(2)

    data = load_yaml(DATA)
    if not PACKS.exists():
        print("Aucun pack trouvé; exécutez scripts/prepare_issue_packs.py d'abord.")
        sys.exit(1)

    for cat, item in repo_items(data):
        key = item.get("key")
        name = item.get("name", key)
        url = item.get("url")
        if not (key and url):
            continue
        slug = parse_repo_slug(url)
        if not slug:
            print(f"[skip] URL inattendue pour {name}: {url}")
            continue
        owner, repo = slug
        body_path = PACKS / key / "ISSUE_BODY.md"
        if not body_path.exists():
            print(f"[skip] Pas de pack pour {key}")
            continue
        body = body_path.read_text(encoding="utf-8")
        title = f"{name} — alignement documentaire"
        payload = {
            "title": title,
            "body": body,
            # Labels optionnels si existants côté repo
            "labels": ["documentation", "status:triage"],
        }
        path = f"/repos/{owner}/{repo}/issues"
        gh_post(path, token or "", payload, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
