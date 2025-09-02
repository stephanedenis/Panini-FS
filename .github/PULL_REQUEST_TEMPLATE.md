<!-- PR Template unifié -->

Titre: <type>: <résumé court> (Refs #<issue>)

## Objet

Brève description du changement et impact.

## Journal

Lien vers l’entrée la plus récente sous `Copilotage/journal/` (obligatoire)

## Contexte

- Issue liée: #<num>
- Branche: <type>/issue-<num>-<slug>
- Métadonnées obligatoires (labels de provenance):
  - `prov:host=<host>`, `prov:pid=<pid>`
  - `agent:<nom>`, `model:<nom>`, `owner:<agent|human|pair|ops|infra>`
- Interdits: labels commençant par `journal:` et tags de titre `[journal:…]`

## Changements

- [ ] …

## Qualité (rapide)

- [ ] Build/Lint/Tests: PASS
- [ ] Docs/README mises à jour si nécessaire
- [ ] Journal ajouté dans `Copilotage/journal/`
- [ ] Labels `prov:host=*`, `prov:pid=*`, `agent:*`, `owner:*`, `model:*` présents

## Clôture

- Closes #<num>

Astuce: utilisez `Copilotage/scripts/devops/gh_pr_open.sh` pour ouvrir la PR et ajouter automatiquement des labels de provenance (`--model`, `--owner`).
