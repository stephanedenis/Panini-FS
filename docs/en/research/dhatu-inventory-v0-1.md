---
title: Dhātu inventory v0.1 (draft)
status: draft
---

# Dhātu inventory v0.1 (draft)

A small, iterative set of primitives for experiments. Subject to change.

## Principles
- Stable, human-readable, and composable primitives.
- UPPERCASE for operators; lowercase for lexical items.
- Explicit relations; avoid hidden overload.

## YAML (draft)

```yaml
version: 0.1
core:
  - AGENT
  - ACTION
  - PATIENT
  - PLACE
  - TIME
  - REL
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
    ON: rel:on
    IN: rel:in
    OF: rel:of
  MODALITY:
    CAN: modal:can
    MUST: modal:must
  ASPECT:
    HABITUAL: aspect:habitual
    PERFECTIVE: aspect:perfective
notes:
  - Under lexicon, keys are frequent aliases; stable IDs should back them (e.g., concept:book, action:hunt).
```

## Links
- See “Semantic universals” and “Semantic compression” for the evaluation protocol.
