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

## Baby sign → Dhātu (micro-cas)

- « encore » (geste de la main) → [QUANT:>0] [ACTION:répéter]  
	Variante orientée objet: [QUANT:>0] [ACTION:donner] [OBJ:aliment/jouet]
- « lait » (poing qui se serre) → [ACTION:boire] [OBJ:lait] [AGENT:destinataire]
- « fini » / « tout fait » → [NEGATION] [ACTION:continuer]  
	Variante d’état: [STATE:terminé]

Notes:
- On privilégie des combinaisons de primitives existantes (NEGATION, QUANT, ACTION, STATE) pour éviter d’introduire de nouveaux opérateurs.
- Les lexèmes (répéter, donner, lait, continuer, terminé) restent du vocabulaire; l’inventaire Dhātu n’impose pas un lexique fermé.

## Références

- MacWhinney, B. (2000–). CHILDES — Child Language Data Exchange System (TalkBank). https://childes.talkbank.org/
- Goldin-Meadow, S. (2003). The Resilience of Language. Psychology Press. ISBN: 978-1-84872-004-1
- Universal Dependencies (UD). https://universaldependencies.org/
- Page « Références de recherche »: ../research/references.md
