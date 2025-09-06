#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ecosystem.yml"
OUT_DIR = ROOT / "docs" / "ecosystem"
REPOS_DIR = OUT_DIR / "repos"


def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_out():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPOS_DIR.mkdir(parents=True, exist_ok=True)


def _iter_all_repos(data: dict):
    """Yield tuples (category, item) for root, submodules, external."""
    root = data.get("root_repo") or {}
    if root:
        yield ("root", root)
    for m in data.get("submodules") or []:
        yield ("submodule", m)
    for m in data.get("external") or []:
        yield ("external", m)


def _repo_display_label(item: dict, fallback_key: str | None = None) -> str:
    name = item.get("name") or fallback_key or item.get("key") or ""
    role = item.get("role")
    if role:
        return f"{name} ({role})"
    return name


def _repo_page_filename(item: dict) -> str:
    key = item.get("key") or (item.get("name", "").lower().replace(" ", "-")) or "repo"
    return f"{key}.md"


def render_catalog(data: dict) -> str:
    lines = ["# Écosystème Panini — Catalogue des dépôts", ""]
    root = data.get("root_repo", {})
    # Lien vers page détaillée locale + lien externe GitHub
    if root:
        root_page = _repo_page_filename({"key": "root"})
        gh = root.get("url", "")
        lines.append(
            f"- Dépôt maître: [{root.get('name','PaniniFS')}](/ecosystem/repos/{root_page}) "
            + (f"([GitHub]({gh}))" if gh else "")
            + f" — {root.get('description','')}"
        )
    lines.append("")
    if data.get("submodules"):
        lines.append("## Modules principaux")
        for m in data["submodules"]:
            page = _repo_page_filename(m)
            gh = m.get("url", "")
            lines.append(
                f"- [{m['name']}](/ecosystem/repos/{page}) "
                + (f"([GitHub]({gh}))" if gh else "")
                + f" — rôle: {m.get('role','-')} — {m.get('description','')}"
            )
        lines.append("")
    if data.get("external"):
        lines.append("## Dépôts externes intégrés (submodules)")
        for m in data["external"]:
            page = _repo_page_filename(m)
            gh = m.get("url", "")
            lines.append(
                f"- [{m['name']}](/ecosystem/repos/{page}) "
                + (f"([GitHub]({gh}))" if gh else "")
                + f" — rôle: {m.get('role','-')} — {m.get('description','')}"
            )
        lines.append("")
    lines.append(
        "> Note: ce catalogue est généré depuis `data/ecosystem.yml` (documentation-first)."
    )
    return "\n".join(lines) + "\n"


def render_overview(data: dict) -> str:
    lines = ["# Écosystème Panini — Panorama & relations", ""]
    lines.append("Ce panorama résume les dépendances et influences entre les dépôts.")
    lines.append("")
    # Diagramme Mermaid généré automatiquement
    lines.append("```mermaid")
    lines.append("graph TD")
    # Nodes
    key_to_id: dict[str, str] = {}
    idx = 0
    for cat, item in _iter_all_repos(data):
        idx += 1
        key = item.get("key") or ("root" if cat == "root" else f"node{idx}")
        label = _repo_display_label(item, fallback_key=key)
        node_id = key.replace("-", "_")
        key_to_id[key] = node_id
        style = {
            "root": ":::root",
            "submodule": ":::module",
            "external": ":::external",
        }.get(cat, "")
        lines.append(f"  {node_id}[{label}] {style}")
    # Edges
    # Always connect root to others (if present)
    root_key = "root"
    root_id = key_to_id.get(root_key)
    if root_id:
        for k, nid in key_to_id.items():
            if k != root_key:
                lines.append(f"  {root_id} --> {nid}")
    # Declared relations
    for rel in data.get("relations", []) or []:
        src = rel.get("from")
        tos = rel.get("to") or []
        if src in key_to_id:
            for t in tos:
                if t in key_to_id:
                    lines.append(f"  {key_to_id[src]} --> {key_to_id[t]}")
    # Simple styles (Material Mermaid themes support classDef)
    lines.append("  classDef root fill:#2b90d9,stroke:#1b5b8a,color:#fff;")
    lines.append("  classDef module fill:#d9f0ff,stroke:#2b90d9,color:#000;")
    lines.append("  classDef external fill:#f9f1d9,stroke:#c49f34,color:#000;")
    lines.append("```")
    lines.append("")
    lines.append("## Relations (haut niveau)")
    rels = data.get("relations", [])
    if not rels:
        lines.append("(Aucune relation déclarée)")
    else:
        for r in rels:
            src = r.get("from")
            tos = r.get("to", [])
            lines.append(f"- {src} → {', '.join(tos)}")
    lines.append("")
    lines.append(
        "> Note: ces relations sont déclaratives et évolutives — modifiez `data/ecosystem.yml`."
    )
    return "\n".join(lines) + "\n"


def render_repo_page(item: dict, category: str) -> str:
    name = item.get("name", item.get("key", "(sans nom)"))
    url = item.get("url", "")
    docs_url = item.get("docs_url") or item.get("docs")
    path = item.get("path", "")
    role = item.get("role", "-")
    desc = item.get("description", "")
    # Champs optionnels futurs
    status = item.get("status")
    tags = item.get("tags")
    langs = item.get("languages")
    contact = item.get("contact")
    lines = [f"# {name}", ""]
    if desc:
        lines.append(desc)
        lines.append("")
    lines.append(f"- Catégorie: {category}")
    if role:
        lines.append(f"- Rôle: {role}")
    if path:
        lines.append(f"- Chemin dans ce repo: `{path}`")
    if url:
        lines.append(f"- Dépôt source: {url}")
    if docs_url:
        lines.append(f"- Documentation: {docs_url}")
    if status:
        lines.append(f"- Statut: {status}")
    if langs:
        lines.append(f"- Langages: {', '.join(langs)}")
    if tags:
        lines.append(f"- Tags: {', '.join(tags)}")
    if contact:
        lines.append(f"- Contact: {contact}")
    lines.append("")
    lines.append(
        "> Page générée automatiquement depuis `data/ecosystem.yml`. Éditez la source pour mettre à jour."
    )
    return "\n".join(lines) + "\n"


def main():
    data = load_yaml(DATA)
    ensure_out()
    (OUT_DIR / "catalogue.md").write_text(render_catalog(data), encoding="utf-8")
    (OUT_DIR / "panorama.md").write_text(render_overview(data), encoding="utf-8")
    # Générer pages de détail
    generated = [str(OUT_DIR / "catalogue.md"), str(OUT_DIR / "panorama.md")]
    for category, item in _iter_all_repos(data):
        page = REPOS_DIR / _repo_page_filename(item if category != "root" else {"key": "root"})
        page.write_text(render_repo_page(item, category), encoding="utf-8")
        generated.append(str(page))
    print("Generated:", *generated)


if __name__ == "__main__":
    main()
