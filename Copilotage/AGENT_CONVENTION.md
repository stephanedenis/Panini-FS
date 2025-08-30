# Convention d’identification des agents

Objectif: distinguer les PRs par agent pour permettre des validations croisées.

## Comment marquer une PR
- Ajoutez dans le titre: `[journal:HOST-pidPID]` (ex: `[journal:totoro-pid12345]`).
- Optionnel: ajoutez `[model:NOM]` (ex: `[model:gpt-4o]`, `[model:claude-3.5]`).
- Optionnel: pour lever toute ambiguïté d’attribution, ajoutez `[owner:human]` si la PR est portée par un humain (sinon propriétaire inféré côté automatisation quand `journal`/`model` présents).
- À défaut, utilisez un nom de branche: `agents/HOST/ma-feature` (moins précis; ne remplace pas le PID).

## Automatisation
- Le workflow `.github/workflows/label-agent.yml` ajoute automatiquement des labels `agent:<host>`, `journal:<host>-pid<pid>` et `model:<nom>` si présent.
- Le workflow `.github/workflows/validate-agent-session.yml` échoue si le titre ne contient pas `[journal:HOST-pidPID]`.
- Exception: ajoutez le label `copilotage-exempt` pour bypass (cas rares).

## Bonnes pratiques
- HOST = hostname court (ex: `totoro`). PID = PID du process VS Code (ex: `17771`).
- `model` = type d’agent IA utilisé (ex: `gpt-4o`, `claude-3.5`, `mistral-large`).
- Garder le même ID sur toute la durée d’une session.
