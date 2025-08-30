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
