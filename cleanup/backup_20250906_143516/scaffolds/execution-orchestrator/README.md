# ExecutionOrchestrator

Orchestre des exécutions (drivers: local, colab, cloud) et intègre `missions/` (ex-autonomous-missions).

- CLI: `exec-orch`
- API: run(mission, backend, params) -> run_id; status(run_id); cancel(run_id)

Roadmap
- drivers/local, drivers/colab, drivers/cloud
- dossier `missions/` avec catalogue
- smoke tests (CI)
