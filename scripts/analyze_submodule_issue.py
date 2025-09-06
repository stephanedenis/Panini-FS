#!/usr/bin/env python3
"""
Analyze a GitHub issue to detect the primary submodule it belongs to and other impacted submodules.

Inputs:
  - --repo owner/repo and --issue NUMBER (requires GITHUB_TOKEN) OR
  - --input-file FILE (plain text content of the issue body)

Outputs:
  JSON to stdout with fields: {
    "title": str,
    "number": int|None,
    "labels": [str],
    "primary_submodule": str|None,
    "impacted_submodules": [str],
    "confidence": float,
    "evidence": { ... }
  }

Heuristics:
  1) Prefer explicit label: submodule:<name>
  2) Look for template field "Submodule path" or patterns matching submodule paths from .gitmodules
  3) Look for submodule repository URLs from .gitmodules
  4) As fallback, look for words matching submodule path last segments
  5) Impacted submodules = all additional matches besides the primary

No external dependencies required (uses stdlib only).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

try:
    from urllib.request import Request, urlopen
except ImportError:  # pragma: no cover
    Request = None  # type: ignore
    urlopen = None  # type: ignore


GITMODULES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".gitmodules")


@dataclass
class Submodule:
    name: str          # e.g. modules/semantic-core
    path: str          # same as name (path in worktree)
    url: str           # remote URL


def load_submodules(path: str = GITMODULES_PATH) -> List[Submodule]:
    subs: List[Submodule] = []
    if not os.path.exists(path):
        return subs
    current: Dict[str, str] = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("[submodule "):
                if current:
                    if "path" in current and "url" in current:
                        subs.append(Submodule(name=current.get("name", current["path"]), path=current["path"], url=current["url"]))
                current = {}
                # Extract name between quotes
                m = re.search(r'\"([^\"]+)\"', line)
                if m:
                    current["name"] = m.group(1)
            elif line.startswith("path = "):
                current["path"] = line.split("=", 1)[1].strip()
            elif line.startswith("url = "):
                current["url"] = line.split("=", 1)[1].strip()
        # last one
        if current:
            if "path" in current and "url" in current:
                subs.append(Submodule(name=current.get("name", current["path"]), path=current["path"], url=current["url"]))
    return subs


def github_get_issue(repo: str, number: int, token: str) -> Tuple[str, List[str], str]:
    api = f"https://api.github.com/repos/{repo}/issues/{number}"
    headers = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}", "X-GitHub-Api-Version": "2022-11-28"}
    req = Request(api, headers=headers)  # type: ignore[arg-type]
    with urlopen(req) as resp:  # type: ignore[arg-type]
        data = json.loads(resp.read().decode("utf-8"))
    title = data.get("title", "")
    labels = [l.get("name", "") for l in data.get("labels", []) if isinstance(l, dict)]
    body = data.get("body", "") or ""
    return title, labels, body


def build_patterns(subs: List[Submodule]) -> Dict[str, Dict[str, re.Pattern]]:
    patterns: Dict[str, Dict[str, re.Pattern]] = {}
    for s in subs:
        key = normalize_key(s)
        # exact path occurrence
        path_pat = re.compile(rf"(?<![\w/]){re.escape(s.path)}(?![\w/])")
        # url occurrence (handle SSH and HTTPS variants)
        url_core = s.url.replace("git@github.com:", "https://github.com/")
        url_core = re.sub(r"\.git$", "", url_core)
        url_pat = re.compile(re.escape(url_core))
        # last segment alias
        last_seg = s.path.split("/")[-1]
        last_pat = re.compile(rf"(?<![\w/]){re.escape(last_seg)}(?![\w/])")
        patterns[key] = {"path": path_pat, "url": url_pat, "alias": last_pat}
    return patterns


def normalize_key(s: Submodule) -> str:
    # Prefer path last segment as key, with dashes
    return s.path.split("/")[-1].lower()


def analyze_text(text: str, labels: List[str], subs: List[Submodule]) -> Tuple[Optional[str], List[str], float, Dict[str, List[str]]]:
    patterns = build_patterns(subs)
    evidence: Dict[str, List[str]] = {"labels": [], "path": [], "url": [], "alias": [], "template": []}
    keys_by_label = []
    # Label-based hint: submodule:<key>
    for lb in labels:
        m = re.match(r"submodule:([a-z0-9._\-]+)", lb.strip().lower())
        if m:
            keys_by_label.append(m.group(1))
            evidence["labels"].append(lb)

    # Template field: Submodule path
    for line in text.splitlines():
        if line.strip().lower().startswith("submodule path"):
            # ex: "Submodule path (as in .gitmodules): modules/semantic-core"
            path = line.split(":", 1)[-1].strip()
            if path:
                evidence["template"].append(path)

    matches: Dict[str, int] = {}
    for s in subs:
        key = normalize_key(s)
        pts = 0
        # Path exact
        if patterns[key]["path"].search(text):
            pts += 3
            evidence["path"].append(s.path)
        # URL
        if patterns[key]["url"].search(text):
            pts += 3
            evidence["url"].append(s.url)
        # Alias
        if patterns[key]["alias"].search(text):
            pts += 1
            evidence["alias"].append(key)
        # Template override
        if any(s.path in t for t in evidence["template"]):
            pts += 4
        if key in keys_by_label:
            pts += 5
        if pts:
            matches[key] = pts

    if not matches and not keys_by_label and not evidence["template"]:
        return None, [], 0.0, evidence

    # Determine primary by highest score; tie-breaker: template > label > path > alias
    def score_tuple(k: str) -> Tuple[int, int, int, int, int]:
        pts = matches.get(k, 0)
        has_tmpl = int(any(pat for pat in evidence["template"] if k in pat or pat.endswith("/" + k)))
        has_label = int(k in keys_by_label)
        has_path = int(safe_contains(evidence["path"], k))
        has_alias = int(k in evidence["alias"])
        return (pts, has_tmpl, has_label, has_path, has_alias)

    primary = None
    if matches:
        primary = max(matches.keys(), key=score_tuple)
    elif keys_by_label:
        primary = keys_by_label[0]

    impacted = sorted([k for k in matches.keys() if k != primary])

    # Confidence: normalize roughly by max possible ~ 5 (label) + 4 (template) + 3 (path) + 3 (url) + 1 (alias) = 16
    max_possible = 16.0
    conf = min(1.0, (matches.get(primary or "", 0)) / max_possible) if primary else 0.0
    return primary, impacted, conf, evidence


def safe_contains(paths: List[str], key: str) -> bool:
    for p in paths:
        if p.split("/")[-1].lower() == key.lower():
            return True
    return False


def main() -> None:
    ap = argparse.ArgumentParser(description="Analyze issue text to determine submodule ownership and impact.")
    ap.add_argument("--repo", help="owner/repo (required with --issue)")
    ap.add_argument("--issue", type=int, help="issue number to fetch via GitHub API")
    ap.add_argument("--input-file", help="analyze a local text file instead of calling the API")
    ap.add_argument("--print-evidence", action="store_true", help="include evidence details in output")
    args = ap.parse_args()

    if not os.path.exists(GITMODULES_PATH):
        print(json.dumps({"error": ".gitmodules not found"}))
        sys.exit(0)

    subs = load_submodules(GITMODULES_PATH)
    if not subs:
        print(json.dumps({"error": "no submodules found"}))
        sys.exit(0)

    title = ""
    labels: List[str] = []
    body = ""
    number: Optional[int] = None

    if args.input_file:
        with open(args.input_file, "r", encoding="utf-8") as f:
            body = f.read()
        title = os.path.basename(args.input_file)
    else:
        if not (args.repo and args.issue):
            print("Either --input-file or both --repo and --issue must be provided", file=sys.stderr)
            sys.exit(2)
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if not token:
            print("GITHUB_TOKEN or GH_TOKEN must be set to call the GitHub API", file=sys.stderr)
            sys.exit(2)
        title, labels, body = github_get_issue(args.repo, args.issue, token)
        number = args.issue

    primary, impacted, conf, evidence = analyze_text(body, labels, subs)

    # Build normalized label suggestions
    def map_key_to_label(k: str) -> str:
        alias = {
            "shared": "copilotage-shared",
        }
        return f"submodule:{alias.get(k, k)}"

    primary_label = map_key_to_label(primary) if primary else None
    impacted_labels = [map_key_to_label(k) for k in impacted]

    out: Dict[str, object] = {
        "title": title,
        "number": number,
        "labels": labels,
        "primary_submodule": primary,
        "primary_label": primary_label,
        "impacted_submodules": impacted,
        "impacted_labels": impacted_labels,
        "confidence": round(conf, 3),
    }
    if args.print_evidence:
        out["evidence"] = evidence  # type: ignore[assignment]
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
