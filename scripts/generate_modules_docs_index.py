#!/usr/bin/env python3
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_MODULES = ROOT / 'docs_new' / 'modules' / 'index.md'

def discover():
    modules = []
    for p in sorted((ROOT / 'modules').iterdir()):
        if not p.is_dir():
            continue
        if not (p / '.git').exists():
            continue
        entry = {
            'name': p.name,
            'has_docs': (p / 'docs').exists(),
            'docs_index': (p / 'docs' / 'index.md').exists(),
        }
        modules.append(entry)
    return modules

def render(mods):
    lines = [
        '# Documentation des modules',
        '',
        'Cette page est générée automatiquement. Ne pas éditer manuellement.',
        '',
        '## Modules détectés',
        ''
    ]
    for m in mods:
        if m['has_docs']:
            if m['docs_index']:
                lines.append(f"- {m['name']}: modules/{m['name']}/docs/index.md")
            else:
                lines.append(f"- {m['name']}: modules/{m['name']}/docs/ (pas d'index.md)")
        else:
            lines.append(f"- {m['name']}: (pas de dossier docs/)")
    lines.append('')
    return '\n'.join(lines)

def main():
    mods = discover()
    DOCS_MODULES.parent.mkdir(parents=True, exist_ok=True)
    DOCS_MODULES.write_text(render(mods), encoding='utf-8')

if __name__ == '__main__':
    main()
