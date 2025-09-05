# Agrégation de la documentation des modules

Ce dossier est généré par `scripts/aggregate_submodule_docs.py` lors du build Pages.
Il contient une copie des dossiers `docs/` des sous-modules (`modules/*`).

- Source: modules/<module>/docs/
- Destination: docs_new/modules/_ext/<module>/

Ne pas modifier manuellement; toute modification doit se faire dans les dépôts des sous-modules.

Chaque sous-module peut publier une SPA OntoWave comme `index.html` au sein de son dépôt pour une navigation dynamique; ici nous ne servons qu’une agrégation statique pour l’indexation MkDocs unifiée.