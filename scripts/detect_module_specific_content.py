#!/usr/bin/env python3
"""
Détecte les fichiers du dépôt principal qui semblent spécifiques à un sous-module
afin de préparer une externalisation propre (via issues ou PRs dans les submodules).

Heuristiques:
- Noms de fichiers et chemins contenant les clés de submodules (key)
- Contenu texte contenant des mentions fortes (key, name, url du repo)
- Exclusions: docs/ecosystem/**, mkdocs.yml, README/LICENCE racine, scripts de génération écosystème

Sortie: JSON imprimé sur stdout avec mapping { key: [paths...] }
"""
from __future__ import annotations
from pathlib import Path
import json
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ecosystem.yml"

EXCLUDE_DIRS = {
    ".git",
    "docs/ecosystem",
    "site",
    "issues_packs",
    "modules",  # déjà externalisé via submodules
}

EXCLUDE_FILES = {
    "mkdocs.yml",
    "README.md",
    "LICENSE",
}

TEXT_EXTS = {".md", ".txt", ".yml", ".yaml", ".json", ".py", ".sh"}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def iter_files(root: Path):
    for p in root.rglob("*"):
        if p.is_dir():
            rel = p.relative_to(root).as_posix()
            if any(rel == d or rel.startswith(d + "/") for d in EXCLUDE_DIRS):
                # skip entire directory trees
                continue
            continue
        rel = p.relative_to(root).as_posix()
        if rel in EXCLUDE_FILES:
            continue
        if any(rel == d or rel.startswith(d + "/") for d in EXCLUDE_DIRS):
            continue
        yield p


def main():
    data = load_yaml(DATA)
    keys = [m.get("key") for m in (data.get("submodules") or []) if m.get("key")]
    keys += [m.get("key") for m in (data.get("external") or []) if m.get("key")]
    keys = [k for k in keys if k]
    # Quick patterns map
    patterns = {k: re.compile(re.escape(k), re.IGNORECASE) for k in keys}
    mapping: dict[str, list[str]] = {k: [] for k in keys}
    for p in iter_files(ROOT):
        rel = p.relative_to(ROOT).as_posix()
        # Filename-based hint
        for k, rgx in patterns.items():
            if rgx.search(rel):
                mapping[k].append(rel)
                break
        else:
            # Content-based hint (text files only)
            if p.suffix.lower() in TEXT_EXTS:
                try:
                    txt = p.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue
                for k, rgx in patterns.items():
                    if rgx.search(txt):
                        mapping[k].append(rel)
                        break
    # Remove empties
    mapping = {k: sorted(set(v)) for k, v in mapping.items() if v}
    print(json.dumps(mapping, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
