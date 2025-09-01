# Publications Toolkit

This folder hosts helper scripts and metadata for generating public artifacts:

- Draft PDFs (books/articles) for review
- Mirrors to Leanpub/Medium source files
- Future automation (publication-engine integration)

## Layout

- `build_pdfs.py` — quick-and-dirty Markdown→PDF exporter (Playwright/Pandoc fallback)
- `render_diagrams.py` — pre-render Mermaid/PlantUML code fences to SVG
- `prepare_leanpub.py` — create `leanpub/manuscript/` folder with Book.txt
- `print.css` — print-friendly CSS for HTML fallbacks
- `sources.yml` — mapping to root source files
- `requirements.txt` — minimal Python deps for the toolkit

## Install

- Python deps (in a venv recommended):
  - `pip install -r publications/requirements.txt`
- Optional binaries:
  - `pandoc` + `wkhtmltopdf` (or `xelatex`) for direct PDF
  - `mmdc` (mermaid-cli) and/or `plantuml` for local diagram rendering
  - Or set `KROKI_URL` to use a Kroki server
  - For Playwright PDF: run `playwright install --with-deps` once

## Usage

- Pre-render diagrams and prepare Leanpub manuscript:
  - `python3 publications/prepare_leanpub.py`
  - Output: `publications/leanpub/manuscript/` with `Book.txt` and SVG diagrams

- Generate review PDFs (tries Pandoc, else HTML + Playwright, else HTML only):
  - `python3 publications/build_pdfs.py`
  - Output: `publications/out/` files: `books_fr.pdf`, `books_en.pdf`, `articles_fr.pdf`, `articles_en.pdf` (or `.html` fallbacks)

## Notes

- Markua compatibility: regular Markdown is fine. Diagrams are embedded as external SVGs for Leanpub.
- For MkDocs site, diagrams continue to render via Material/Kroki; this toolkit is for export pipelines.
