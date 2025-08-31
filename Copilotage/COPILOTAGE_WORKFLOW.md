# Flux de travail standard pour agents IA

Objectif: garantir que chaque travail suit une discipline traçable via GitHub.

Règles obligatoires:
- Chaque travail démarre par une tâche (issue) GitHub.
- Une branche dédiée est créée: `<type>/issue-<num>-<slug>` (ex: `feat/issue-42-vision-agent`).
- Tous les commits référencent l’issue: `... (#<num>)` ou `Refs #<num>`.
- Une Pull Request relie la branche à `master/main` et ferme l’issue (`Closes #<num>`).
- Titre de PR: inclure `[journal:HOST-pidPID]` (ex: `[journal:totoro-pid17771]`). Optionnels: `[model:NOM]`, `[owner:human|agent]`.
- Quality gates dans la PR: build/lint/tests, checklist "Done".

Pratiques recommandées:
- Petites PRs, descriptions concises, changelog clair.
- CI minimale dans sous-modules; lint (ruff/black) à venir.

Automatisation:
- Utiliser `Copilotage/scripts/devops/gh_task_init.sh` pour ouvrir une issue et créer la branche.
- Utiliser `Copilotage/scripts/devops/gh_pr_open.sh` pour ouvrir une PR avec préfixe automatique `[journal:HOST-pidPID]` (options `--model`, `--owner`).

Journalisation Copilotage (obligatoire):
- À chaque session, ajouter un fichier `Copilotage/journal/<date>-<host>-pid<pid>-<session>.md`.
- Contenu minimal: Contexte, Décisions & actions clés, Liens (issues/PR), Tests/quality gates, Prochaines étapes.
- Nommage: `YYYY-MM-DD-<host>-pid<pid>-<slug>.md` (host: ex. Hauru; pid: pid VSCode si dispo, sinon shell).
- Voir `Copilotage/AGENT_CONVENTION.md` pour la règle d’identification agent/session.

Cheatsheet:
- Issue types: feat | fix | docs | chore | refactor | perf | test | ci
- Slug court, kebab-case.

---

Mainteneur: consigner tout écart dans l’issue.

## Directives d’autonomie de l’agent

- Travailler par blocs de 5–10 minutes sans demander de confirmation, tant que les règles sont respectées.
- Préférer des lots d’actions cohérents (lecture→édition→validation→commit→push→PR) plutôt que des micro-étapes.
- Toujours tracer l’avancement à l’écran: bref préambule avant un lot d’actions, puis mini-checkpoint après 3–5 actions ou >3 fichiers édités.
- Avant un lot d’outils: une phrase “pourquoi/quoi/résultat attendu”, puis exécuter; après: “résumé et suite”.
- Éviter les questions non essentielles; n’en poser qu’en cas de blocage réel ou décision irréversible.
- Commits atomiques et message concis; référencer l’issue; ouvrir/mettre à jour la PR en fin de lot.
- Qualité en continu: build/lint/tests rapides après changements substantiels; ne pas laisser un build cassé.

### Note sur “Conserver” (modifications Copilot)

- Par design, l’éditeur demande une confirmation manuelle pour appliquer les modifications proposées par Copilot (bouton « Conserver » par fichier, ou « Conserver tout » depuis la vue des changements).
- Il n’existe pas d’option officielle pour tout accepter automatiquement sans confirmation.
- Astuce: utilisez « Conserver tout » avant de lancer l’étape de commit/push, et activez l’auto‑save VS Code pour éviter des fichiers non enregistrés.
