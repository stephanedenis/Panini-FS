#!/usr/bin/env python3
"""
Prépare des "packs d'issue" par sous-module pour décentraliser la doc/détails.

Pour chaque submodule/external de data/ecosystem.yml, crée:
- issues_packs/<key>/ISSUE_BODY.md : squelette d'issue avec contexte, liens, TODO.
- issues_packs/<key>/files.txt : liste de fichiers candidats à externaliser (heuristique simple).

Ces artefacts sont destinés à être copiés/collés dans des issues des sous-modules.
"""
from pathlib import Path
import json
import shutil
import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ecosystem.yml"
OUT = ROOT / "issues_packs"
DETECT_JSON = Path("/tmp/module_moves.json")


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def repo_items(data: dict):
    for cat in ("submodules", "external"):
        for item in data.get(cat) or []:
            yield cat, item


def guess_files_to_externalize(key: str, detected: dict[str, list[str]] | None = None) -> list[str]:
    # Heuristique: pointer vers docs/ et modules/<key>/README.md s'ils existent
    if detected and key in detected:
        return list(detected.get(key) or [])
    candidates: list[str] = []
    # mapping simple de key -> chemin module
    module_dir = ROOT / "modules" / key
    if module_dir.exists():
        readme = module_dir / "README.md"
        if readme.exists():
            candidates.append(str(readme.relative_to(ROOT)))
        docs_dir = module_dir / "docs"
        if docs_dir.exists():
            candidates.append(str(docs_dir.relative_to(ROOT)))
    return candidates


def main():
    data = load_yaml(DATA)
    OUT.mkdir(parents=True, exist_ok=True)
    detected = None
    if DETECT_JSON.exists():
        try:
            detected = json.loads(DETECT_JSON.read_text(encoding="utf-8"))
        except Exception:
            detected = None
    for cat, item in repo_items(data):
        key = item.get("key")
        if not key:
            continue
        d = OUT / key
        d.mkdir(parents=True, exist_ok=True)
        name = item.get("name", key)
        url = item.get("url", "")
        docs = item.get("docs_url") or ""
        role = item.get("role", "-")
        desc = item.get("description", "")
        files = guess_files_to_externalize(key, detected)
        # Copier les fichiers dans payload/ pour faciliter l'upload manuel dans l'issue submodule
        copied = []
        payload_dir = d / "payload"
        for rel in files:
            src = ROOT / rel
            if not src.exists() or src.is_dir():
                continue
            try:
                payload_path = payload_dir / rel
                payload_path.parent.mkdir(parents=True, exist_ok=True)
                # éviter les gros fichiers (>1 Mo)
                if src.stat().st_size > 1_000_000:
                    continue
                shutil.copy2(src, payload_path)
                copied.append(rel)
            except Exception:
                continue
        # ISSUE BODY
        body = []
        body.append(f"# {name} — alignement documentaire")
        body.append("")
        body.append(desc)
        body.append("")
        body.append(f"- Dépôt: {url}")
        if docs:
            body.append(f"- Documentation: {docs}")
        body.append(f"- Rôle: {role}")
        body.append("")
        body.append("## Tâches proposées")
        body.append("- [ ] Vérifier/compléter la documentation interne (README, docs/)")
        body.append("- [ ] Centraliser les détails locaux et lier depuis PaniniFS plutôt que dupliquer")
        body.append("- [ ] Mettre à jour data/ecosystem.yml (status, tags, contacts, docs_url si besoin)")
        body.append("")
        if files:
            body.append("## Fichiers candidats à externaliser")
            for f in files:
                body.append(f"- {f}")
            body.append("")
        if copied:
            body.append("Les contenus correspondants (<=1 Mo) sont fournis dans `payload/` pour upload.")
            body.append("")
        body.append(
            "> Note: cette issue est générée depuis PaniniFS pour décentraliser le travail vers le sous-module."
        )
        (d / "ISSUE_BODY.md").write_text("\n".join(body) + "\n", encoding="utf-8")
        # files list
        (d / "files.txt").write_text("\n".join(files) + "\n", encoding="utf-8")
    print("Issue packs ready:", str(OUT))


if __name__ == "__main__":
    main()
