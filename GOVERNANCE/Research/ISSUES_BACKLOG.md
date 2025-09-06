# Backlog d’issues — Piste Recherche

Utilisez ces gabarits si la création automatique via CLI n’est pas disponible.

---

## research: native review prompts enfant (batch 1) [owner:agent]

Objectif: Revue par locuteurs natifs des prompts enfant marqués `needs_native_review` + corrections.

Langues (volumes estimés):
- ewe: 10; iku: 10; yor: 10
- arb: 2; cmn: 2; jpn: 2; kor: 2; zul: 2
- eus: 3
- deu: 1; hau: 1; heb: 1; hin: 1; hun: 1; nld: 1; spa: 1; swa: 1; tur: 1

Tâches:
- [ ] Organiser la revue native (réseaux, ressources).
- [ ] Corriger prompts (naturel, orthographe, phénomènes).
- [ ] Re-valider metrics (coverage=1.0).

---

## research: langues signées — ASL prompts + gold + conventions v0 [owner:agent]

Objectif: Couvrir ASL (gloses) pour stress-test multimodal.

Tâches:
- [ ] 10 prompts enfant ASL (gloses + notes non-manuel si pertinent).
- [ ] Gold encodings associés.
- [ ] Conventions signe v0 (glossage, espace, pointage) dans universaux.
- [ ] Validator: mode optionnel "sign".
- [ ] Metrics: coverage=1.0; primitives comparables.

---

## research: langues signées — LSF prompts + gold [owner:agent]

Objectif: Étendre avec LSF (gloses FR).

Tâches:
- [ ] 10 prompts enfant LSF.
- [ ] Gold encodings; tests metrics.
- [ ] Ajuster conventions si besoin.

---

## research: évidentialité — Quechua prompts + gold + convention EVID (v0) [owner:agent]

Objectif: Couvrir EVID obligatoire (Quechua).

Tâches:
- [ ] 10 prompts enfant (variété standardisée).
- [ ] Gold encodings; définir EVID:direct/indirect/reported v0.
- [ ] Doc universaux: section "Convention EVID (v0)".
- [ ] Metrics coverage=1.0.

---

## research: évidentialité — Tuyuca/Tariana (stress-test) [owner:agent]

Objectif: Stress-test EVID.

Tâches:
- [ ] Choisir Tuyuca ou Tariana.
- [ ] 10 prompts; gold; metrics.
- [ ] Ajuster EVID si nécessaire.

---

## research: conventions v0.2 — EVID, CLASS, APPL, Scope(NEG/QUANT) [owner:agent]

Objectif: Étendre conventions structurelles (sans nouvelles primitives).

Tâches:
- [ ] Définir marqueurs et principes.
- [ ] Micro-cas (cmn CLASS; bantu APPL; portée NEG/QUANT; EVID cross-langues).
- [ ] Mettre à jour universaux + exemples.
- [ ] Lint basique dans validator.

---

## docs: tableau métriques + ancrages de citations [owner:agent]

Objectif: Améliorer lisibilité recherche.

Tâches:
- [ ] Tableau synthèse: langues × prompts × primitives moyennes (docs/).
- [ ] Ancrages intra-texte [ref:#] avec glossaire/citations.
- [ ] Strict build ok.

---

## ci: artefacts PDF (wkhtmltopdf ou Playwright) [owner:agent]

Objectif: Produire des PDF CI pour brouillons.

Tâches:
- [ ] Ajouter installation wkhtmltopdf OU Playwright.
- [ ] Publier artefacts PDF pour books/articles FR/EN.
