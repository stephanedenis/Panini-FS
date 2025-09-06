# Migration Checklist — Option B

Cette checklist décrit des étapes sans effet destructif par défaut.

## Préparation
- [ ] Ouvrir une issue "Restructure modules (Option B)" et lier ADR.
- [x] Créer le repo `PaniniFS-ExecutionOrchestrator` (vide, README, MIT, CI minimal).
- [ ] Désactiver les protections temporaires si nécessaire (push branches).
 - [x] Mettre en place la gouvernance PR par labels de provenance (prov:host, prov:pid, agent, model, owner) + validation CI.
 - [x] Activer les workflows d'autonomie (guardian, auto-merge opt-in) pour faciliter les PR prérequis (PR #37).

## Migration code (locale)
- [ ] Cloner les repos: CloudOrchestrator, CoLabController, AutonomousMissions.
- [ ] Regrouper historiques:
  - [x] Importer `cloud-orchestrator` → branche `import/cloud` dans ExecutionOrchestrator (PR ouverte).
  - [x] Importer `colab-controller` → branche `import/colab` (PR ouverte).
  - [ ] Fusionner en `main` avec dossier `drivers/colab`, `drivers/cloud`.
  - [x] Importer `autonomous-missions` → `missions/` (PR ouverte, historique préservé si possible).
- [ ] Rendre les chemins et imports relatifs compatibles.

## Mise à jour parent (PaniniFS)
- [x] Mettre à jour `.gitmodules` (supprimer 2 anciens, ajouter `modules/execution-orchestrator`).
- [x] Synchroniser submodules (`git submodule sync && git submodule update --init --recursive`).
- [x] Mettre à jour READMEs racine et modules.

## CI/Qualité
- [x] Ajouter smoke tests pour orchestrateur et missions (pytest + GH Actions).
- [ ] Lint/format minimal (ruff/black) ou équivalent.
- [ ] Badges CI à jour.
 - [x] Ajout build docs strict (MkDocs Material + i18n + Kroki SVG liens) sur push/PR.
 - [x] Générateur d'index des modules et workflow d'auto-maj.

## Déploiement
- [ ] Tag v0.1 sur ExecutionOrchestrator.
- [ ] Archiver (ou déprécier) les anciens repos avec README de redirection.
 - [ ] Publier la doc mise à jour (GitHub Pages) après merge PR #37.

## Post-migration
- [ ] Créer issues pour `attribution-registry` et `datasets-ingestion` (scopes, contrats, MVP).
- [ ] Mettre à jour `Copilotage/knowledge/MODULES_OVERVIEW_AND_PARENT_PROJECT.md`.
 - [ ] Ajouter squelettes de docs par module dans leurs repos respectifs (ou agrégation dans `docs/modules/_ext`).
 - [ ] Activer les checks de style (ruff/black) et type (mypy) sur orchestrateur.
