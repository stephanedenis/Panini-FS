# Dhātu Experiments v0.1 and Typological Sample (child-directed-first)

This page consolidates artifacts from `experiments/dhatu/` (v0.1) into a unified view for research and publications. It documents data sources, the typological sample, targeted phenomena, and reproducible metrics.

## Goal and scope
- Establish a minimal set of cross-lingual primitives (Dhātu) exercised on a toy corpus and multilingual child-directed prompts.
- Build a balanced typological sample (child-directed-first) for cross-language comparisons.
- Provide simple metrics and source links for traceability and reproducibility.

## Data sources (external refs)
- CHILDES (TalkBank): https://childes.talkbank.org/
- WALS (World Atlas of Language Structures): https://wals.info/
- Universal Dependencies (UD): https://universaldependencies.org/
- African Storybook: https://www.africanstorybook.org/
- Global Storybooks: https://globalstorybooks.net/
- Storybooks Canada: https://storybookscanada.ca/

## Typological sample v0.1
Priority: child‑directed, morpho‑syntactic diversity. Selected languages and profiles:

- English (eng) — Indo‑European > Germanic — SVO
  - CHILDES: Brown/Providence → https://childes.talkbank.org/access/Eng-NA/
  - GlobalStorybooks: English → https://globalstorybooks.net/collections/english/
- French (fra) — Indo‑European > Romance — SVO
  - CHILDES: French → https://childes.talkbank.org/access/French/
  - GlobalStorybooks: Français → https://globalstorybooks.net/collections/french/
- Spanish (spa) — Indo‑European > Romance — SVO
  - CHILDES: Spanish → https://childes.talkbank.org/access/Spanish/
  - GlobalStorybooks: Español → https://globalstorybooks.net/collections/spanish/
- German (deu) — Indo‑European > Germanic — SVO, V2
  - CHILDES: German → https://childes.talkbank.org/access/German/
  - GlobalStorybooks: Deutsch → https://globalstorybooks.net/collections/german/
- Dutch (nld) — Indo‑European > Germanic — SVO, V2
  - CHILDES: Dutch → https://childes.talkbank.org/access/Dutch/
- Italian (ita) — Indo‑European > Romance — SVO
  - CHILDES: Italian → https://childes.talkbank.org/access/Italian/
  - GlobalStorybooks: Italiano → https://globalstorybooks.net/collections/italian/
- Portuguese (por) — Indo‑European > Romance — SVO
  - CHILDES: Portuguese → https://childes.talkbank.org/access/Portuguese/
  - GlobalStorybooks: Português → https://globalstorybooks.net/collections/portuguese/
- Mandarin Chinese (cmn) — Sino‑Tibetan — SVO, classifiers
  - CHILDES: Mandarin → https://childes.talkbank.org/access/Mandarin/
  - GlobalStorybooks: 中文 (简体) → https://globalstorybooks.net/collections/chinese-simplified/
- Japanese (jpn) — Japonic — SOV, honorifics
  - CHILDES: Japanese → https://childes.talkbank.org/access/Japanese/
  - GlobalStorybooks: 日本語 → https://globalstorybooks.net/collections/japanese/
- Korean (kor) — Koreanic — SOV, honorifics
  - CHILDES: Korean → https://childes.talkbank.org/access/Korean/
  - GlobalStorybooks: 한국어 → https://globalstorybooks.net/collections/korean/
- Turkish (tur) — Turkic — SOV, agglutinative
  - CHILDES: Turkish → https://childes.talkbank.org/access/Turkish/
  - GlobalStorybooks: Türkçe → https://globalstorybooks.net/collections/turkish/
- Hungarian (hun) — Uralic — agglutinative
  - CHILDES: Hungarian → https://childes.talkbank.org/access/Hungarian/
  - GlobalStorybooks: Magyar → https://globalstorybooks.net/collections/hungarian/
- Hebrew (heb) — Afro‑Asiatic > Semitic — root‑and‑pattern
  - CHILDES: Hebrew → https://childes.talkbank.org/access/Hebrew/
  - GlobalStorybooks: עברית → https://globalstorybooks.net/collections/hebrew/
- Arabic (arb) — Afro‑Asiatic > Semitic — VSO/SVO, root‑and‑pattern
  - GlobalStorybooks: العربية → https://globalstorybooks.net/collections/arabic/
- Swahili (swa) — Niger‑Congo > Bantu — SVO, noun classes
  - AfricanStorybook: Kiswahili → https://www.africanstorybook.org/language/kiswahili
- Yoruba (yor) — Niger‑Congo — SVO, SVC
  - AfricanStorybook: Yorùbá → https://www.africanstorybook.org/language/yoruba
- Hausa (hau) — Afro‑Asiatic > Chadic — SVO
  - AfricanStorybook: Hausa → https://www.africanstorybook.org/language/hausa
- Zulu (zul) — Niger‑Congo > Bantu — SVO, noun classes
  - AfricanStorybook: isiZulu → https://www.africanstorybook.org/language/isizulu
- Inuktitut (iku) — Eskimo–Aleut — polysynthetic, incorporation
  - StorybooksCanada: ᐃᓄᒃᑎᑐᑦ → https://storybookscanada.ca/?lang=iu

## Child‑directed prompts: available languages
Codes in `experiments/dhatu/prompts_child/`:

`arb, cmn, deu, en, eus, ewe, fr, hau, heb, hin, hun, iku, jpn, kor, nld, spa, swa, tur, yor, zul`

## Covered phenomena (aggregate)
Counts across child languages (top categories):

- spatial:in — 38
- AAO — 20
- possession — 20
- quantification — 20
- negation — 20
- time:now — 20
- event:sequence — 20
- comparison:more — 20
- existence — 20
- spatial:on — 19
- evidential:reported — 19
- modality:possibility — 15
- aspect:progressive — 12
- modality:permission — 5
- SVC — 3
- plural — 2
- aspect? — 2
- SVC-like — 2
- spatial:dans — 2
- aspect:progressive? — 1
- spatial:sur — 1
- incorporation? — 1
- evidential:inferential — 1
- habitual? — 1

## Experimental metrics (v0.1)
- Toy corpus (`toy_corpus.json` + `gold_encodings.json`):
  - sentences: 12
  - covered: 12 — rate = 1.0
  - avg primitives per encoding: 3.667
- Child prompts (child gold encodings): `gold_encodings_child.json` currently empty → detailed metrics pending (annotation in progress).

## Repro (local)
Run from repo root:

- Typological sample and sources:
  - python3 experiments/dhatu/validator.py --list-sample
- Available child languages:
  - python3 experiments/dhatu/validator.py --list-child-langs
- Phenomena counts across child languages:
  - python3 experiments/dhatu/validator.py --phenomena
- Toy corpus metrics:
  - python3 experiments/dhatu/validator.py --metrics

## Internal links
- Dhātu Inventory v0.1: `research/dhatu-inventory-v0-1.md`
- Research references: `research/references.md`

---
Last updated: generated from `experiments/dhatu/` v0.1 sources.
