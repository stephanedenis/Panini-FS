# Traçabilité & Attribution multi-agents

Objectif: attribuer clairement les contributions entre agents humains et automatisés.

## Identifiants
- PR: labels requis: `prov:host=...`, `prov:pid=...`, `agent:...`, `model:...`, `owner:...`.
	Note: la journalisation Copilotage (dossier `Copilotage/journal/`) est obligatoire et mise à jour dans chaque PR, mais n'est pas encodée dans les labels de PR.
- Commits: `Refs #<issue>` dans le message; optionnellement `Co-authored-by:` pour pairs.
- Journal: `Copilotage/journal/YYYY-MM-DD-<host>-pid<pid>-<slug>.md` par session.

## Cross-check
- Revue croisée: une PR ouverte par un agent doit être revue/mergée par un autre agent.
- Chercher `agent:<host>` ≠ reviewer/merger actuel.

## Déviations
- Utiliser le label `copilotage-exempt` pour documenter un bypass (raison courte dans la PR).

## Outils
- `gh_pr_open.sh` pour ouvrir la PR et ajouter automatiquement les labels de provenance courts.
- `label-agent.yml` et `validate-agent-provenance.yml` pour labels dérivés et garde-fou CI (validation sur labels courts).
