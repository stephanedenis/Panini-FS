# Roadmap Recherche — PaniniFS (brouillon)

Objectif: cadrer les prochains jalons de la piste Recherche (prompts enfant multilingues, conventions, évaluation) et pointer vers les tickets de suivi. Cette roadmap est volontairement courte et itérative; elle sera réévaluée à chaque jalon.

## Contexte
- Corpus prompts enfant multilingues avec encodages-or en “primitives” + conventions SVC vs SEQ; INCORP déjà en v0.
- Build strict MkDocs/CI; pipeline publications (Leanpub/HTML/PDF) opérationnel.
- Backlog: revues natives, langues signées, évidentialité, extension de conventions, tableaux de métriques, PDF CI.

## Jalon M1 — Revue native (Batch 1)
But: corriger naturel/orthographe/phénomènes pour prompts marqués `needs_native_review`.
- Cible haute priorité: ewe (10), iku (10), yor (10)
- Autres: arb, cmn, jpn, kor, zul (≈2 chacun); eus (3); deu/hau/heb/hin/hun/nld/spa/swa/tur (≈1 chacun)
- Critères de sortie: coverage=1.0 inchangé; remarques intégrées; exemples mis à jour.
- Suivi: “research: native review prompts enfant (batch 1) [owner:agent]”.

## Jalon M2 — Langues signées (ASL, LSF)
But: stress-test multimodal (gloses; éventuels marqueurs non-manuels).
- ASL: 10 prompts + gold + conventions signe v0 (glossage, espace, pointage); mode validator "sign".
- LSF: 10 prompts + gold; ajustements conventions.
- Critères de sortie: coverage=1.0; primitives comparables aux langues orales; doc universaux mise à jour.
- Suivi: “research: langues signées — ASL …”, “research: langues signées — LSF …”.

## Jalon M3 — Évidentialité (Quechua + stress-test)
But: couvrir EVID obligatoire et tester robustesse.
- Quechua: 10 prompts enfant; définir EVID:direct/indirect/reported (v0) + doc universaux.
- Stress-test: Tuyuca ou Tariana (10 prompts) selon ressources disponibles.
- Critères de sortie: coverage=1.0; cohérence interlangues; notes de limites.
- Suivi: “research: évidentialité — Quechua …”, “research: évidentialité — Tuyuca/Tariana …”.

## Jalon M4 — Conventions v0.2
But: étendre sans nouvelles primitives (structurel uniquement).
- EVID, CLASS (classificateurs), APPL (applicatifs/valence), portée Scope(NEG/QUANT)
- Micro-cas: cmn CLASS; bantu APPL; portée NEG/QUANT; EVID cross-langues.
- Lint basique dans validator (détections d’incohérences simples).
- Suivi: “research: conventions v0.2 — EVID, CLASS, APPL, Scope(NEG/QUANT) …”.

## Jalon M5 — Documentation (métriques + citations)
But: améliorer lisibilité et traçabilité publique.
- Tableau de synthèse: langues × prompts × primitives moyennes (docs/), liens vers encodages-or.
- Ancrages intra-texte [ref:#] + glossaire/citations.
- Build strict sans avertissements.
- Suivi: “docs: tableau métriques + ancrages de citations …”.

## Jalon M6 — CI artefacts PDF
But: générer et publier PDF dans les artefacts CI (brouillons FR/EN livres/articles).
- Installer wkhtmltopdf ou Playwright dans CI; intégrer dans workflow publications.
- Suivi: “ci: artefacts PDF (wkhtmltopdf ou Playwright) …”.

## Risques & dépendances
- Disponibilité de relecteurs natifs (mitigation: réseaux académiques, STORYBOOKS/CHILDES, pairs).
- Données enfant pour ASL/LSF/Tuyuca/Tariana limitées (mitigation: prompts synthétiques guidés + validation expert·e).
- Complexité conventions vs simplicité primitives (principe: pas de nouvelles primitives sans preuve forte; préférer marqueurs structurels).

## Mesures de succès
- Coverage=1.0 sur l’ensemble des langues/jeux; variance raisonnable des primitives moyennes.
- Conventions documentées et testées par micro-cas; validator couvre les incohérences communes.
- Artefacts de publication (HTML/PDF) produits automatiquement; page “Publications” à jour.

## Suivi
- Voir les issues GitHub portant les titres listés ci-dessus (préfixes “research:”, “docs:”, “ci:”).
- Mise à jour de cette roadmap à la fin de chaque jalon (ajouter date, delta et blocages le cas échéant).