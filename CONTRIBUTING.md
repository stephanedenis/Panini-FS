# Contributing — Copilotage

Ce projet applique le workflow Copilotage (issue → branche → PR → journal).

Lisez d’abord:
- Copilotage/COPILOTAGE_WORKFLOW.md
- Copilotage/README.md
- Copilotage/AGENT_CONVENTION.md

Démarrage rapide
- Ouvrir une issue (templates fournis)
- Créer la branche avec: `Copilotage/scripts/devops/gh_task_init.sh "[type] titre" type slug`
- Commits courts avec références: `Refs #<num>`
- Ouvrir une PR (template fourni) et ajouter le journal de session dans `Copilotage/journal/`

Agent ID et cross-check
- Chaque agent DOIT inclure un identifiant dans le titre de PR: `[agent:ID]` (ex: `[agent:steph-laptop]`) ou nom de branche `agents/ID/...`.
- Un workflow auto-applique un label `agent:<id>` pour faciliter les validations croisées.

CI
- Workflows légers (CodeQL + CI minimal). Visez des PRs petites et fréquentes.

Merci de respecter l’esprit “Camping”: simplicité, couplage faible, docs claires.


## Submodules — principe d’édition indépendante

Important: les submodules sont des dépôts Git séparés, édités et versionnés indépendamment.

- Ne pas modifier directement des fichiers à l’intérieur des répertoires déclarés dans `.gitmodules` (ex: `modules/*`, `copilotage/shared`, `RESEARCH`). Toute modification de contenu doit être faite via une PR dans le dépôt du submodule.
- Pour proposer un changement de submodule, ouvrez une issue ici avec le template « Submodule change request », puis ouvrez l’issue miroir dans le dépôt du submodule. Cette issue sert au suivi transversal (planification/alignement) côté monorepo.
- Une fois la PR fusionnée dans le submodule, mettez à jour le pointeur dans ce repo (commit de mise à jour du submodule), puis ouvrez la PR d’agrégation ici.
- Étiquetage recommandé: `target:submodule` + `submodule:<nom>` et `type:submodule-change`.
- VS Code: travaillez dans le workspace du submodule (chaque submodule est un projet/workspace VS Code indépendant). Voir `SUBMODULES_TEMPLATE/README.md` pour les bonnes pratiques (workspaces dédiés, couleur Peacock, docs locales, CI minimal).

Conseils pour agents IA Copilot:
- Décrire explicitement la cible du changement (monorepo vs sous-module) dans le titre/description des issues/PRs.
- Si une édition de submodule est nécessaire, créer la tâche dans le dépôt cible avant toute tentative d’édition depuis ce repo. Ici, ne commitez que la mise à jour du pointeur du submodule.
- Prévoir un court « plan de propagation »: PR du submodule → mise à jour du pointeur → validations CI/docs.

Liste indicative des submodules (voir `.gitmodules` pour référence à jour):
- modules/autonomous-missions
- modules/semantic-core
- modules/publication-engine
- modules/ultra-reactive
- modules/execution-orchestrator
- modules/datasets-ingestion
- modules/attribution-registry
- modules/ontowave-app
- copilotage/shared
- RESEARCH
