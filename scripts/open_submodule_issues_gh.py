#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse
import subprocess
import sys
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ecosystem.yml"
PACKS = ROOT / "issues_packs"


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def repo_items(data: dict):
    for cat in ("submodules", "external"):
        for item in data.get(cat) or []:
            yield cat, item


def parse_repo_slug(url: str) -> tuple[str, str] | None:
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+)$", url.strip())
    if not m:
        return None
    return m.group(1), m.group(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    # Check gh availability
    try:
        subprocess.run(["gh", "--version"], check=True, stdout=subprocess.DEVNULL)
    except Exception:
        print("Erreur: GitHub CLI (gh) introuvable.", file=sys.stderr)
        sys.exit(2)

    data = load_yaml(DATA)
    created = 0
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
        title = f"{name} — alignement documentaire"
        cmd = [
            "gh", "issue", "create",
            "-R", f"{owner}/{repo}",
            "-t", title,
            "-F", str(body_path),
            "-l", "documentation",
            "-l", "status:triage",
        ]
        if args.dry_run:
            print("[dry-run] ", " ".join(cmd))
        else:
            subprocess.run(cmd, check=False)
            created += 1
    print("Done. Issues processed:", created)


if __name__ == "__main__":
    main()
