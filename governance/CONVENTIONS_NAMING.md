# Conventions de nommage (initial draft)

## Dossiers top-level
- kebab-case (ex: `governance`, `architecture`, `operations`).
- Pas d'accents, pas de majuscules.

## Fichiers Markdown internes
- kebab-case ou sujet-clair.md (anglais ou fr mais cohérent sous-dossier).
- Archives datées: `YYYY-MM-DD-sujet.md`.

## Scripts
- Python: snake_case (`generate_modules_docs_index.py`).
- Shell: kebab-case (`deploy-docs.sh`).
- Un binaire entrypoint max par responsabilité.

## Journaux Copilotage
- `journal/YYYY-MM-DD-<host>-pid<pid>-<slug>.md` (déjà en place).

## Modules docs agrégées
- Sous `docs/modules/_ext/<module>/`.

(À enrichir: lint automatique + check CI futur.)
