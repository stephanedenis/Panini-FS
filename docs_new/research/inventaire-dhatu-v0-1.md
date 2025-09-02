---
title: Inventaire Dhātu v0.1 (brouillon)
status: draft
---

# Inventaire Dhātu v0.1 (brouillon)

Esquisse d’un petit inventaire de primitives pour itération et évaluation. Sujet à changements.

## Principes
- Primitives stables, lisibles, et composables.
- Noms en MAJUSCULE pour les opérateurs, minuscules pour les lexèmes.
- Relations explicites; éviter la surcharge implicite.

## YAML (brouillon)

```yaml
version: 0.1
core:
  - AGENT
  - ACTION
  - PATIENT
  - PLACE
  - TIME
  - REL  # relation générique (ex.: SUR, DANS, DE)
  - POSSESSION
  - NEGATION
  - QUANT
  - MODALITY
  - ASPECT
  - COREF
  - INTERROGATIVE
  - STATE
lexicon:
  REL:
    SUR: rel:sur
    DANS: rel:dans
    DE: rel:de
  MODALITY:
    PEUT: modal:can
    DOIT: modal:must
  ASPECT:
    HABITUEL: aspect:habitual
    ACCOMPLI: aspect:perfective
notes:
  - Les clés sous lexicon sont des alias fréquents; la référence finale sera ancrée à des IDs stables.
  - Les étiquettes FR/EN devront être harmonisées via des IDs (ex.: concept:book, action:hunt).
```

## Liens
- Voir les pages « Universaux sémantiques » et « Compression sémantique » pour le protocole d’évaluation.
