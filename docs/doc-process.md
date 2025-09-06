# Processus documentation (docs as code)

- Source unique: `docs/` (FR par défaut) + `docs/en/`.
- Synchronisation FR/EN: toute PR modifiant une page FR doit modifier la page EN correspondante (et inversement).
- Plugin i18n (MkDocs): navigation bilingue, URLs `/` et `/en/`.
- Revue: au moins 1 relecteur; vérifier cohérence des deux langues.
- Style: voir [Guide de style](style-guide.md).
- Schémas: privilégier PlantUML/Mermaid (via Kroki) avec SVG et hyperliens.
- Gouvernance: les TODO: dans la doc créent/mettent à jour des issues (workflow CI).
