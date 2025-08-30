# Traçabilité & Attribution multi-agents

Objectif: attribuer clairement les contributions entre agents humains et automatisés.

## Identifiants
- PR: `[journal:HOST-pidPID]` requis (labels auto `agent:HOST`, `journal:HOST-pidPID`).
- Commits: `Refs #<issue>` dans le message; optionnellement `Co-authored-by:` pour pairs.
- Journal: `Copilotage/journal/YYYY-MM-DD-<host>-pid<pid>-<slug>.md` par session.

## Cross-check
- Revue croisée: une PR ouverte par un agent doit être revue/mergée par un autre agent.
- Chercher `agent:<host>` ≠ reviewer/merger actuel.

## Déviations
- Utiliser le label `copilotage-exempt` pour documenter un bypass (raison courte dans la PR).

## Outils
- `gh_pr_open.sh` pour titres PR conformes.
- `label-agent.yml` et `validate-agent-session.yml` pour labels et garde-fou CI.
