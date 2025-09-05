---
title: OntoWave — Vision and role in the ecosystem
---

# OntoWave — Vision and role in the ecosystem

OntoWave is the semantic browser and client-side Markdown reader of the PaniniFS ecosystem. Its mission is to make knowledge navigable, alive, and interoperable: a lightweight front-end that connects documents, concepts, and semantic graphs into a smooth experience.

## Why a separate project?

- Loose coupling: OntoWave evolves at its own pace (web app) while PaniniFS remains the documentation/conceptual backbone (MkDocs + Pages).
- Portability: Static Vite + TypeScript app, deployable anywhere (Pages, S3, CDN, offline).
- Extensibility: Reusable core for extensions (VS Code, browser, Azure DevOps) without bloating PaniniFS.

## Core capabilities (current MVP)

- Fast Markdown rendering (markdown-it) with anchors, footnotes, link attributes.
- Rich syntaxes: code (highlight.js), formulas (KaTeX), diagrams (Mermaid).
- Hash routing (/#/path) for static hosting.
- Configurable content sources via `public/config.json` and a generated `sitemap.json`.

## Mid-term vision

- Semantic navigation (concept anchors, backlinks, concept maps).
- Contextual search and filters (tags, entities, relations, temporality).
- Offline/edge-first mode, local and incremental index.
- Extension kits: 
  - VS Code extension (semantic editor, synced preview),
  - Web extension (page enrichment),
  - CI integration (semantic lint, broken links, graph diff) and Azure DevOps.

## Role within PaniniFS

- PaniniFS publishes and structures the corpus (strict MkDocs, i18n, workflows, research RSS).
- OntoWave provides exploratory and semantic reading on top of this corpus and other sources.
- Both stay decoupled: PaniniFS references OntoWave, but does not build it in the Pages pipeline.

## Planned integrations

- Cross-links from PaniniFS pages to OntoWave views (e.g., concept maps).
- Expose a `sitemap.json` and metadata (frontmatter) for OntoWave to index.
- Eventually, a “knowledge graph” connector to bridge Dhātu, semantic universals, and navigation facets.

### Recommended pattern in submodules

- Serve the OntoWave SPA as `index.html` at the root of the module's `docs/` folder.
- Static docs (Markdown) stay in `docs/` for MkDocs aggregation; the SPA provides dynamic navigation on the same corpus.
- No build coupling in PaniniFS: submodules own their SPA lifecycle.

## References

- OntoWave repo: https://github.com/stephanedenis/OntoWave
- License and CI: lint, type-check, build, PR artifacts.

Status: autonomous MVP (green CI), progressive roadmap. All contributions go through the OntoWave repository.
