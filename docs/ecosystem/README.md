# Écosystème Panini — documentation-first

Cette section décrit l’écosystème de dépôts liés à PaniniFS en mode documentation-first.

- La source de vérité est `data/ecosystem.yml` (éditable via PR dans le dépôt maître).
- Les pages `catalogue.md` et `panorama.md` sont générées par `scripts/generate_ecosystem_docs.py`.
- Le diagramme Mermaid dans `panorama.md` est généré automatiquement.
- Des fiches dépôts sont générées dans `ecosystem/repos/`.
- Aucun changement n’est effectué automatiquement dans les autres dépôts: la gouvernance, les labels et les workflows pilotent les tâches à distance.

Mise à jour:
1. Éditer `data/ecosystem.yml` (ajouts/modifs de dépôts, descriptions, relations).
2. Exécuter `python3 scripts/generate_ecosystem_docs.py`.
3. Ouvrir une PR de documentation.

Bonnes pratiques:
- Garder des descriptions brèves et orientées rôle.
- Déclarer des relations “from → to” à haut niveau uniquement.
- Lier les issues de coordination avec le template « Submodule change request » si des actions techniques sont nécessaires.

Décentralisation (annexer aux issues des sous-modules):
1. Générer les « packs d’issue »: `python3 scripts/prepare_issue_packs.py` (créés sous `issues_packs/`).
2. Ouvrir automatiquement les issues côté sous-modules (optionnel):
	- Dry-run: `python3 scripts/open_submodule_issues.py --dry-run`
	- Création: exporter `GH_TOKEN` puis `python3 scripts/open_submodule_issues.py`.
3. Continuer le travail dans chaque repo; ici on ne garde que le panorama et les liens.