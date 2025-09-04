# Copilotage Playbook (Conseils non bloquants)

Objectif: documenter les bonnes pratiques d’architecture, de résilience et d’harmonisation sans imposer de dépendances.

Principes
- Architecture hexagonale + SOLID (domain, application, infrastructure séparés).
- Résilience: points de sauvegarde, recovery, health checks.
- CI non bloquante “advice”: fournit des recommandations (ne casse pas le build).
- Harmonisation inter‑machines via outillage dédié (ex: dotfiles harmonizer), hors de ce repo public.

Bonnes pratiques
- Séparer logique métier (pure) des adapters techniques.
- Tests: pyramide (unit > integration > e2e), seuils par couche.
- Sécurité: pas de secrets en clair; scans en CI; dépendances tenues à jour.
- Documentation: ADRs, runbooks, troubleshooting.

Intégration conseillée (optionnelle)
- Utiliser un dépôt partagé “copilotage-shared” pour règles/outils communs;
  dans ce repo public, rester sans submodule; consommer des conseils via CI.


---

## Standards d’architecture et gouvernance
- Couche Domain sans dépendances I/O; invariants, value objects, services purs.
- Application: orchestration de cas d’usage; pas de logique métier.
- Infrastructure: adapters (DB, FS, réseau, API); remplaçables.
- ADRs: 1 ADR par décision structurante (numérotée, datée, impact/conséquences).
- Revue d’architecture périodique (mensuelle) + diagrammes à jour.

## Stratégie de tests et qualité
- Pyramide: Unit (≥80%) > Intégration (10–15%) > E2E (5–10%).
- Seuils cibles: Domain 100%, Application 90%, Infrastructure 70% (min global 85%).
- Lint: ruff/flake8 (Python) ou équivalents par langage; formatteur auto.
- Static analysis: mypy/pyright (si applicable).

## Sécurité et conformité
- Zéro secret en clair (ENV/CI secrets uniquement). Revues de secrets à chaque PR.
- Dépendances: scans vulnérabilités réguliers (advice-only sur public).
- Politique M371621: séparation stricte public/privé; audit logs; chiffrement au repos/hors repo.

## CI/CD (conseils non bloquants)
- Job “advice”:
  - inventaire structure (domain/application/infrastructure/src)
  - lint rapide (si stack compatible)
  - rappels ADRs/tests/sécurité
- Passage progressif vers jobs bloquants uniquement après accord.

## Gestion des dépendances
- Stratégie de mises à jour régulières (hebdo) via bot (Renovate/Dependabot).
- Verrouillage de versions pour reproductibilité.

## Versionning et releases
- SemVer quand applicable; CHANGELOG maintenu.
- Tags signés (si possible). Artefacts reproductibles.

## Observabilité et runbooks
- Logs structurés; niveaux normalisés.
- Métriques clés (latence, erreurs, saturation) si service.
- Runbooks d’incident + procédures de rollback.

## Résilience et recovery
- Points de sauvegarde avant opérations risquées.
- Santé de session (health checks) documentée.

## Harmonisation multi‑appareils (conseils)
- Outillage externe (dotfiles harmonizer) hors repo public.
- Standards d’outillage documentés, pas imposés.

## Checklists PR (à copier dans description)
- [ ] Pas de secrets / données privées
- [ ] Tests ajoutés/mis à jour
- [ ] ADR si décision d’architecture
- [ ] CI “advice” passe (ou justifié)
- [ ] Docs/runbooks mis à jour
