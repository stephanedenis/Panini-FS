#!/usr/bin/env python3
"""
VS Code settings tuner (Linux focus).

Safely adjusts user-level VS Code settings to reduce confirmation prompts and
improve non-interactive workflows for this project. Creates a timestamped backup
before applying any change.

Targets (detected automatically):
- Code (stable)
- Code - Insiders
- VSCodium
- Code - OSS
- code-server

Usage:
- Dry-run by default (prints the planned changes).
- Pass --apply to write changes.
- Pass --targets to restrict which installations to touch (comma-separated).
"""
from __future__ import annotations
import argparse
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List

HOME = Path.home()

@dataclass
class VSCodeInstall:
    name: str
    settings_path: Path

    def exists(self) -> bool:
        return self.settings_path.exists()


def candidate_installs() -> List[VSCodeInstall]:
    candidates = [
        VSCodeInstall("code", HOME / ".config/Code/User/settings.json"),
        VSCodeInstall("insiders", HOME / ".config/Code - Insiders/User/settings.json"),
        VSCodeInstall("vscodium", HOME / ".config/VSCodium/User/settings.json"),
        VSCodeInstall("oss", HOME / ".config/Code - OSS/User/settings.json"),
        VSCodeInstall("codeserver", HOME / ".local/share/code-server/User/settings.json"),
    ]
    return [c for c in candidates if c.settings_path.parent.exists()]


def strip_json_comments(text: str) -> str:
    # Remove /* ... */ block comments
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    # Remove // line comments (not robust for URLs-in-strings, but settings are simple)
    text = re.sub(r"^\s*//.*$", "", text, flags=re.M)
    return text


def load_settings(path: Path) -> Dict:
    if not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8")
    try:
        return json.loads(strip_json_comments(raw))
    except json.JSONDecodeError:
        # Fallback to empty if parsing fails; we keep backup anyway before write
        return {}


def ensure_keys(settings: Dict) -> Dict:
    desired = {
        # Allow automatic tasks without prompts
        "task.allowAutomaticTasks": "on",
        # Reduce terminal/exit confirmations
        "terminal.integrated.confirmOnExit": "never",
        # Trust: open files even if workspace not yet trusted (reduces friction)
        "security.workspace.trust.untrustedFiles": "open",
        # Don't ask before closing the window
        "window.confirmBeforeClose": "never",
        # Git prompts
        "git.confirmSync": False,
    }
    updated = dict(settings)
    for k, v in desired.items():
        if updated.get(k) != v:
            updated[k] = v
    return updated


def backup(path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = path.with_suffix(path.suffix + f".bak.{ts}")
    if path.exists():
        shutil.copy2(path, backup_path)
    return backup_path


def write_settings(path: Path, data: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    path.write_text(text, encoding="utf-8")


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="Tune VS Code user settings to reduce confirmations.")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default is dry-run)")
    parser.add_argument("--targets", type=str, default="",
                        help="Comma-separated subset of targets: code,insiders,vscodium,oss,codeserver (default: all detected)")
    args = parser.parse_args(argv)

    installs = candidate_installs()
    if args.targets:
        wanted = {t.strip() for t in args.targets.split(",") if t.strip()}
        installs = [i for i in installs if i.name in wanted]

    if not installs:
        print("No VS Code installations detected under ~/.config or ~/.local/share.")
        return 0

    changes = 0
    for inst in installs:
        spath = inst.settings_path
        cur = load_settings(spath)
        new = ensure_keys(cur)
        if cur == new:
            print(f"[{inst.name}] No changes needed: {spath}")
            continue
        print(f"[{inst.name}] Will update: {spath}")
        diff_keys = [k for k in new.keys() if cur.get(k) != new.get(k)]
        for k in diff_keys:
            print(f"  - {k}: {cur.get(k)!r} -> {new.get(k)!r}")
        if args.apply:
            spath.parent.mkdir(parents=True, exist_ok=True)
            backup(spath)
            write_settings(spath, new)
            print(f"[{inst.name}] Updated and backed up previous settings.json")
        changes += 1

    if not args.apply and changes:
        print("\nDry-run only. Re-run with --apply to write changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
