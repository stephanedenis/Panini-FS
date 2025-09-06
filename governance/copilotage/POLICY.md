# Politique du dossier copilotage

But et portée
- Centraliser les informations IA sur la mission principale, les missions en cours et les préférences d’interaction IA‑humain.
- Héberger des outils et aides produits par l’IA pour fluidifier ces interactions (prompts, checklists, tableaux de bord, scripts d’assistance non bloquants).

Principe de non‑dépendance (contrat ferme)
- Le dossier `governance/copilotage/` ne doit contenir aucun artefact requis pour construire, tester, exécuter ou déployer le projet.
- Supprimer ce dossier ne doit pas casser la build, les tests ni l’exécution.
- Aucun import/chemin de production ne doit référencer `governance/copilotage/`.

Contenus autorisés (exemples)
- Journaux de sessions, playbooks, comptes‑rendus, prompts, guides d’interaction.
- Scripts utilitaires facultatifs (ex. wrappers de commandes, vérifications, migrations guidées) non importés par le code de production.

Contenus interdits (exemples)
- Logique métier, bibliothèques réutilisées par l’application, modules importés par la prod.
- Secrets et configurations runtime obligatoires.
- Étapes CI/CD obligatoires. Si nécessaire au pipeline, les déplacer hors de `copilotage`.

Application aux dossiers dérivés/collaborants
- Toute arborescence « copilotage » liée à ce dépôt DOIT appliquer cette politique et pointer vers ce document.

Vérification recommandée
- Utiliser `scripts/check_copilotage_independence.py` pour détecter des imports/chemins suspects.

Révision: 2025‑09‑05.
