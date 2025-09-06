# Relais — 2025-09-02

Contexte: consolidation des règles Copilotage (owner, journal, templates, CI). Branch: `ci/owner-labeler-and-templates` (PR #53).

À faire (prochain agent):
- [ ] Vérifier que le label `owner:*` est appliqué automatiquement sur la PR #53 après passage du workflow.
- [ ] Vérifier que la CI `copilotage-journal-check.yml` est verte (PR #53 contient bien un lien `Copilotage/journal/`).
- [ ] Si besoin, compléter `Copilotage/scripts/devops/gh_pr_open.sh` pour forcer l’inclusion de `[owner:...]` dans le titre généré.
- [ ] Fusionner #53 une fois CI verte, puis supprimer la branche.

Optionnel:
- [ ] Ajouter une courte note dans `GOVERNANCE/Copilotage/CHECKLIST_PR.md` pour l’éventail complet des owners.
