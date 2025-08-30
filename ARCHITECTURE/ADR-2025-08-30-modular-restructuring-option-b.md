# ADR 2025-08-30 — Restructuration modulaire (Option B)

Statut: Acceptée  
Contexte: docs/issue-20-assimilation-archives  
Motivation: simplifier la découpe, réduire la fragmentation et clarifier les contrats.

## Décision
- Fusionner `modules/cloud-orchestrator` et `modules/colab-controller` en un unique module: `execution-orchestrator` (drivers: local, colab, cloud).
- Intégrer `modules/autonomous-missions` comme répertoire `missions/` à l’intérieur d’`execution-orchestrator` (et non plus comme submodule séparé).
- Renommer fonctionnellement `modules/ultra-reactive` en rôle “monitoring-watchdog” (le nom du repo peut rester pour l’instant; on aligne d’abord le contrat et le README).
- Préparer 2 modules à créer: `attribution-registry` et `datasets-ingestion`.

## Alternatives envisagées
- Option A: conserver `autonomous-missions` séparé — rejeté (trop de fragmentation, faible besoin de versionnage indépendant à ce stade).
- Option C: éclater `semantic-core` en 2 submodules (fingerprints vs hypergraph) — remis à plus tard; d’abord clarifier les packages internes.

## Impact attendu
- Contrats plus nets: run orchestration, missions, monitoring, core sémantique et publication.
- Moins d’overhead Git et moins de coordination inter-repos.

## Plan de migration (résumé)
1) Créer repo `PaniniFS-ExecutionOrchestrator` (privé → public plus tard).  
2) Migrer l’historique de `cloud-orchestrator` et `colab-controller` en branches (subtree/filter-repo), puis fusionner.  
3) Importer le contenu d’`autonomous-missions` sous `missions/` (préserver l’historique si possible).  
4) Mettre à jour `.gitmodules` et CI.  
5) Aligner READMEs et contrats; publier un tag v0.1.

Voir `ARCHITECTURE/migration-checklist-option-b.md` pour les étapes détaillées.
