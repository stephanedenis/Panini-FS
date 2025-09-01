#!/usr/bin/env python3
"""
Prepare a Leanpub-friendly manuscript folder from root mirror files:
- Renders diagrams to SVG and replaces code fences with image links
- Copies assets and emits a manuscript/ with Book.txt

Assumptions:
- Root sources listed in publications/sources.yml
- Leanpub Markua-compatible Markdown is acceptable; diagrams are external SVGs
"""
from __future__ import annotations
import shutil
import re
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "publications"
OUT = PUB / "leanpub" / "manuscript"
DIAGS = PUB / "diagrams"

FENCE_RE = re.compile(r"```(mermaid|plantuml|puml)\n([\s\S]*?)\n```", re.MULTILINE)


def load_sources():
    return yaml.safe_load((PUB / "sources.yml").read_text())


def replace_fences_with_images(text: str) -> str:
    def _repl(m: re.Match[str]) -> str:
        kind = m.group(1)
        code = m.group(2).strip()
        import hashlib

        h = hashlib.sha1(f"{kind}\n{code}".encode("utf-8")).hexdigest()
        name = f"diag_{h}.svg"
        # Leanpub: standard Markdown image
        return f"\n![diagram]({name})\n"

    return FENCE_RE.sub(_repl, text)


def prepare():
    sources = load_sources()
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)
    DIAGS.mkdir(parents=True, exist_ok=True)

    # Render diagrams first
    md_files = []
    for kind, langs in sources.items():
        for lang, rel in langs.items():
            md_files.append(str((ROOT / rel).resolve()))
    # Import sibling module
    sys.path.insert(0, str(PUB))
    try:
        import render_diagrams  # type: ignore
    except Exception as e:
        print(f"[error] unable to import render_diagrams: {e}")
        return

    render_diagrams.main(md_files, str(DIAGS))

    # Copy and transform
    book_list = []
    for kind, langs in sources.items():
        for lang, rel in langs.items():
            src = ROOT / rel
            if not src.exists():
                print(f"[skip] missing {src}")
                continue
            text = src.read_text(encoding="utf-8")
            text = replace_fences_with_images(text)
            # Copy diagrams referenced
            for svg in DIAGS.glob("diag_*.svg"):
                shutil.copy2(svg, OUT / svg.name)
            # Write chapter file name
            out_name = f"{kind}_{lang}.md"
            (OUT / out_name).write_text(text, encoding="utf-8")
            book_list.append(out_name)

    # Emit Book.txt in rough order: FR then EN
    (OUT / "Book.txt").write_text("\n".join(book_list) + "\n", encoding="utf-8")
    print(f"[ok] Leanpub manuscript at {OUT}")


if __name__ == "__main__":
    prepare()
