# Vue d’ensemble des modules et projet parent Panini

Constat: PaniniFS = sous-projet filesystem. Un projet parent "Panini" devrait regrouper vision, recherche, outils et PaniniFS.

Parent Panini (proposé)
- Repos parent: Panini (vision, gouvernance globale, publications, roadmaps)
- Subprojects: PaniniFS (filesystem), SemanticCore, PublicationEngine, ExecutionOrchestrator, MonitoringWatchdog, etc.
- Docs: site unifié (mkdocs), pages par sous-projet.

Découpe cible (Option B)
- semantic-core — noyau sémantique (dhātu, fingerprints, hypergraphe/treillis)
- execution-orchestrator — orchestrateur d’exécutions (drivers local/colab/cloud)
	- missions/ — catalogue des missions autonomes (intégré)
- monitoring-watchdog — monitoring/doctor (ex-ultra-reactive)
- publication-engine — pipelines éditoriaux (Medium/Leanpub)
- attribution-registry — registre de provenance/licences (nouveau)
- datasets-ingestion — ingestion/normalisation corpus (nouveau)

À faire
- Voir `ARCHITECTURE/ADR-2025-08-30-modular-restructuring-option-b.md` et `ARCHITECTURE/module-contracts.md`.
- Créer le repo ExecutionOrchestrator et migrer cloud-orchestrator/colab-controller + autonomous-missions (missions/).
- Créer les repos attribution-registry et datasets-ingestion (MVP + contrats).
