---
title: Hypothèses et alternatives (Dhātu)
status: draft
---

# Hypothèses et alternatives pour des universaux robustes

Objectif: avancer vite par hypothèses opérables tout en gardant des pistes alternatives pour couvrir la diversité typologique (généralisation).

## Hypothèses de travail

- Rôles sémantiques minimaux (AGENT, PATIENT/THÈME, RÉCIPIENT/BÉNÉF) suffisent à reconstruire la plupart des structures d’argumentation.
- Opérateurs universels: NÉGATION, MODALITÉ (possibilité/obligation), ÉVIDENCE (source), QUANTIFICATION, TEMPS/ASPECT, COMPARAISON, EXISTENCE/LOCALISATION.
- Relations spatiales de base (DANS/SUR/SOUS/PROCHE/VERS/DEPUIS/À‑TRAVERS) sont suffisantes; spécialisations par domaine (topologie fine) peuvent être dérivées.
- La morphologie (valence, voix, incorporation) n’introduit pas de nouvelle primitive sémantique, seulement des combinaisons ou omissions.

## Alternatives envisagées

- Rôles vs. Dépendances: remplacer/compléter les rôles par un petit set de relations de dépendances sémantiques (head‑dependent) pour gérer l’ordre libre et l’ergativité.
- Évidence: modéliser l’évidentialité non comme opérateur mais comme méta‑attribut de l’acte assertif (portée pragmatique) — utile pour langues à marquage obligatoire.
- Quantification: primitives de classe (TOTAL, PARTITIF, DISTRIBUTIF) vs. opérateurs numériques purs — choisir selon stabilité inter‑langues.
- Comparaison: traiter PLUS/MOINS comme prédicats de degré vs. opérateurs sur échelles (sélection d’échelle contextuelle).
- Existence/Localisation: fusionner « IL‑Y‑A » et « ÊTRE‑À » via un opérateur de mise‑en‑scène (SCÈNE) — pertinent pour langues sans copule.

## Épreuves ciblées (stress‑tests)

- Ergativité/split: marquage d’arguments (Basque, Hindi‑Urdu) — valider neutralité des rôles.
- Sérialisation verbale (Ewe, Yoruba): séquences d’événements sans subordination.
- Polysynthèse (Inuktitut, Mohawk): incorporation nominale sans nouvelle primitive.
- Classificateurs (Mandarin): compatibilité avec QUANT et types.
- Évidentialité (Quechua, Tariana): portée/assertion vs. proposition.
- Langues signées (ASL, NSL): simultanéité/spatialisation — mapping vers primitives séquentielles.

## Données enfants d’abord

- Priorité aux textes dirigés vers l’enfant (CHILDES, Global/African Storybooks) pour ancrer les phénomènes minimaux.
- Voir `experiments/dhatu/typological_sample.json` et prompts `experiments/dhatu/prompts_child/`.

## Progrès et validation

- Utiliser `experiments/dhatu/validator.py` pour lister l’échantillon (`--list-sample`), les prompts (`--list-child fr|en`) et agrégats de phénomènes (`--phenomena`).
- Maintenir la parité FR/EN côté docs; référencer « Références de recherche » pour sources typologiques.
