# Contrats d’interface par module (MVP)

## semantic-core
- Entrées: texte/code/blob
- Sorties: dhātu[], fingerprints, hypergraph/treillis
- API (pseudo):
  - extract_dhatu(input) -> [Dhatu]
  - semantic_hash(input) -> str
  - graph.query(q) -> ResultSet

## execution-orchestrator (nouveau)
- Entrées: mission spec + backend (local|colab|cloud)
- Sorties: run_id, logs, artefacts
- API:
  - run(mission, backend, params) -> run_id
  - status(run_id) -> {state, progress}
  - cancel(run_id) -> bool
  - drivers: register(name, adapter)

## missions (déplacé dans execution-orchestrator)
- Entrées: paramètres; Sorties: plan et steps
- API:
  - list_missions() -> [name]
  - render_plan(name, params) -> [Step]

## monitoring-watchdog (ex-ultra-reactive)
- Entrées: cibles à monitorer; Sorties: events/alertes
- API:
  - subscribe(target, probe) -> sub_id
  - on_event(handler)

## publication-engine
- Entrées: sources RESEARCH; Sorties: miroirs, exports Medium/Leanpub
- API/CLI:
  - sync()
  - export_medium()
  - export_leanpub()

## attribution-registry (à créer)
- Entrées: artefacts + métadonnées; Sorties: enregistrements/citations/signatures
- API:
  - register(artifact, meta) -> id
  - resolve(id) -> record
  - verify(signature) -> bool

## datasets-ingestion (à créer)
- Entrées: sources externes; Sorties: datasets normalisés + manifests
- API/CLI:
  - fetch(source)
  - normalize(dataset)
  - publish(manifest)
