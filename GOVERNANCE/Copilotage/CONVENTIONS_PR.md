# 🧾 Conventions Pull Requests

## Titre
`[hostname-pid-agent-model] sujet concis [owner:agent|human|pair|ops|infra]`

Exemple:
`[xps15-4321-agent-gpt4o] publications: manuscrits FR/EN, CI artefacts [owner:agent]` (ou `[owner:human|pair|ops|infra]` selon le cas)

## Checklist PR
- [ ] Build MkDocs en mode strict: PASS
- [ ] Scripts ajoutés/testés (usage minimal vérifié)
- [ ] Conventions i18n respectées (FR défaut, EN miroir)
- [ ] Références précises (DOI/URL/ISBN) quand applicable
- [ ] CI verte (ou justification si non bloquant)

## Description minimale
- But et portée du changement
- Détails techniques saillants (schéma, scripts, conventions)
- Validation effectuée (build/tests/smoke)
- Impacts/risques connus et mitigations

## Etiquettes recommandées
- `area:docs` `area:publications` `area:copilotage`
- `owner:agent` ou `owner:human`
