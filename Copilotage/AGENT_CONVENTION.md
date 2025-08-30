# Convention d’identification des agents

Objectif: distinguer les PRs par agent pour permettre des validations croisées.

## Comment marquer une PR
- Ajoutez dans le titre: `[agent:ID]` (ex: `[agent:steph-laptop]`).
- À défaut, utilisez un nom de branche: `agents/ID/ma-feature`.

## Automatisation
- Le workflow `.github/workflows/label-agent.yml` ajoute automatiquement un label `agent:<id>` aux PRs.
- Si aucun ID n’est détecté, aucune action; pensez à éditer le titre de la PR.

## Bonnes pratiques
- ID court et stable par machine/process (ex: `steph-laptop`, `workstation-1`).
- Garder le même ID sur toute la durée d’une session.
