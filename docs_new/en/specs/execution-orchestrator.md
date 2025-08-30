# Specifications — Execution Orchestrator

Minimal contract:

- Input: `mission` (str), `backend` in {local, colab, cloud}
- Output: exit code int (0 = success)
- Drivers: expose `run(mission: str) -> int`
- Missions: expose `run() -> int` or `main() -> int`

Errors:
- unknown backend → exit code 2
- unknown mission → delegated to driver

Tests: CLI smoke, `echo` mission test.
