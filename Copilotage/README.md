# Copilotage — Guide de contribution et d’orchestration

Ce dossier regroupe les normes, scripts et artefacts pour structurer le travail assisté par agents IA.

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
4) Ouvrez une PR vers master avec checklists et journal associé.

## Outils DevOps
- scripts/devops/gh_task_init.sh — crée/retrouve l’issue et la branche
- scripts/devops/gh_pr_open.sh — ouvre une PR avec titre auto-préfixé `[journal:HOST-pidPID]`

### Exemple
```bash
Copilotage/scripts/devops/gh_task_init.sh "[docs] Consolidation Copilotage" docs copilotage-docs
# travail...
Copilotage/scripts/devops/gh_pr_open.sh "Consolidation Copilotage"
```

Journalisation
- Script: Copilotage/scripts/devops/journal_session.sh session
- Ajoutez Contexte, Actions, Liens, Tests, Next.

Bonnes pratiques
- Petites PRs, descriptions concrètes.
- CI légère, docs systématiques si public.
- Respect du mode “Camping” (simplicité, faible couplage).

---
Mainteneur: tenez ce README synchronisé avec l’évolution des scripts et du workflow.