---
title: OntoWave — Vision et rôle dans l’écosystème
---

# OntoWave — Vision et rôle dans l’écosystème

OntoWave est le navigateur sémantique et lecteur Markdown côté client de l’écosystème PaniniFS. Sa mission est de rendre la connaissance navigable, vivante et interopérable : un front-end ultra-léger qui relie des documents, des concepts et des graphes sémantiques en une expérience fluide.

## Pourquoi un projet séparé ?

- Couplage faible: OntoWave évolue à son propre rythme (web app) tandis que PaniniFS reste le socle documentaire et conceptuel (MkDocs + Pages).
- Portabilité: Une application statique Vite + TypeScript, déployable partout (Pages, S3, CDN, offline).
- Extensibilité: Cœur réutilisable pour des extensions (VS Code, navigateur, Azure DevOps) sans alourdir PaniniFS.

## Capabilités cœur (MVP actuel)

- Rendu Markdown rapide (markdown-it) avec ancrage, notes de bas de page, attributs de liens.
- Syntaxes riches: code (highlight.js), formules (KaTeX), diagrammes (Mermaid).
- Routage hash (/#/chemin) compatible hébergement statique.
- Configuration de sources de contenu via `public/config.json` et génération de `sitemap.json`.

## Vision moyen terme

- Navigation sémantique (ancrages conceptuels, back/forward links, cartes de concepts).
- Recherche et filtres contextuels (tags, entités, relations, temporalité).
- Mode offline/edge-first, index local et incrémental.
- Kits d’extension: 
  - Extension VS Code (éditeur sémantique, preview synchronisée),
  - Web extension (enrichissement de pages),
  - Intégration CI (lint sémantique, liens cassés, graph diff) et Azure DevOps.

## Rôle dans PaniniFS

- PaniniFS publie et structure le corpus (MkDocs strict, i18n, workflows, RSS recherche).
- OntoWave offre une lecture exploratoire et sémantique au-dessus de ce corpus et d’autres sources.
- Les deux restent découplés : PaniniFS référence OntoWave, mais ne le build pas dans le pipeline Pages.

## Intégrations prévues

- Liens croisés depuis les pages PaniniFS vers des vues OntoWave (par exemple des cartes de concepts).
- Exposition d’un `sitemap.json` et de métadonnées (frontmatter) que OntoWave pourra indexer.
- À terme, un connecteur « knowledge graph » pour rapprocher Dhātu, universaux sémantiques et facettes de navigation.

### Pattern recommandé dans les sous-modules

- Servir le SPA OntoWave comme `index.html` à la racine du dossier docs/ du module.
- La doc statique (Markdown) reste dans `docs/` pour agrégation MkDocs; le SPA offre une navigation dynamique sur le même corpus.
- Aucune dépendance build côté PaniniFS: les sous-modules restent autonomes pour leur SPA.

## Références

- Dépôt OntoWave : https://github.com/stephanedenis/OntoWave
- Licence et CI : lint, type-check, build, artefacts PR.

Statut : MVP autonome opérationnel (CI verte), feuille de route progressive. Toute contribution passe par le dépôt OntoWave.
