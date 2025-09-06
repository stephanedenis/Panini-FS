---
title: Semantic universals (Dhātu)
status: draft
---

# Semantic universals (Dhātu)

Draft synthesis of assumptions, validation paths, and references.

## Synthesis (draft)

- Problem: identify a compact set of semantic primitives (Dhātu) usable across storage/communication/processing.
- Context: CI stabilized; documentation refocused on the WHAT (research), not the HOW (infra).

## Assumptions
- A small, stable set of semantic primitives can encode broad conceptual coverage.
- Human language acquisition stages inform the emergence order of these universals.

## Minimal validation protocol (v0)

- Coverage: map a 100-item frequent concept set (nouns, verbs, relations) to a minimal Dhātu inventory; measure % covered without adding primitives.
- Ambiguity: for each encoding, count plausible decodings; v0 target ≤ 1.5 interpretations on average (with short context).
- Reversibility: decode Dhātu reps to EN/FR paraphrases and judge semantic equivalence by humans or a robust LLM (agreement ≥ 0.8).
- Parsimony: penalize primitive count per concept (median ≤ 4 primitives/concept at v0).

## Micro-cases (sanity checks)

1) Agent-Action-Object (AAO)
	- Input: "The cat hunts the mouse."
	- Expected Dhātu: [AGENT:cat] [ACTION:hunt] [PATIENT:mouse] [ASPECT:habitual?]
	- Tests: tense, negation, modality.

2) Possession and location
	- Input: "The book is on Mary's table."
	- Expected Dhātu: [OBJ:book] [REL:on] [REF:table] [REL:of] [REF:Mary]
	- Tests: attachment ambiguity and relation stacking.

3) Simple quantification
	- Input: "Three children run."
	- Expected Dhātu: [QUANT:3] [AGENT:child] [ACTION:run]
	- Tests: plural, indefinites.

## Sources (FR journals)
- See Copilotage journals dated 2025‑08‑30 for context and decisions.

## References (selected)

- Haspelmath, M. (2007). Pre-established categories don't exist: Consequences for language description and typology. Linguistic Typology, 11(1). DOI: 10.1515/LINGTY.2007.011
- WALS — World Atlas of Language Structures. https://wals.info/
- Universal Dependencies (UD). https://universaldependencies.org/
- See also: ../research/references.md

## Try it (mini harness)

- Folder: `experiments/dhatu/`
- List toy corpus: `python experiments/dhatu/validator.py --list`
- Compute basic metrics: `python experiments/dhatu/validator.py --metrics`
