# Architecture

Modules principaux:

- semantic-core — traitement sémantique
- execution-orchestrator — drivers (local/colab/cloud), `missions/`
- publication-engine — génération de publications
- datasets-ingestion — ingestion de données
- attribution-registry — attribution et traçabilité

Principe: séparation nette (contrats, tests), CI par module, documentation commune.
