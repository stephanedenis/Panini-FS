# Scripts Copilotage — points d’entrée

- headless_env_loader.py — chargeur d’env headless minimal
- github_workflow_monitor.py — monitor GitHub minimal (squelette)
- tests/ — tests basiques (imports, smoke)

Installation rapide:
- pip install -r Copilotage/scripts/requirements.txt

Exécution tests:
- pytest Copilotage/scripts/tests -q

Automatisation tâches/branches:
- devops/gh_task_init.sh — crée une issue et une branche associée

Journalisation:
- devops/journal_session.sh — génère un squelette de journal dans Copilotage/journal