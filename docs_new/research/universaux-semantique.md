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

## Risques et limites

- Biais linguistiques (FR/EN) vs. universaux crosslinguistiques.
- Conflation sémantique entre relation lexicale et structure logique.
- Coût cognitif de décodage si la base de primitives s’étend trop.
 - Effet « anglais-centrique » des corpus et des LLM évaluateurs.

## Suivi et métriques

- Taux de couverture (%) sur listes de fréquence (SUBTLEX, Wikidata labels, WordNet synsets de base).
- Ambiguïté moyenne (décodages plausibles par encodage) sur un set de phrases tests.
- Taille moyenne de représentation (nombre de primitives par concept/phrase).
- Accord inter-évaluateurs (ou proxy LLM) sur la réversibilité.
 - Stabilité inter-paraphrases (distance d’édition entre encodages; écart-type).

## Sources (journaux)

- Récapitulatif complet: https://github.com/stephanedenis/PaniniFS/blob/master/Copilotage/journal/2025-08-30-RECAPITULATIF-COMPLET-totoro-pid17771.md
- Session: https://github.com/stephanedenis/PaniniFS/blob/master/Copilotage/journal/2025-08-30-session.md
- Hauru pid74498 session: https://github.com/stephanedenis/PaniniFS/blob/master/Copilotage/journal/2025-08-30-hauru-pid74498-session.md
- CI stabilisation/merge: https://github.com/stephanedenis/PaniniFS/blob/master/Copilotage/journal/2025-08-30-ci-stabilisation-merge.md
- Camping final: https://github.com/stephanedenis/PaniniFS/blob/master/Copilotage/journal/2025-08-30-totoro-pid17771-camping-final.md
- Assimilation archives: https://github.com/stephanedenis/PaniniFS/blob/master/Copilotage/journal/2025-08-30-linux-pid0-assimilation-archives.md

---

Notes pratiques
- L’inventaire de travail: voir « Inventaire Dhātu v0.1 ».
- Convention de nommage: MAJUSCULE pour rôles/opérateurs; minuscules pour lexèmes; REL peut être spécialisé (SUR/DANS/DE) selon le domaine.
- Pour les alias anglais: maintenir un fichier EN miroir afin de satisfaire la gouvernance FR/EN tout en centralisant le contenu canonique.
