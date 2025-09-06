#!/usr/bin/env python3
"""
Detect (and optionally fix) uppercase letters in tracked file paths.

Default is --check (non destructive). Use --fix to propose git mv renames.
Exceptions: common top-level files like README.md, LICENSE, SECURITY.md, CNAME, etc.
"""
from __future__ import annotations
import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXCEPTIONS = {
    'README.md', 'README.en.md', 'LICENSE', 'SECURITY.md', 'CNAME',
    'CODE_OF_CONDUCT.md', 'CONTRIBUTING.md', 'CONTRIBUTING.en.md',
}

# Do not auto-rename under these prefixes in --fix mode (phase 2 later)
EXCLUDE_PREFIXES = [
    'RESEARCH/', 'OPERATIONS/', 'SANDBOX/', 'SUBMODULES_TEMPLATE/',
    'TEST_WORKFLOW_OUTPUT/', 'DOCUMENTATION/', 'GOVERNANCE/', 'ECOSYSTEM/', 'CORE/',
    '.github/', 'docs/', 'modules/', 'Copilotage/', 'publications/',
]

def git_ls_files() -> list[str]:
    res = subprocess.run(['git', 'ls-files'], cwd=ROOT, stdout=subprocess.PIPE, text=True, check=True)
    return [line.strip() for line in res.stdout.splitlines() if line.strip()]

def to_kebab_lower(name: str) -> str:
    # Keep extension case as-is; convert basename to lowercase and replace spaces with '-'
    if '/' not in name:
        return name.lower()
    parts = name.split('/')
    new_parts = []
    for p in parts:
        if p in ('.git', '.github'):
            new_parts.append(p)
            continue
        new_parts.append(p.lower().replace(' ', '-'))
    return '/'.join(new_parts)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fix', action='store_true', help='apply git mv to enforce lowercase paths')
    ap.add_argument('--check', action='store_true', help='only check and exit non-zero if violations found (default)')
    args = ap.parse_args()
    check_mode = True if not args.fix else False
    uppercase_paths: list[str] = []

    for path in git_ls_files():
        if any(path.startswith(pref) for pref in ('.git/',)):
            continue
        base = Path(path).name
        if base in EXCEPTIONS:
            continue
        if re.search(r'[A-Z]', path):
            uppercase_paths.append(path)

    if not uppercase_paths:
        print('OK: no uppercase paths detected.')
        return 0

    if check_mode:
        print('Found uppercase paths:')
        for p in uppercase_paths:
            print(f' - {p}')
        print('\nTo fix locally: run this script with --fix (review diffs before commit).')
        return 1

    # fix mode: propose git mv
    for p in uppercase_paths:
        if any(p.startswith(pref) for pref in EXCLUDE_PREFIXES):
            print(f'Skip (excluded area): {p}')
            continue
        new_p = to_kebab_lower(p)
        if new_p == p:
            continue
        # Ensure parent exists
        new_parent = ROOT / new_p
        new_parent.parent.mkdir(parents=True, exist_ok=True)
        print(f'git mv "{p}" "{new_p}"')
        subprocess.run(['git', 'mv', p, new_p], cwd=ROOT, check=False)
    print('Renames attempted. Review with git status/diff.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
