#!/usr/bin/env python3
"""
Render Mermaid and PlantUML code fences from Markdown into SVG files.

Resolution order per diagram type:
- Mermaid: mermaid-cli (mmdc) → Kroki (if KROKI_URL set) → skip with message
- PlantUML: plantuml (or java -jar plantuml.jar) → Kroki (if KROKI_URL set) → skip

Outputs SVGs named by SHA1 of content into a target images directory.

Usage (internal): invoked by prepare_leanpub.py, but can be run standalone too.
"""
from __future__ import annotations
import re
import os
import hashlib
import subprocess
from pathlib import Path
from typing import Optional

try:
    import requests  # type: ignore
except Exception:
    requests = None  # optional; only used with Kroki


FENCE_RE = re.compile(r"```(mermaid|plantuml|puml)\n([\s\S]*?)\n```", re.MULTILINE)


def sha1(data: str) -> str:
    return hashlib.sha1(data.encode("utf-8")).hexdigest()


def have(cmd: str) -> bool:
    from shutil import which
    return which(cmd) is not None


def render_mermaid_to_svg(code: str, out_svg: Path) -> bool:
    # Try mermaid-cli (mmdc)
    if have("mmdc"):
        tmp = out_svg.with_suffix(".mmd")
        tmp.write_text(code, encoding="utf-8")
        cmd = [
            "mmdc",
            "-i",
            str(tmp),
            "-o",
            str(out_svg),
            "-b",
            "transparent",
        ]
        print("[mmdc]", " ".join(cmd))
        ok = subprocess.call(cmd) == 0
        try:
            tmp.unlink()
        except Exception:
            pass
        if ok:
            return True
    # Fallback: Kroki
    kroki = os.environ.get("KROKI_URL")
    if kroki and requests is not None:
        try:
            url = f"{kroki.rstrip('/')}/mermaid/svg"
            resp = requests.post(url, data=code.encode("utf-8"), timeout=30)
            if resp.ok:
                out_svg.write_bytes(resp.content)
                print(f"[kroki] {out_svg}")
                return True
            else:
                print(f"[kroki] HTTP {resp.status_code}: {resp.text[:120]}")
        except Exception as e:
            print(f"[kroki] error: {e}")
    print("[skip] Mermaid rendering not available (install mermaid-cli or set KROKI_URL)")
    return False


def render_plantuml_to_svg(code: str, out_svg: Path) -> bool:
    # Try plantuml CLI
    if have("plantuml"):
        tmp = out_svg.with_suffix(".puml")
        tmp.write_text(code, encoding="utf-8")
        cmd = ["plantuml", "-tsvg", str(tmp)]
        print("[plantuml]", " ".join(cmd))
        ok = subprocess.call(cmd) == 0
        if ok:
            # plantuml writes alongside input
            gen = tmp.with_suffix(".svg")
            if gen.exists():
                gen.replace(out_svg)
                try:
                    tmp.unlink()
                except Exception:
                    pass
                return True
    # Fallback: Kroki
    kroki = os.environ.get("KROKI_URL")
    if kroki and requests is not None:
        try:
            url = f"{kroki.rstrip('/')}/plantuml/svg"
            resp = requests.post(url, data=code.encode("utf-8"), timeout=30)
            if resp.ok:
                out_svg.write_bytes(resp.content)
                print(f"[kroki] {out_svg}")
                return True
            else:
                print(f"[kroki] HTTP {resp.status_code}: {resp.text[:120]}")
        except Exception as e:
            print(f"[kroki] error: {e}")
    print("[skip] PlantUML rendering not available (install plantuml or set KROKI_URL)")
    return False


def extract_and_render(md_path: Path, images_dir: Path) -> dict[str, str]:
    images_dir.mkdir(parents=True, exist_ok=True)
    content = md_path.read_text(encoding="utf-8")
    mapping: dict[str, str] = {}
    for m in FENCE_RE.finditer(content):
        kind = m.group(1)
        code = m.group(2).strip()
        h = sha1(f"{kind}\n{code}")
        out_svg = images_dir / f"diag_{h}.svg"
        if out_svg.exists():
            mapping[m.group(0)] = out_svg.name
            continue
        ok = False
        if kind == "mermaid":
            ok = render_mermaid_to_svg(code, out_svg)
        else:
            ok = render_plantuml_to_svg(code, out_svg)
        if ok:
            mapping[m.group(0)] = out_svg.name
    return mapping


def main(md_files: list[str], images_dir: str) -> int:
    out_dir = Path(images_dir)
    for f in md_files:
        p = Path(f)
        if not p.exists():
            print(f"[skip] {p} not found")
            continue
        mapping = extract_and_render(p, out_dir)
        print(f"[done] {p}: {len(mapping)} diagram(s) rendered")
    return 0


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--images-dir", default="publications/diagrams", help="Output dir for SVGs")
    ap.add_argument("md", nargs="+", help="Markdown files to scan")
    args = ap.parse_args()
    raise SystemExit(main(args.md, args.images_dir))
