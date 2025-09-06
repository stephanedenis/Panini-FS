Titre: <type>: <résumé court> (Refs #<issue>)

Contexte
- Issue liée: #<num>
- Branche: <type>/issue-<num>-<slug>
- Métadonnées PR (obligatoire): labels courts `prov:host=<host>`, `prov:pid=<pid>`, `agent:<agent>`, `model:<modele>`, `owner:<human|agent>`
- Interdits: tout label commençant par `journal:` et les tags de titre `[journal:…]`
- Modèle (optionnel): [model:<nom>] (ex: gpt-4o, claude-3.5)
- Propriétaire (optionnel): [owner:human] pour marquer une PR portée par un humain (sinon propriétaire inféré)

Changements
- [ ] …

Vérifications
- [ ] CI passe (CodeQL, CI minimal)
- [ ] Docs/dashboard impactés mis à jour si nécessaire
- [ ] Journal de session ajouté dans `Copilotage/journal/`
- [ ] Labels `prov:host=*`, `prov:pid=*`, `agent:*`, `owner:*` et `model:*` présents
- [ ] Merge par un agent différent (cross-check)
- [ ] Si des submodules sont concernés, lier la/les PR(s) du submodule et confirmer la mise à jour du pointeur (commit submodule)

Clôture
- Closes #<num> (remplacer si pertinent)

Astuce: utilisez `Copilotage/scripts/devops/gh_pr_open.sh` pour ouvrir la PR et ajouter automatiquement le label `provenance:` (`--model`, `--owner`).
Astuce 2: `gh_pr_open.sh` peut aussi ajouter `autofill-provenance` et `automerge-provenance` (opt-in) pour l’auto-complétion et l’auto-merge quand la provenance est complète.
