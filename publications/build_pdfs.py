#!/usr/bin/env python3
"""
Minimal Markdown→PDF exporter for PaniniFS publications.

Order of attempts per source:
1) Pandoc → PDF using wkhtmltopdf or xelatex (if available)
2) Pandoc → HTML + Playwright (Chromium) → PDF (if Playwright available)
3) Pandoc → HTML only (print-ready fallback)

Targets root mirror files listed in publications/sources.yml.
Outputs to publications/out/.
"""
import subprocess
import sys
import os
import shutil
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "publications"
OUT = PUB / "out"
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = yaml.safe_load((PUB / "sources.yml").read_text())


def have(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def _pandoc_pdf_engine() -> str | None:
    # Prefer wkhtmltopdf if present (lighter than full LaTeX)
    if have("wkhtmltopdf"):
        return "wkhtmltopdf"
    if have("xelatex"):
        return "xelatex"
    return None


def export_via_pandoc(src: Path, out_pdf: Path) -> bool:
    if not have("pandoc"):
        return False
    engine = _pandoc_pdf_engine()
    if not engine:
        return False
    cmd = [
        "pandoc",
        str(src),
        "-o",
        str(out_pdf),
        f"--pdf-engine={engine}",
        "-V",
        "geometry:margin=1in",
    ]
    print("[pandoc]", " ".join(cmd))
    return subprocess.call(cmd) == 0


def export_html_via_pandoc(src: Path, out_html: Path, css: Path | None = None) -> bool:
    if not have("pandoc"):
        return False
    cmd = [
        "pandoc",
        str(src),
        "-o",
        str(out_html),
        "--from=markdown",
        "--to=html5",
        "--standalone",
        "--metadata",
        f"pagetitle={src.stem}",
    ]
    if css and css.exists():
        cmd += ["-c", str(css)]
    print("[pandoc-html]", " ".join(cmd))
    return subprocess.call(cmd) == 0


def export_pdf_via_playwright(html: Path, out_pdf: Path) -> bool:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except Exception as e:
        print(f"[skip] Playwright not available: {e}")
        return False
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(html.as_uri(), wait_until="load")
            page.emulate_media(media="print")
            page.pdf(path=str(out_pdf), print_background=True, margin={"top": "16mm", "bottom": "16mm", "left": "16mm", "right": "16mm"})
            browser.close()
        print(f"[ok] playwright {out_pdf}")
        return True
    except Exception as e:
        print(f"[fail] Playwright PDF for {html}: {e}")
        return False


def main() -> int:
    css = PUB / "print.css"
    pairs = []
    for kind, langs in SOURCES.items():
        for lang, rel in langs.items():
            src = ROOT / rel
            if not src.exists():
                print(f"[skip] missing {src}")
                continue
            out_pdf = OUT / f"{kind}_{lang}.pdf"
            out_html = OUT / f"{kind}_{lang}.html"
            # 1) Direct Pandoc -> PDF
            if export_via_pandoc(src, out_pdf):
                print(f"[ok] {out_pdf}")
                continue
            # 2) Pandoc -> HTML, then Playwright -> PDF
            ok_html = export_html_via_pandoc(src, out_html, css)
            if ok_html and export_pdf_via_playwright(out_html, out_pdf):
                continue
            # 3) Fallback: keep HTML for manual Print to PDF
            if ok_html:
                print(f"[ok] HTML fallback: {out_html} (use your browser: Print → Save as PDF)")
            else:
                print(
                    f"[fail] Could not produce HTML/PDF for {src}; install pandoc and optionally wkhtmltopdf or Playwright browsers."
                )
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
