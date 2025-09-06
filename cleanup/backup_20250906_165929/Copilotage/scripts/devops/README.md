# DevOps utilitaires (Copilotage)

- devops/gh_task_init.sh — ouvre (ou réutilise) une issue et crée la branche `<type>/issue-<num>-<slug>`
- devops/gh_pr_open.sh — ouvre une PR et ajoute les labels `prov:host=…`, `prov:pid=…`, `agent:GitHubCopilot`, `model=…`, `owner=…`
- devops/journal_session.sh — génère un squelette de journal dans Copilotage/journal
- fix_remotes.sh: bascule/normalise l'URL du remote (HTTPS <-> SSH)
- git_audit.sh: audit rapide (remotes, status, fetch, submodules, dernier commit)
- bootstrap_submodules.sh: ajoute/initialise les submodules de l'écosystème (modules/*)
- setup_dev_environment.sh: setup rapide de l'environnement local (requirements, audit, remotes)

Racine propre: aucun utilitaire ne doit rester à la racine. Placez tout ici.

## Usage rapide

```
# Créer l’issue + branche
Copilotage/scripts/devops/gh_task_init.sh "[docs] Consolidation Copilotage" docs copilotage-docs

# Travailler… puis ouvrir la PR
Copilotage/scripts/devops/gh_pr_open.sh "Consolidation Copilotage"
```

Règle CI: métadonnées `provenance` requises via labels courts (`prov:host`, `prov:pid`, `agent:*`, `model:*`, `owner:*`).