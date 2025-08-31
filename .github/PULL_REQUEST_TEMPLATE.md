Titre: <type>: <résumé court> (Refs #<issue>)

Contexte
- Issue liée: #<num>
- Branche: <type>/issue-<num>-<slug>
- Métadonnées PR (obligatoire): ajoutez le label `provenance:host=<host>,pid=<pid>,agent=GitHubCopilot,model=<modele>,owner=<human|agent>`
- Modèle (optionnel): [model:<nom>] (ex: gpt-4o, claude-3.5)
- Propriétaire (optionnel): [owner:human] pour marquer une PR portée par un humain (sinon propriétaire inféré)

Changements
- [ ] …

Vérifications
- [ ] CI passe (CodeQL, CI minimal)
- [ ] Docs/dashboard impactés mis à jour si nécessaire
- [ ] Journal de session ajouté dans `Copilotage/journal/`
- [ ] Label `provenance:...` présent et labels dérivés: `agent:<id>`, `owner:human|agent` et si applicable `model:<nom>`
- [ ] Merge par un agent différent (cross-check)

Clôture
- Closes #<num> (remplacer si pertinent)

Astuce: utilisez `Copilotage/scripts/devops/gh_pr_open.sh` pour ouvrir la PR et ajouter automatiquement le label `provenance:` (`--model`, `--owner`).
