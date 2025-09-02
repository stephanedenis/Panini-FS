#!/usr/bin/env python3
"""
Monitor GitHub PRs with Playwright (headless):
- Navigates to PR overview and checks pages
- Extracts status summary and saves screenshots

Usage:
  python scripts/devops/monitor_prs_playwright.py --repo stephanedenis/PaniniFS --prs 40,42 --out artifacts/playwright

If --prs is omitted, it will try to read open PR numbers via `gh pr list --json number`.
Requires: playwright (pip) and a browser installed (e.g. `python -m playwright install chromium`).
"""
from __future__ import annotations
import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import List

from playwright.sync_api import sync_playwright


def gh_json(args: List[str]) -> list:
    try:
        out = subprocess.check_output(["gh", *args], text=True)
        return json.loads(out)
    except Exception:
        return []


def get_pr_numbers(owner_repo: str, prs_arg: str | None) -> List[int]:
    if prs_arg:
        return [int(x) for x in prs_arg.split(",") if x.strip()]
    data = gh_json(["pr", "list", "--repo", owner_repo, "--state", "open", "--json", "number"])
    return [int(d["number"]) for d in data]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="owner/repo, e.g. stephanedenis/PaniniFS")
    ap.add_argument("--prs", help="Comma-separated PR numbers (default: list open PRs via gh)")
    ap.add_argument("--out", default="artifacts/playwright", help="Output directory for screenshots")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    owner, repo = args.repo.split("/", 1)
    pr_numbers = get_pr_numbers(args.repo, args.prs)
    if not pr_numbers:
        print("No PRs to monitor.")
        return 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1360, "height": 900})
        page = context.new_page()
        for pr in pr_numbers:
            base = f"https://github.com/{owner}/{repo}/pull/{pr}"
            checks = f"{base}/checks"
            print(f"[PR #{pr}] Visiting {base}")
            page.goto(base, wait_until="networkidle")
            # Grab a quick status summary from the header if present
            try:
                title = page.locator("h1.gh-header-title").inner_text(timeout=2000).strip()
            except Exception:
                title = "(title not found)"
            try:
                state = page.locator("span.State").first.inner_text(timeout=2000).strip()
            except Exception:
                state = "(state unknown)"
            print(f"  - title: {title}")
            print(f"  - state: {state}")
            shot1 = out_dir / f"pr-{pr}-overview.png"
            page.screenshot(path=str(shot1), full_page=True)

            print(f"[PR #{pr}] Visiting {checks}")
            page.goto(checks, wait_until="networkidle")
            # Try to capture checks summary; GitHub UI may vary
            try:
                summary = page.locator("[data-test-selector='checks-summary']").inner_text(timeout=2000).strip()
            except Exception:
                try:
                    summary = page.locator("text=Summary").first.inner_text(timeout=2000).strip()
                except Exception:
                    summary = "(checks summary not found)"
            print(f"  - checks: {summary[:200].replace('\n',' ')}...")
            shot2 = out_dir / f"pr-{pr}-checks.png"
            page.screenshot(path=str(shot2), full_page=True)

        context.close()
        browser.close()
    print(f"Screenshots saved to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
