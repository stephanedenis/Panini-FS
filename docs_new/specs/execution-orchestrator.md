# Spécifications — Execution Orchestrator

Contrat minimal:

- Entrée: `mission` (str), `backend` in {local, colab, cloud}
- Sortie: code de retour int (0 = succès)
- Drivers: exposent `run(mission: str) -> int`
- Missions: exposent `run() -> int` ou `main() -> int`

Erreurs:
- backend inconnu → code 2
- mission inconnue → déléguée au driver

Tests: smoke CLI, test mission `echo`.
