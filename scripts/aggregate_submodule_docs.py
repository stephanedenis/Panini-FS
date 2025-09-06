#!/usr/bin/env python3
"""
Agrège les dossiers docs/ des sous-modules (modules/*) dans docs/modules/_ext/<module>/.
Ignorés: .git, node_modules, site, build, dist.
"""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
MODULES_DIR = ROOT / 'modules'
TARGET_ROOT = ROOT / 'docs' / 'modules' / '_ext'

EXCLUDES = {'.git', 'node_modules', 'site', 'build', 'dist', '.cache', '.venv'}


def copy_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    for item in src.iterdir():
        if item.name in EXCLUDES:
            continue
        if item.is_dir():
            copy_tree(item, dst / item.name)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst_file = dst if dst.suffix else (dst / item.name)  # defensive
            if dst.is_dir():
                dst_file = dst / item.name
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dst_file)


def main() -> int:
    if not MODULES_DIR.exists():
        print("No 'modules' directory found. Skipping aggregation.")
        return 0

    # Reset target directory
    if TARGET_ROOT.exists():
        shutil.rmtree(TARGET_ROOT)
    TARGET_ROOT.mkdir(parents=True, exist_ok=True)

    aggregated = []
    for mod in sorted(MODULES_DIR.iterdir()):
        if not mod.is_dir():
            continue
        docs_dir = mod / 'docs'
        if not docs_dir.exists():
            continue
        target = TARGET_ROOT / mod.name
        copy_tree(docs_dir, target)
        aggregated.append(mod.name)

    print(f"Aggregated {len(aggregated)} module(s): {', '.join(aggregated) if aggregated else '-'}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
