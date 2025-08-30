#!/usr/bin/env python3
"""
Sync publication mirrors at repo root from RESEARCH sources with a provenance banner.

Usage:
  python Copilotage/scripts/editorial/sync_publications.py [--final]

- Copies rich sources to root mirrors when source is non-empty.
- Adds a provenance banner with source path, date, and current branch.
- Leaves *_FINAL_* files as placeholders unless --final is set (no-op by default).
"""
from __future__ import annotations
import argparse
import datetime as dt
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

BANNER_EN = "<!-- SYNC: Source={src}; Date={date}; Branch={branch}. Edit the source, not this file. -->\n\n"
BANNER_FR = "<!-- SYNC: Source={src}; Date={date}; Branch={branch}. Modifiez la source, pas ce fichier. -->\n\n"

MAPPINGS = [
    # Medium articles
    ("RESEARCH/publications/articles/english/ARTICLE_MEDIUM_2025_EN.md", "ARTICLE_MEDIUM_2025_EN.md", BANNER_EN),
    ("RESEARCH/publications/articles/french/ARTICLE_MEDIUM_2025.md", "ARTICLE_MEDIUM_2025.md", BANNER_FR),
    # Leanpub books
    ("RESEARCH/publications/books/french/LIVRE_LEANPUB_2025.md", "LIVRE_LEANPUB_2025.md", BANNER_FR),
    ("RESEARCH/publications/books/english/LIVRE_LEANPUB_2025_EN.md", "LIVRE_LEANPUB_2025_EN.md", BANNER_EN),
]

FINAL_TARGETS = [
    "ARTICLE_MEDIUM_FINAL_2025.md",
    "ARTICLE_MEDIUM_FINAL_2025_EN.md",
    "LIVRE_LEANPUB_FINAL_2025.md",
]


def get_branch() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ROOT).decode().strip()
    except Exception:
        return "unknown"


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def write_text(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def is_non_empty(p: Path) -> bool:
    if not p.exists():
        return False
    try:
        content = read_text(p).strip()
    except Exception:
        return False
    return len(content) > 0


def sync_one(src_rel: str, dst_rel: str, banner_template: str) -> bool:
    src = ROOT / src_rel
    dst = ROOT / dst_rel
    if not is_non_empty(src):
        return False
    content = read_text(src)
    date = dt.date.today().isoformat()
    branch = get_branch()
    banner = banner_template.format(src=src_rel, date=date, branch=branch)

    # If destination already has a SYNC banner, strip the previous banner line(s)
    dst_text = ""
    if dst.exists():
        existing = read_text(dst)
        lines = existing.splitlines()
        if lines and lines[0].startswith("<!-- SYNC: "):
            # remove initial banner block (first line only or until blank line)
            # Find first blank line after banner
            i = 1
            while i < len(lines) and lines[i].strip() != "":
                i += 1
            dst_text = "\n".join(lines[i+1:]) if i < len(lines) else ""
        else:
            dst_text = existing

    new_text = banner + content
    # Only write if changed
    if dst_text.strip() == content.strip() and dst.exists():
        return False
    write_text(dst, new_text)
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--final", action="store_true", help="Update *_FINAL_* placeholders (currently no-op)")
    args = ap.parse_args()

    changed = False
    for src, dst, banner in MAPPINGS:
        if sync_one(src, dst, banner):
            print(f"synced: {dst} <- {src}")
            changed = True
        else:
            print(f"skipped (missing or unchanged): {dst}")

    if args.final:
        # Placeholder for future final-assembly logic
        for t in FINAL_TARGETS:
            print(f"final target untouched: {t}")

    if changed:
        print("DONE: Some files updated.")
        return 0
    print("DONE: No changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
