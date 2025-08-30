Titre: [journal:<host>-pid<pid>] [model:<nom>] <type>: <résumé court> (Refs #<issue>)

Contexte
- Issue liée: #<num>
- Branche: <type>/issue-<num>-<slug>
- Agent/Session: [journal:<host>-pid<pid>] (ou [agent:<id>] si PID indisponible)
- Modèle (optionnel): [model:<nom>] (ex: gpt-4o, claude-3.5)

Changements
- [ ] …

Vérifications
- [ ] CI passe (CodeQL, CI minimal)
- [ ] Docs/dashboard impactés mis à jour si nécessaire
- [ ] Journal de session ajouté dans `Copilotage/journal/`
- [ ] Labels auto présents: `agent:<id>`, `journal:<host>-pid<pid>` et si applicable `model:<nom>`
- [ ] Merge par un agent différent (cross-check)

Clôture
- Closes #<num> (remplacer si pertinent)

Astuce: utilisez `Copilotage/scripts/devops/gh_pr_open.sh` pour générer le titre conforme.
