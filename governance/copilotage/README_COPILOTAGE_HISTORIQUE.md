# README Copilotage (historique migré)

Ce fichier est une copie préservée de l'ancien `Copilotage/README.md` avant fusion.

---

# Copilotage — Guide de contribution et d’orchestration

[![CI Minimal](https://github.com/stephanedenis/PaniniFS/actions/workflows/paniniFS-ci.yml/badge.svg)](https://github.com/stephanedenis/PaniniFS/actions/workflows/paniniFS-ci.yml)
[![CodeQL](https://github.com/stephanedenis/PaniniFS/actions/workflows/codeql.yml/badge.svg)](https://github.com/stephanedenis/PaniniFS/actions/workflows/codeql.yml)
[![Label PRs by Agent](https://github.com/stephanedenis/PaniniFS/actions/workflows/label-agent.yml/badge.svg)](https://github.com/stephanedenis/PaniniFS/actions/workflows/label-agent.yml)
[![Validate Agent Provenance](https://github.com/stephanedenis/PaniniFS/actions/workflows/validate-agent-provenance.yml/badge.svg)](https://github.com/stephanedenis/PaniniFS/actions/workflows/validate-agent-provenance.yml)
[![Cross-check visibility](https://github.com/stephanedenis/PaniniFS/actions/workflows/cross-check-visibility.yml/badge.svg)](https://github.com/stephanedenis/PaniniFS/actions/workflows/cross-check-visibility.yml)

Ce dossier regroupait les normes, scripts et artefacts pour structurer le travail assisté par agents IA.

Contenu clé
- COPILOTAGE_WORKFLOW.md — Règles et processus (issue→branche→PR, journal, quality gates)
- scripts/ — Outils d’automatisation (création d’issue/branche, journal, moniteurs)
- journal/ — Traçabilité des sessions (un fichier par session)
- knowledge/ — Essences et principes
- agents/ — Orchestrateurs/agents spécialisés (expérimental)

Quickstart
1) Créez une issue: décrire l’objectif, livrables, critères d’acceptation.
2) Créez la branche liée:
   - Script: Copilotage/scripts/devops/gh_task_init.sh "[type] Titre" type slug
3) Travaillez en petits commits référencés: "… (Refs #<num>)".
4) Ouvrez une PR vers master avec checklists, journal associé et labels `prov:host`, `prov:pid`, `agent:*`, `model:*`, `owner:*`.

Outils DevOps
- scripts/devops/gh_task_init.sh — crée/retrouve l’issue et la branche
- scripts/devops/gh_pr_open.sh — ouvre une PR et ajoute les labels provenance

Journalisation
- Script: Copilotage/scripts/devops/journal_session.sh session
- Ajoutez Contexte, Actions, Liens, Tests, Next.

Bonnes pratiques
- Petites PRs, descriptions concrètes.
- CI légère, docs systématiques si public.
- Respect du mode “Camping” (simplicité, faible couplage).

---
Mainteneur: ce contenu est désormais maintenu dans `governance/copilotage/`.
