# Copilotage (fusion fusionnée 2025-09-05)

Ce dossier unifie l'ancien `Copilotage/` (workflow, scripts, journaux, knowledge interne) et `copilotage/` (config + sous-module partagé).

## Arborescence normalisée
- `agents/` — Orchestrateurs et agents spécialisés (expérimental)
- `scripts/` — Outils d'automatisation (DevOps, collecte, analyse)
- `journal/` — Traçabilité des sessions (host + pid + date)
- `knowledge/` — Essences conceptuelles internes (non destinées à la doc publique directe)
- `shared/` — Sous-module partagé (ex-`copilotage/shared`)

## Principales sources migrées
- `README_COPILOTAGE_HISTORIQUE.md` (ex-`Copilotage/README.md`)
- `COPILOTAGE_WORKFLOW.md`
- Journaux 2025-08-30 → 2025-09-01
- Notes de vision & roadmaps internes
- Scripts DevOps et automation

## Règles post-fusion
1. Toute nouvelle ressource interne va ici (pas de recréation de `Copilotage/`).
2. Les liens historiques GitHub resteront valides via l'historique Git; pour les docs publiques, référencer désormais `governance/copilotage/...`.
3. Le sous-module `copilotage/shared` est monté sous `shared/`; maintenir .gitmodules synchronisé si déplacement futur.

## TODO de finalisation
- [ ] Mettre à jour les liens dans `docs/research/universaux-semantique.md` (pointent encore vers `Copilotage/journal/...`).
- [ ] Vérifier génération index modules après renommages (aucun impact attendu).
- [ ] Ajouter lint + validations provenance centralisées.

Révision: 2025-09-05.

## Portée et contrat de non‑dépendance

Ce dossier concentre le copilotage IA du projet.

Objectif:
- Consolider les informations IA relatives à la mission principale, aux missions en cours et aux préférences d’interactions IA‑humain.
- Héberger les outils produits par l’IA pour optimiser le travail lors de ces interactions (prompts, checklists, scripts d’assistance non bloquants).

Limite explicite:
- Rien ici ne doit être requis pour construire, tester, exécuter ou déployer le projet principal. Un humain doit pouvoir travailler sans consulter ni exécuter de scripts de `copilotage`.

Consignes:
- Autorisé: journaux, playbooks, prompts, guides, tableaux de bord, scripts utilitaires facultatifs.
- Interdit: logique métier, bibliothèques importées par la prod, secrets runtime, étapes CI/CD obligatoires.

Application:
- Toute arborescence « copilotage » dérivée/collaborante DOIT appliquer cette politique.
- Voir `POLICY.md` pour la version complète et `scripts/check_copilotage_independence.py` pour une vérification rapide.
