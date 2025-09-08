#!/usr/bin/env python3
"""
Quick check to ensure the project does not depend on governance/copilotage.

Rules:
- No runtime/production code should import modules from governance/copilotage.
- No build/test/deploy critical scripts should reference governance/copilotage as a required path.

This is a best‑effort static scan. Use it as a pre‑commit hook or CI optional step.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COPI_PATH = ROOT / 'governance' / 'copilotage'

# Heuristics: treat these as production or critical areas to scan
PROD_GLOBS = [
    '*.py', '*.rs', '*.go', '*.ts', '*.tsx', '*.js', '*.jsx', '*.java', '*.kt',
    '*.sh', 'Makefile', 'Dockerfile', '*.yml', '*.yaml', 'pyproject.toml', 'package.json',
]

EXCLUDE_DIRS = {
    '.git', '.github', '.venv', 'venv', 'node_modules', 'governance/copilotage', 'docs', 'e2e', 'tests',
    'scripts',  # Exclude scripts directory to avoid self-reference
}

IMPORT_PATTERNS = [
    re.compile(r"from\s+governance\.copilotage(\.|\s|$)"),
    re.compile(r"import\s+governance\.copilotage(\.|\s|$)"),
]

PATH_PATTERNS = [
    re.compile(r"governance/copilotage"),
]

def iter_files():
    for p in ROOT.rglob('*'):
        if p.is_dir():
            # skip excluded dirs
            rel = p.relative_to(ROOT).as_posix()
            if rel in EXCLUDE_DIRS:
                # prune by skipping children
                for _ in []:
                    pass
                continue
            continue
        rel = p.relative_to(ROOT).as_posix()
        # skip excluded dirs by prefix
        if any(rel.startswith(d + '/') for d in EXCLUDE_DIRS):
            continue
        if any(p.match(glob) for glob in PROD_GLOBS):
            yield p

def main():
    if not COPI_PATH.exists():
        print("OK: governance/copilotage missing (nothing to check)")
        return 0

    offenders: list[tuple[str, str]] = []
    for f in iter_files():
        try:
            text = f.read_text(encoding='utf-8', errors='ignore')
        except (OSError, UnicodeDecodeError):
            continue
        for pat in IMPORT_PATTERNS:
            if pat.search(text):
                offenders.append((f.as_posix(), 'import'))
                break
        else:
            for pat in PATH_PATTERNS:
                if pat.search(text):
                    # allow references inside governance/copilotage itself
                    rel = f.relative_to(ROOT).as_posix()
                    if not rel.startswith('governance/copilotage/'):
                        offenders.append((f.as_posix(), 'path'))
                        break

    if offenders:
        print("FAIL: found potential dependencies on governance/copilotage:")
        for path, kind in offenders:
            print(f" - [{kind}] {path}")
        print("\nRemediation: move required assets out of copilotage or make them optional.")
        return 1
    print("OK: no production dependency on governance/copilotage detected.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
