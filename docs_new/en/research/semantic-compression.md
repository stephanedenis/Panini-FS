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

## Try it (mini harness)

- Folder: `experiments/dhatu/`
- List toy corpus: `python experiments/dhatu/validator.py --list`
- Compute basic metrics: `python experiments/dhatu/validator.py --metrics`

## References

- Shannon, C. E. (1948). A Mathematical Theory of Communication. Bell System Technical Journal, 27(3), 379–423; 27(4), 623–656. DOI: 10.1002/j.1538-7305.1948.tb01338.x
- Tishby, N., Pereira, F. C., & Bialek, W. (2000). The Information Bottleneck Method. arXiv:physics/0004057. DOI: 10.48550/arXiv.physics/0004057
- Hinton, G. E., & Salakhutdinov, R. R. (2006). Reducing the Dimensionality of Data with Neural Networks. Science, 313(5786), 504–507. DOI: 10.1126/science.1127647
- See also: ../research/references.md
