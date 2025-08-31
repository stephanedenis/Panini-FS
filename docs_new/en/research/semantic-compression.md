---
title: Computational semantic compression
status: draft
---

# Computational semantic compression

Principles, metrics, and use cases (storage, communication, processing, learning, education).

## Synthesis (draft)
- Target minimal loss of meaning at fixed bitrate via Dhātu representations.
- Evaluate trade-offs: fidelity, decodability, learnability.

## Metrics (to refine)
- Concept coverage, mutual information retained, ambiguity rate, reconstruction accuracy.

## Minimal evaluation protocol

1) Bilingual toy corpus (FR/EN) of 100 sentences covering AAO, spatial relations, tense, negation, quantification.
2) Gold manual encoding + rule/LLM-guided automatic attempt.
3) Decode to paraphrases and score similarity/ambiguity.
4) Report mean/median/variance for coverage, ambiguity, length, reconstruction.

## Micro-cases

- Simple instruction: "Close the door" → [ACTION:close][OBJ:door][AGENT:addressee]
- Yes/No question: "Are you hungry?" → [INTERROGATIVE][STATE:hunger][AGENT:addressee]
- Attachment ambiguity: "I saw the man with the telescope"

## Implementation notes

- Version a small Dhātu inventory (v0.1) in YAML for iteration.
- Provide a validator with unit tests and toy sentences.
- Grow coverage by domain (household objects, motion, social interactions).
