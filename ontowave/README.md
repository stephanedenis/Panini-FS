# OntoWave (MVP)

Un mini site statique type « mdwiki » moderne, sans build documentaire, qui rend des fichiers Markdown côté client.

Principes:
- Aucune compilation de contenu: les `.md` sont chargés via `fetch` et rendus côté navigateur.
- Router hash (`#/chemin`) pour l’hébergement statique (GitHub Pages, S3, Nginx…).
- Racines de contenu configurables (permet de mapper des sous-arborescences ou des submodules).
- Rendu Markdown avec markdown-it, titres ancrés, code surligné, Mermaid et KaTeX.
- Optionnel: génération d’un `sitemap.json` (outil Node) pour la recherche ou la navigation.

## Démarrage

```bash
cd ontowave
npm install
npm run dev
```

Déploiement:
```bash
npm run build
npm run preview # ou servez le dossier dist/ sur Pages
```

## Structure
- `public/config.json`: configuration des racines de contenu (par défaut `content/`).
- `content/`: vos fichiers Markdown (exemples fournis).
- `src/`: app Vite (TypeScript), router et rendu Markdown.
- `tools/build-sitemap.mjs`: génère `public/sitemap.json` en scannant les racines.

## Intégration submodules
Publiez/recopiez vos sous-modules vers des répertoires montés comme racines de `config.json` (ex: `RESEARCH/`). L’app les servira tels quels et gérera les liens `.md` → routes `#/…`.

***

Limitations MVP:
- Pas d’indexation de recherche (prévue via `sitemap.json` + Web Worker elasticlunr).
- Sécurité XSS: le contenu est supposé de confiance. Ajoutez DOMPurify si nécessaire.
