---
title: Compression sémantique (computationnelle)
status: draft
---

# Compression sémantique (computationnelle)

Principes, cas d’usage et métriques pour évaluer la compression sémantique via Dhātu.

## Objectif

Minimiser la perte de sens à débit (bitrate) fixé en représentant connaissances et messages sous forme de primitives Dhātu compactes.

## Métriques (v0)

- Couverture conceptuelle: % de concepts/fragments encodés sans primitive additionnelle.
- Taux de reconstruction: similarité sémantique (humains/LLM) entre original et paraphrase décodée.
- Taux d’ambiguïté: décodages plausibles par encodage; plus bas est mieux.
- Taille moyenne d’encodage: primitives par proposition; budget cible à fixer par use case.
- Coût d’apprentissage: exemples nécessaires pour apprendre un mapping stable (few-shot) sur un domaine.

## Protocole d’évaluation minimal

1) Corpus jouet bilingue (FR/EN) de 100 phrases couvrant AAO, relations spatiales, temps, négation, quantification.
2) Encodage manuel de référence (gold) + tentative d’encodage automatique (règles/LLM guidé).
3) Décodage vers paraphrases FR/EN et scoring de similarité/ambiguïté.
4) Calcul des métriques ci-dessus; rapporter moyenne, médiane, variabilité.

## Micro-cas

- Instruction simple: « Ferme la porte » → [ACTION:fermer][OBJ:porte][AGENT:destinataire]
- Question oui/non: « As-tu faim ? » → [INTERROGATIVE][ÉTAT:faim][AGENT:destinataire]
- Contre-exemple ambigu: « Je vois l’homme avec le télescope » (attachement prépositionnel)

## Pistes d’implémentation

- Définir un petit inventaire Dhātu versionné (v0.1) dans un fichier YAML pour itérer.
- Écrire un validateur d’encodage/décodage (tests unitaires) avec jeux de phrases jouets.
- Incrémenter la couverture par domaines (objets domestiques, mouvements, interactions sociales de base).
