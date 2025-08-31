Titre: <type>: <résumé court> (Refs #<issue>)

Contexte
- Issue liée: #<num>
- Branche: <type>/issue-<num>-<slug>
- Métadonnées PR (obligatoire): ajoutez ces labels courts: `prov:host=<host>`, `prov:pid=<pid>`, `agent:GitHubCopilot`, `model=<modele>`, `owner=<human|agent>`
- Modèle (optionnel): [model:<nom>] (ex: gpt-4o, claude-3.5)
- Propriétaire (optionnel): [owner:human] pour marquer une PR portée par un humain (sinon propriétaire inféré)

Changements
- [ ] …

Vérifications
- [ ] CI passe (CodeQL, CI minimal)
- [ ] Docs/dashboard impactés mis à jour si nécessaire
- [ ] Journal de session ajouté dans `Copilotage/journal/`
- [ ] Labels `prov:host`, `prov:pid`, `agent:*`, `owner:*` et `model:*` présents
- [ ] Merge par un agent différent (cross-check)

Clôture
- Closes #<num> (remplacer si pertinent)

Astuce: utilisez `Copilotage/scripts/devops/gh_pr_open.sh` pour ouvrir la PR et ajouter automatiquement le label `provenance:` (`--model`, `--owner`).
