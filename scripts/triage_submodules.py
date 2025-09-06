#!/usr/bin/env python3
"""
Backfill submodule triage across existing GitHub issues.

Usage:
  triage_submodules.py --repo owner/repo [--state open|all|closed] [--max 500] [--since 2025-01-01] [--dry-run]

Requires:
  - GITHUB_TOKEN or GH_TOKEN environment variable with repo scope.

Behavior:
  - Fetch issues (not PRs) via GitHub REST API with pagination.
  - Analyze each issue using analyze_submodule_issue heuristics.
  - Ensure labels exist, add recommended labels, and comment a summary.
  - If --dry-run, only prints actions.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Dict, List, Optional

from analyze_submodule_issue import (
    analyze_text,
    load_submodules,
)

from urllib.request import Request, urlopen
from urllib.error import HTTPError


API_ROOT = "https://api.github.com"


def gh_get(url: str, token: str) -> Dict:
    req = Request(url, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "submodule-triage"
    })
    with urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def gh_post(url: str, token: str, payload: Dict) -> Dict:
    data = json.dumps(payload).encode("utf-8")
    req = Request(url, data=data, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
        "User-Agent": "submodule-triage"
    })
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"POST {url} failed: {e.code} {e.reason} {body}") from e


def ensure_label(repo: str, name: str, token: str, color: str = "f9d0c4", description: str = "") -> None:
    url = f"{API_ROOT}/repos/{repo}/labels"
    try:
        gh_post(url, token, {"name": name, "color": color, "description": description})
    except RuntimeError as e:
        # 422 indicates already exists; ignore
        if "422" not in str(e):
            raise


def add_labels(repo: str, issue_number: int, labels: List[str], token: str) -> None:
    url = f"{API_ROOT}/repos/{repo}/issues/{issue_number}/labels"
    gh_post(url, token, {"labels": labels})


def add_comment(repo: str, issue_number: int, body: str, token: str) -> None:
    url = f"{API_ROOT}/repos/{repo}/issues/{issue_number}/comments"
    gh_post(url, token, {"body": body})


def list_issues(repo: str, token: str, state: str, since: Optional[str], max_items: int) -> List[Dict]:
    issues: List[Dict] = []
    page = 1
    while True:
        params = [f"state={state}", "per_page=100", f"page={page}"]
        if since:
            params.append(f"since={since}")
        url = f"{API_ROOT}/repos/{repo}/issues?{'&'.join(params)}"
        batch = gh_get(url, token)
        if not isinstance(batch, list) or not batch:
            break
        for it in batch:
            if "pull_request" in it:
                continue  # skip PRs
            issues.append(it)
            if len(issues) >= max_items:
                return issues
        page += 1
    return issues


def main() -> None:
    ap = argparse.ArgumentParser(description="Backfill submodule triage across existing GitHub issues")
    ap.add_argument("--repo", required=True, help="owner/repo")
    ap.add_argument("--state", default="open", choices=["open", "all", "closed"], help="issue state to scan")
    ap.add_argument("--max", type=int, default=500, help="maximum number of issues to process")
    ap.add_argument("--since", help="ISO datetime filter (e.g., 2025-01-01T00:00:00Z or 2025-01-01)")
    ap.add_argument("--dry-run", action="store_true", help="only print actions without applying changes")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print("GITHUB_TOKEN or GH_TOKEN is required", file=sys.stderr)
        sys.exit(2)

    subs = load_submodules()
    if not subs:
        print("No submodules found in .gitmodules", file=sys.stderr)
        sys.exit(1)

    issues = list_issues(args.repo, token, args.state, args.since, args.max)
    print(f"Found {len(issues)} issues to analyze")

    # Ensure base labels exist
    ensure_label(args.repo, "target:submodule", token, color="1d76db", description="Change lives in a submodule (external repo)")
    ensure_label(args.repo, "type:submodule-change", token, color="c2e0c6", description="Request to change a submodule and update pointer here")

    # Ensure per-submodule labels (best-effort)
    for s in subs:
        key = s.path.split("/")[-1].lower()
        alias = "copilotage-shared" if key == "shared" else key
        ensure_label(args.repo, f"submodule:{alias}", token)

    total_labeled = 0
    for it in issues:
        num_val = it.get("number")
        if not isinstance(num_val, int):
            continue
        num = num_val
        title = it.get("title", "")
        body = it.get("body", "") or ""
        labels = [l.get("name", "") for l in it.get("labels", [])]

        primary, impacted, conf, _ = analyze_text(body, labels, subs)
        if not primary and not impacted:
            continue

        primary_label = f"submodule:{'copilotage-shared' if (primary or '') == 'shared' else (primary or '')}" if primary else None
        impacted_labels = [f"submodule:{'copilotage-shared' if k=='shared' else k}" for k in impacted]

        to_add = set(["target:submodule", "type:submodule-change"]) | set(filter(None, [primary_label])) | set(impacted_labels)

        msg = f"Submodule triage → primary: {primary or 'n/a'}, impacted: {', '.join(impacted) or 'none'}, confidence: {round(conf, 3)}"

        print(f"Issue #{num}: {title}\n  + Labels: {sorted(to_add)}\n  + Comment: {msg}")
        if args.dry_run:
            continue

        # Ensure labels (again) then add only missing ones
        for lb in to_add:
            ensure_label(args.repo, lb, token)
        existing = set(labels)
        missing = sorted(to_add - existing)
        if missing:
            add_labels(args.repo, num, missing, token)
            add_comment(args.repo, num, msg, token)
            total_labeled += 1

    print(f"Applied triage to {total_labeled} issues (state={args.state}, dry_run={args.dry_run})")


if __name__ == "__main__":
    main()
