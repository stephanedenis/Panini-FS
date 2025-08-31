---
title: Langage humain et développement
status: draft
---

# Langage humain et développement

Parcours de l’enfant à l’adulte, jalons, théories, observations et implications pour PaniniFS.

## Jalons clés (0–6 ans)

- 0–9 mois: proto-communication (regard, pointage, babillage) → précurseurs d’AGENT, ATTENTION, DEIXIS.
- 10–18 mois: mots isolés, holophrases → encodage compact d’intentions (VERBE/OBJET implicites).
- 18–30 mois: explosion lexicale, deux mots → émergence AAO, relations spatiales basiques (SUR, DANS, À).
- 30–48 mois: morphosyntaxe, temps, négation, quantification → opérateurs de TEMPS, MODALITÉ, QUANT.
- 4–6 ans: récits simples, anaphores, théorie de l’esprit → COREFERENCE, CAUSALITÉ, INTENTION.

## Alignement Dhātu (esquisse)

- Opérateurs de base: AGENT, ACTION, PATIENT, LIEU, TEMPS, POSSESSION, NÉGATION, QUANTIFICATION, MODALITÉ.
- Règle d’introduction progressive: n’activer une primitive que lorsque l’observation enfantine typique l’exige.

## Micro-évaluations

1) Négation précoce
	- Énoncé: « pas dodo » (2 ans)
	- Dhātu: [NÉGATION] [ACTION:dormir] [AGENT:locuteur]
	- Vérifier: robustesse à l’ellipse et au télégrammatique.

2) Relation spatiale
	- Énoncé: « camion sur pont »
	- Dhātu: [OBJ:camion] [REL:SUR] [REF:pont]
	- Vérifier: transfert à « dans/sous/devant ».

3) Anaphore simple
	- Énoncé: « Marie prend le livre. Elle lit. »
	- Dhātu: [AGENT:Marie][ACTION:prendre][OBJ:livre] … [COREF:AGENT précédent][ACTION:lire]
	- Vérifier: résolution de COREF minimale.

## Métriques

- Taux d’alignement jalon→primitive (pour chaque tranche d’âge, quelles primitives sont nécessaires/suffisantes?).
- Taux de succès de décodage des productions télégraphiques en propositions complètes.
- Réduction de complexité: nombre de primitives actives vs. expressivité atteinte.
