# Expériences Dhātu v0.1 et échantillon typologique (child-directed-first)

Cette page consolide les artefacts du dossier `experiments/dhatu/` (v0.1) en une vue unifiée utile à la recherche et aux publications. Elle décrit les sources, l’échantillon typologique, les phénomènes visés, et des métriques reproductibles.

## Objectif et portée
- Cadrer un ensemble minimal de primitives (Dhātu) éprouvé sur un corpus jouet et des prompts enfant multilingues.
- Construire un échantillon typologique équilibré “child-directed-first” pour des comparaisons interlangues.
- Documenter des métriques simples et des liens vers les sources afin d’assurer traçabilité et reproductibilité.

## Sources de données (références externes)
- CHILDES (TalkBank): https://childes.talkbank.org/
- WALS (World Atlas of Language Structures): https://wals.info/
- Universal Dependencies (UD): https://universaldependencies.org/
- African Storybook: https://www.africanstorybook.org/
- Global Storybooks: https://globalstorybooks.net/
- Storybooks Canada: https://storybookscanada.ca/

Ces sources couvrent des registres enfant/adulte et des familles variées (Indo‑européen, sino‑tibétain, afro‑asiatique, nigéro‑congolais, eskimo‑aléoute, etc.).

## Échantillon typologique v0.1
Priorité: child‑directed, diversité morpho‑syntaxique. Langues et profils (extrait):

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
- Mandarin Chinese (cmn) — Sino‑Tibetan — SVO, classificateurs
  - CHILDES: Mandarin → https://childes.talkbank.org/access/Mandarin/
  - GlobalStorybooks: 中文 (简体) → https://globalstorybooks.net/collections/chinese-simplified/
- Japanese (jpn) — Japonic — SOV, honorifiques
  - CHILDES: Japanese → https://childes.talkbank.org/access/Japanese/
  - GlobalStorybooks: 日本語 → https://globalstorybooks.net/collections/japanese/
- Korean (kor) — Koreanic — SOV, honorifiques
  - CHILDES: Korean → https://childes.talkbank.org/access/Korean/
  - GlobalStorybooks: 한국어 → https://globalstorybooks.net/collections/korean/
- Turkish (tur) — Turkic — SOV, agglutinant
  - CHILDES: Turkish → https://childes.talkbank.org/access/Turkish/
  - GlobalStorybooks: Türkçe → https://globalstorybooks.net/collections/turkish/
- Hungarian (hun) — Uralic — agglutinant
  - CHILDES: Hungarian → https://childes.talkbank.org/access/Hungarian/
  - GlobalStorybooks: Magyar → https://globalstorybooks.net/collections/hungarian/
- Hebrew (heb) — Afro‑Asiatic > Semitic — schèmes racinaires
  - CHILDES: Hebrew → https://childes.talkbank.org/access/Hebrew/
  - GlobalStorybooks: עברית → https://globalstorybooks.net/collections/hebrew/
- Arabic (arb) — Afro‑Asiatic > Semitic — VSO/SVO, schèmes racinaires
  - GlobalStorybooks: العربية → https://globalstorybooks.net/collections/arabic/
- Swahili (swa) — Niger‑Congo > Bantu — SVO, classes nominales
  - AfricanStorybook: Kiswahili → https://www.africanstorybook.org/language/kiswahili
- Yoruba (yor) — Niger‑Congo — SVO, SVC
  - AfricanStorybook: Yorùbá → https://www.africanstorybook.org/language/yoruba
- Hausa (hau) — Afro‑Asiatic > Chadic — SVO
  - AfricanStorybook: Hausa → https://www.africanstorybook.org/language/hausa
- Zulu (zul) — Niger‑Congo > Bantu — SVO, classes nominales
  - AfricanStorybook: isiZulu → https://www.africanstorybook.org/language/isizulu
- Inuktitut (iku) — Eskimo–Aleut — polysynthétique, incorporation
  - StorybooksCanada: ᐃᓄᒃᑎᑐᑦ → https://storybookscanada.ca/?lang=iu

## Prompts enfant: langues disponibles
Codes disponibles dans `experiments/dhatu/prompts_child/`:

`arb, cmn, deu, en, eus, ewe, fr, hau, heb, hin, hun, iku, jpn, kor, nld, spa, swa, tur, yor, zul`

## Phénomènes couverts (agrégat)
Comptage (toutes langues enfant confondues) — top catégories:

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

Remarque: ces catégories visent à éprouver des primitives Dhātu translingues (agent‑action‑objet (AAO), relations spatiales, polarité, quantification, modalité, aspect, séquentialité, possession, existence, classes nominales/SVC, (épi)‑evidentialité, etc.).

### Synthèse par langue (auto-généré)

{% include-markdown "../data/dhatu_child_phenomena_summary.md" %}

## Métriques expérimentales (v0.1)
- Corpus jouet (`toy_corpus.json` + `gold_encodings.json`):
  - phrases: 12
  - couvertes: 12 — taux = 1.0
  - primitives moyennes par encodage: 3.667
- Prompts enfant (gold encodings enfants): fichier `gold_encodings_child.json` vide actuellement → métriques détaillées à venir (annotation en cours).

## Reproductibilité (exécution locale)
Exécuter depuis la racine du dépôt:

- Lister l’échantillon typologique et sources:
  - python3 experiments/dhatu/validator.py --list-sample
- Langues disponibles (prompts enfant):
  - python3 experiments/dhatu/validator.py --list-child-langs
- Comptage des phénomènes à travers toutes les langues enfant:
  - python3 experiments/dhatu/validator.py --phenomena
- Métriques corpus jouet (couverture, longueur moyenne):
  - python3 experiments/dhatu/validator.py --metrics

## Liens internes
- Inventaire Dhātu v0.1: `research/inventaire-dhatu-v0-1.md`
- Références de recherche: `research/references.md`

### Langues et sources enfant (auto-généré)

{% include-markdown "../data/dhatu_child_langs.md" %}

---
Dernière mise à jour: générée à partir des sources `experiments/dhatu/` v0.1.
