Date: 2025-08-30
Hôte/Session: totoro
Objet: Stabilisation CI + Merges PR #24 et #23

Résumé
- Restauration `dhatu-validation.yml` (espaces, garde-fous, steps non bloquants).
- Réactivation workflows sains: `maintenance.yml`, `paniniFS-ci.yml`.
- Ouverture puis merge PR #24 (CI fix) -> master.
- Checks verts sur PR #23, merge effectué (finalisation Camping Strategy, Refs #22).

Détails
- Évitement des faux négatifs via conditions shell (skip si dossiers absents).
- Déclencheurs limités pour réduire le bruit sur branches.
- Validation via `gh run list` et `gh pr checks` (tout vert).

Suivi
- Prochaines pistes: lint/format (ruff/black), protections de branches, templates (ajoutés), monitoring étendu.
