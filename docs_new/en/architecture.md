# Architecture

Key modules:

- semantic-core — semantic processing
- execution-orchestrator — drivers (local/colab/cloud), `missions/`
- publication-engine — publications
- datasets-ingestion — data ingestion
- attribution-registry — attribution/traceability

Principle: clear separation (contracts, tests), per-module CI, shared documentation.
