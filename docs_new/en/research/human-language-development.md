---
title: Human language and development
status: draft
---

# Human language and development

From infancy to adulthood: stages, observations, and implications for PaniniFS.

## Synthesis (draft)
- Early communicative primitives (gestures, proto-words) as scaffolds for Dhātu mapping.
- Progressive abstraction and compositionality; memory constraints shape semantic compression.

## Hypotheses
- Milestones correlate with stable semantic operators (e.g., agent/action/object, negation, temporal markers).

## Validation paths
- Align milestones with an incremental Dhātu set; evaluate coverage on child-directed corpora.

## Key milestones (0–6y)

- 0–9 months: proto-communication (gaze, pointing, babbling) → precursors of AGENT, ATTENTION, DEIXIS.
- 10–18 months: single words, holophrases → compact intent encoding (implicit VERB/OBJECT).
- 18–30 months: two-word stage, lexical burst → AAO patterns, basic spatial relations (ON/IN/AT).
- 30–48 months: morphosyntax, tense, negation, quantification → operators: TENSE, MODALITY, QUANT.
- 4–6 years: simple narratives, anaphora, theory of mind → COREFERENCE, CAUSALITY, INTENTION.

## Dhātu alignment (sketch)

- Core operators: AGENT, ACTION, PATIENT, PLACE, TIME, POSSESSION, NEGATION, QUANTIFICATION, MODALITY.
- Progressive introduction rule: add a primitive only when a typical milestone requires it.

## Micro-evaluations

1) Early negation
	- Utterance: "no sleep" (telegraphic)
	- Dhātu: [NEGATION] [ACTION:sleep] [AGENT:speaker]

2) Spatial relation
	- Utterance: "truck on bridge"
	- Dhātu: [OBJ:truck] [REL:ON] [REF:bridge]

3) Simple anaphora
	- Utterance: "Mary takes the book. She reads."
	- Dhātu: [AGENT:Mary][ACTION:take][OBJ:book] … [COREF:prior AGENT][ACTION:read]

## Metrics

- Milestone→primitive alignment rate per age band.
- Success rate decoding telegraphic speech into full propositions.
- Complexity reduction: active primitives vs. achieved expressivity.

## Baby sign → Dhātu (micro-cases)

- "more" (gesture) → [QUANT:>0] [ACTION:repeat]  
	Object-oriented variant: [QUANT:>0] [ACTION:give] [OBJ:food/toy]
- "milk" (hand squeeze) → [ACTION:drink] [OBJ:milk] [AGENT:addressee]
- "all done" / "finished" → [NEGATION] [ACTION:continue]  
	State variant: [STATE:finished]

Notes:
- Reuse existing primitives (NEGATION, QUANT, ACTION, STATE) to avoid inflating the operator set.
- Lexical choices (repeat, give, milk, continue, finished) are vocabulary; Dhātu inventory stays operator-focused.

## References

- MacWhinney, B. (2000–). CHILDES — Child Language Data Exchange System (TalkBank). https://childes.talkbank.org/
- Goldin-Meadow, S. (2003). The Resilience of Language. Psychology Press. ISBN: 978-1-84872-004-1
- Universal Dependencies (UD). https://universaldependencies.org/
- See also: ../research/references.md
