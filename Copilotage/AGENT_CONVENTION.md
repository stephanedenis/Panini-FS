# Convention d’identification des agents

Objectif: distinguer les PRs par agent pour permettre des validations croisées.

## Comment marquer une PR
- Ajoutez dans le titre: `[journal:HOST-pidPID]` (ex: `[journal:totoro-pid12345]`).
- À défaut, utilisez un nom de branche: `agents/HOST/ma-feature` (moins précis; ne remplace pas le PID).

## Automatisation
- Le workflow `.github/workflows/label-agent.yml` ajoute automatiquement des labels `agent:<host>` et `journal:<host>-pid<pid>`.
- Le workflow `.github/workflows/validate-agent-session.yml` échoue si le titre ne contient pas `[journal:HOST-pidPID]`.
- Exception: ajoutez le label `copilotage-exempt` pour bypass (cas rares).

## Bonnes pratiques
- HOST = hostname court (ex: `totoro`). PID = PID du process VS Code (ex: `17771`).
- Garder le même ID sur toute la durée d’une session.
