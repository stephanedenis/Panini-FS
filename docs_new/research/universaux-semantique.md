---
title: Universaux sémantiques (Dhātu)
status: draft
---

# Universaux sémantiques (Dhātu)

Résumé, hypothèses, protocoles de validation, résultats et références.

## Synthèse (draft)

- Problématique: identifier un noyau d’universaux sémantiques stables (Dhātu) exploitable pour stockage/communication/traitement.
- Contexte: consolidation post-vacances, remise en état CI/CD, recentrage sur le QUOI de la recherche.
 - Cible v0: un inventaire minimal praticable (voir « Inventaire Dhātu v0.1 ») et un protocole reproductible.

## Hypothèses (à préciser)

- Un ensemble réduit de primitives sémantiques peut encoder efficacement des concepts à large couverture.
- La trajectoire d’acquisition du langage chez l’enfant éclaire l’ordre d’émergence de ces universaux.
 - Une représentation Dhātu correctement contrainte minimise l’ambiguïté tout en restant décodable sans contexte encyclopédique lourd.

## Portée universelle: échantillonnage et couverture

- Échantillonnage stratifié (WALS/Glottolog): au moins 1 langue par grande famille (≥ 25 familles), couvrant aussi des isolats; équilibre géographique (Afrique, Eurasie, Océanie, Amériques, Papouasie, Australie).
- Priorité données: textes dirigés vers l’enfant (contes, dialogues parent‑enfant) pour ancrer les phénomènes minimaux d’abord.
- Inclure des profils structuraux contrastés:
	- Langues signées (ASL, Langue des Signes Nicaraguayenne/NSL) et émergentes.
	- Créoles/pidgins (Haïtien, Tok Pisin) et langues à SVC (Ewe, Yoruba).
	- Ergativité (Basque, Dyirbal), split‑ergativité (Hindi‑Urdu).
	- Polysynthèse et incorporation nominale (Inuktitut, Mohawk).
	- Ordres marqués (OSV Hixkaryana), ordre libre (Warlpiri), alignements pragmatiques.
	- Classificateurs et mesure (Mandarin, Yudja), classes nominales (Bantu).
	- Évidentialité obligatoire (Quechua, Tariana); systèmes honorifiques (Japonais, Coréen).
	- Idéophones riches (Siwu, Ewe); systèmes numériques atypiques (Oksapmin, Pirahã — avec prudence méthodologique).
- Jeux de données: WALS, APiCS (créoles), Universal Dependencies (arbres multi‑langues), Global Signbank (lexiques signés), Glottolog (métadonnées), TalkBank/CHILDES (développement).
 - Échantillon JSON: `experiments/dhatu/typological_sample.json` (sources: CHILDES, African Storybook, Global Storybooks, UD, WALS).

## Observations (journalisées)

- Stabilisation de l’écosystème et des workflows favorise l’itération scientifique (journaux 2025‑08‑30).
- Nécessité d’isoler l’infrastructure (COMMENT) de la recherche (QUOI) dans la documentation.
 - Les confusions fréquentes portent sur les rôles (AGENT/PATIENT), les relations spatiales/possessives (REL/DE/SUR), et la portée de la négation/modale.

## Protocole minimal de validation (v0)

- Couverture: cartographier un échantillon de 100 concepts fréquents (noms, verbes, relations) vers un set Dhātu minimal; mesurer le taux de concepts encodés sans ajout de primitive.
- Ambiguïté: pour chaque encodage, compter le nombre de décodages plausibles; objectif v0 ≤ 1.5 interprétation moyenne par entrée (avec contexte court).
- Réversibilité: décoder les représentations Dhātu vers des paraphrases FR/EN et évaluer l’équivalence sémantique par jugement humain ou LLM robuste (agreement ≥ 0,8).
- Parcimonie: pénaliser le nombre de primitives utilisées par concept (objectif médian ≤ 4 primitives/concept au v0).
 - Stabilité: tester la robustesse à la paraphrase (10 variantes par phrase) et mesurer la variance des encodages.

Extension universelle (v0.1)
- Échantillon typologique: 30 langues couvrant les profils ci‑dessus; 10 phrases minimales par phénomène (AAO, possession, spatial, quantif., négation, modalité, causation, temps/aspect, évidence, valence, comparaison, existence, part‑tout).
- Traductions contrôlées: pour chaque test, obtenir 2 versions natives (ou sources publiées) pour limiter les biais de calque.
- Équivalence sémantique: jugements par locuteurs ou évaluateurs spécialisés quand disponible (signées/ergatives/polysynthétiques).

## Universaux candidats (liste testable v0)

- Participants et rôles: AGENT, PATIENT/THEME, RECIPIENT/BENEF.
- Événement/action, état, cause/causation; valence et transitivité; voice/opérations (causer, laisser, se‑, passif — comme dérivations, pas primitives).
- Négation (polaritée), modalité (possibilité, obligation), vérité/évidence (évidentialité comme attribut de source, non pas vérité elle‑même).
- Quantification: cardinalité (0,1,2,3…), totalité/partitif, approximatifs (≥, ≤, ~), distributif/collectif.
- Relations spatiales de base: DANS/INTERIEUR, SUR/CONTACT‑SUP, SOUS, PROXIMITÉ, CHEZ/LOCAL‑REF, TRAJECTOIRE (VERS/DEPUIS/À‑TRAVERS).
- Possession/lien: POSSESSION (HAVE/GEN) et relations génitives (appartenance, partie‑tout, type‑de) distinguées par REL‑sous‑types.
- Temps/aspect: AVANT/APRÈS/MAINTENANT; PERFECTIF/IMPERFECTIF; HABITUEL; PROGRESSIF.
- Comparaison et degré: PLUS/LE‑PLUS, MOINS/LE‑MOINS; égalité/identité.
- Existence et localisation: IL‑Y‑A/EXISTE; ÊTRE‑À (copule locative/attributive séparées au besoin).
- Partie‑tout/meronymie; identité/référence; types/classes (EST‑UN/TYPE‑DE).

Critère: tout phénomène morpho‑syntaxique doit pouvoir se paraphraser via combinaisons de ces primitives sémantiques, indépendamment de la réalisation de surface.

## Micro-cas (sanity checks)

1) Agent-Action-Objet (AAO)
	- Entrée: « Le chat chasse la souris. »
	- Dhātu attendu: [AGENT:chat] [ACTION:chasser] [PATIENT:souris] [ASPECT:habituel?]
	- Tests: variation de temps (« chassera »), de négation (« ne chasse pas »), de modalité (« peut chasser »).

2) Possession et localisation
	- Entrée: « Le livre est sur la table de Marie. »
	- Dhātu attendu: [OBJ:livre] [REL:sur] [REF:table] [REL:de] [REF:Marie]
	- Tests: ambigüité de « de » (possession vs. composition), empilement de relations.
	- Décodage cible: « The book is on Marie’s table. » / « Le livre est sur la table appartenant à Marie. »

3) Quantification simple
	- Entrée: « Trois enfants courent. »
	- Dhātu attendu: [QUANT:3] [AGENT:enfant] [ACTION:courir]
	- Tests: accord, pluriel irrégulier, zéro/indéfini (« des enfants »).
	- Variante: « Au moins trois enfants courent. » → [QUANT:>=3] [...]

4) Négation et modalité
	- Entrée: « Il ne peut pas venir. »
	- Dhātu: [AGENT:il][MODALITY:PEUT][NEGATION][ACTION:venir]
	- Test: portée de NEGATION vs. MODALITY (« il peut ne pas venir »).

5) Évidentialité (source de l’information)
	- Entrée: « Il serait venu (à ce qu’on dit). » / Quechua (marque obligatoire de source)
	- Dhātu: [ACTION:venir][ASPECT:ACCOMPLI?][EVIDENCE:REPORTÉ]
	- Test: neutraliser l’ancrage morphologique local tout en conservant la source (visuel, inférentiel, rapporté).

6) Sérialisation verbale (événements chaînés)
	- Entrée (Ewe/Yoruba): « aller‑prendre‑venir » (aller prendre quelque chose et revenir)
	- Dhātu: [ACTION:aller][ACTION:prendre][ACTION:venir][CHAÎNAGE:SEQ]
	- Test: séquence ordonnée d’événements sans subordination morphologique.

7) Incorporation nominale (polysynthèse)
	- Entrée (Mohawk/Inuktitut): verbe+nom incorporé « poisson‑manger »
	- Dhātu: [ACTION:manger][PATIENT:poisson][LIAISON:INCORP]
	- Test: vérifier que l’incorporation n’ajoute pas de primitive sémantique.

## Risques et limites

- Biais linguistiques (FR/EN) vs. universaux crosslinguistiques.
- Conflation sémantique entre relation lexicale et structure logique.
- Coût cognitif de décodage si la base de primitives s’étend trop.
 - Effet « anglais-centrique » des corpus et des LLM évaluateurs.

Limitation proactive
- Multiplier les langues non‑indo‑européennes et les langues signées; valider via WALS/APiCS/Signbank et littérature typologique.

## Suivi et métriques

- Taux de couverture (%) sur listes de fréquence (SUBTLEX, Wikidata labels, WordNet synsets de base).
- Ambiguïté moyenne (décodages plausibles par encodage) sur un set de phrases tests.
- Taille moyenne de représentation (nombre de primitives par concept/phrase).
- Accord inter-évaluateurs (ou proxy LLM) sur la réversibilité.
 - Stabilité inter-paraphrases (distance d’édition entre encodages; écart-type).

Couverture typologique
- Taux de phénomènes couverts par famille/aire (cartes WALS/APiCS); détecter des « trous » (ex. évidentialité non couverte, SVC insuffisantes, etc.).

## Sources (journaux)

- Récapitulatif complet: https://github.com/stephanedenis/PaniniFS/blob/master/Copilotage/journal/2025-08-30-RECAPITULATIF-COMPLET-totoro-pid17771.md
- Session: https://github.com/stephanedenis/PaniniFS/blob/master/Copilotage/journal/2025-08-30-session.md
- Hauru pid74498 session: https://github.com/stephanedenis/PaniniFS/blob/master/Copilotage/journal/2025-08-30-hauru-pid74498-session.md
- CI stabilisation/merge: https://github.com/stephanedenis/PaniniFS/blob/master/Copilotage/journal/2025-08-30-ci-stabilisation-merge.md
- Camping final: https://github.com/stephanedenis/PaniniFS/blob/master/Copilotage/journal/2025-08-30-totoro-pid17771-camping-final.md
- Assimilation archives: https://github.com/stephanedenis/PaniniFS/blob/master/Copilotage/journal/2025-08-30-linux-pid0-assimilation-archives.md

## Références externes (sélection)

- Haspelmath, M. (2007). Pre-established categories don't exist: Consequences for language description and typology. Linguistic Typology, 11(1). DOI: 10.1515/LINGTY.2007.011
- WALS — World Atlas of Language Structures. https://wals.info/
- Universal Dependencies (UD). https://universaldependencies.org/
- Page « Références de recherche »: ../research/references.md
 - Evans, N., & Levinson, S. C. (2009). The myth of language universals. BBS. DOI: 10.1017/S0140525X0999094X
 - Aikhenvald, A. Y. (2004). Evidentiality. Oxford University Press. ISBN: 978-0199204380
 - APiCS — Atlas of Pidgin and Creole Language Structures. https://apics-online.info/
 - Global Signbank (Radboud). https://signbank.science.ru.nl/

---

Notes pratiques
- L’inventaire de travail: voir « Inventaire Dhātu v0.1 ».
- Convention de nommage: MAJUSCULE pour rôles/opérateurs; minuscules pour lexèmes; REL peut être spécialisé (SUR/DANS/DE) selon le domaine.
- Pour les alias anglais: maintenir un fichier EN miroir afin de satisfaire la gouvernance FR/EN tout en centralisant le contenu canonique.

## Essayer (mini-banc d’essai)

- Dossier: `experiments/dhatu/`
- Lister le corpus jouet: `python experiments/dhatu/validator.py --list`
- Calculer des métriques brutes: `python experiments/dhatu/validator.py --metrics`
 - Lister l’échantillon typologique (child-directed-first): `python experiments/dhatu/validator.py --list-sample`
