# Contributing — Copilotage

Ce projet applique le workflow Copilotage (issue → branche → PR → journal).

Lisez d’abord:
- Copilotage/COPILOTAGE_WORKFLOW.md
- Copilotage/README.md

Démarrage rapide
- Ouvrir une issue (templates fournis)
- Créer la branche avec: `Copilotage/scripts/devops/gh_task_init.sh "[type] titre" type slug`
- Commits courts avec références: `Refs #<num>`
- Ouvrir une PR (template fourni) et ajouter le journal de session dans `Copilotage/journal/`

CI
- Workflows légers (CodeQL + CI minimal). Visez des PRs petites et fréquentes.

Merci de respecter l’esprit “Camping”: simplicité, couplage faible, docs claires.
