Titre: [hostname-pid-agent-model] [owner:human|agent] <type>: <résumé court> (Refs #<issue>)

Contexte
- Issue liée: #<num>
- Branche: <type>/issue-<num>-<slug>
- Agent/Session: préfixe obligatoire dans le titre: `[hostname-pid-agent-model]` et tag `[owner:human|agent]`
- Interdits: les tags de titre commençant par `journal:` (utiliser le préfixe ci‑dessus à la place)
- Modèle (optionnel): [model:<nom>] (ex: gpt-4o, claude-3.5)
- Propriétaire (optionnel): [owner:human] pour marquer une PR portée par un humain (sinon propriétaire inféré)

Changements
- [ ] …

Vérifications
- [ ] CI passe (CodeQL, CI minimal)
- [ ] Docs/dashboard impactés mis à jour si nécessaire
- [ ] Journal de session ajouté dans `Copilotage/journal/`
- [ ] Préfixe conforme dans le titre: `[hostname-pid-agent-model]` et `[owner:human|agent]`
- [ ] Merge par un agent différent (cross-check)

Clôture
- Closes #<num> (remplacer si pertinent)

Astuce: utilisez `Copilotage/scripts/devops/gh_pr_open.sh` pour générer le titre conforme (`--model`, `--owner`).
