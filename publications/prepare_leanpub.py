#!/usr/bin/env python3
"""
Prepare Leanpub-friendly manuscript folders from root mirror files, per language (FR/EN):
- Renders diagrams to SVG and replaces code fences with image links
- Splits the book into chapters (by H1) if requested
- Copies assets and emits manuscript_fr/ and manuscript_en/ with Book.txt

Assumptions:
- Root sources listed in publications/sources.yml
- Leanpub Markua-compatible Markdown is acceptable; diagrams are external SVGs
"""
from __future__ import annotations
import shutil
import re
from pathlib import Path
import sys
import argparse
import unicodedata
from typing import Any
import importlib
yaml: Any = importlib.import_module("yaml")

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "publications"
# We create two parallel outputs: manuscript_fr and manuscript_en
OUT_ROOT = PUB / "leanpub"
OUT_FR = OUT_ROOT / "manuscript_fr"
OUT_EN = OUT_ROOT / "manuscript_en"
DIAGS = PUB / "diagrams"

FENCE_RE = re.compile(r"```(mermaid|plantuml|puml)\n([\s\S]*?)\n```", re.MULTILINE)


def load_sources() -> Any:
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

def slugify(title: str) -> str:
    # ASCII-only, hyphen-separated
    t = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    t = re.sub(r"[^a-zA-Z0-9\s-]", "", t)
    t = re.sub(r"\s+", "-", t).strip("-")
    return t.lower() or "section"


def split_by_h1(text: str) -> list[tuple[str, str]]:
    # Split on lines starting with '# ' and keep headings
    lines = text.splitlines()
    parts: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if line.startswith("# "):
            if current:
                parts.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        parts.append(current)
    chapters: list[tuple[str, str]] = []
    for i, chunk in enumerate(parts, 1):
        heading = "Untitled"
        if chunk and chunk[0].startswith("# "):
            heading = chunk[0][2:].strip()
        slug = slugify(heading)
        fname = f"ch{str(i).zfill(2)}-{slug}.md"
        chapters.append((fname, "\n".join(chunk).strip() + "\n"))
    return chapters


def prepare(split_chapters: bool = True, include_articles: bool = True):
    sources = load_sources()
    # Fresh outputs
    for out_dir in (OUT_FR, OUT_EN):
        if out_dir.exists():
            shutil.rmtree(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
    DIAGS.mkdir(parents=True, exist_ok=True)

    # Render diagrams once from all sources
    md_files = [str((ROOT / rel).resolve()) for langs in sources.values() for rel in langs.values()]
    sys.path.insert(0, str(PUB))
    try:
        import render_diagrams  # type: ignore
    except ImportError as e:
        print(f"[error] unable to import render_diagrams: {e}")
        return
    render_diagrams.main(md_files, str(DIAGS))

    # Helper to process a language
    def process_lang(lang: str, out_dir: Path) -> None:
        book_files: list[str] = []
        # Copy diagrams
        for svg in DIAGS.glob("diag_*.svg"):
            shutil.copy2(svg, out_dir / svg.name)
        # Books
        if "books" in sources and lang in sources["books"]:
            src = ROOT / sources["books"][lang]
            if src.exists():
                text = replace_fences_with_images(src.read_text(encoding="utf-8"))
                if split_chapters:
                    chapters = split_by_h1(text)
                    for fname, content in chapters:
                        (out_dir / fname).write_text(content, encoding="utf-8")
                        book_files.append(fname)
                else:
                    name = f"book_{lang}.md"
                    (out_dir / name).write_text(text, encoding="utf-8")
                    book_files.append(name)
        # Articles (optional)
        if include_articles and "articles" in sources and lang in sources["articles"]:
            src = ROOT / sources["articles"][lang]
            if src.exists():
                text = replace_fences_with_images(src.read_text(encoding="utf-8"))
                name = f"article_{lang}.md"
                (out_dir / name).write_text(text, encoding="utf-8")
                book_files.append(name)
        # Emit Book.txt
        (out_dir / "Book.txt").write_text("\n".join(book_files) + "\n", encoding="utf-8")
        print(f"[ok] Book.txt ({lang}) with {len(book_files)} entries")

    process_lang("fr", OUT_FR)
    process_lang("en", OUT_EN)
    print(f"[ok] Leanpub manuscripts at {OUT_FR} and {OUT_EN}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-split", dest="split", action="store_false", help="Do not split into chapters")
    ap.add_argument("--no-articles", dest="articles", action="store_false", help="Do not include articles in Book.txt")
    args = ap.parse_args()
    prepare(split_chapters=args.split, include_articles=args.articles)
