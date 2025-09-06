# Copilotage — Plan d’architecture (squelette)

Objectif
- Décrire la structure cible pour agents, scripts et docs.

Vue d’ensemble
- agents/: orchestrateurs, critiques, tests
- scripts/: automations devops et outils opératoires
- journal/: traçabilité sessions
- knowledge/: principes et référentiels

Flux standards
1) Issue → branche → PR → merge
2) Journal par session
3) CI légère (lint/tests smoke)

Interfaces clés
- GitHub (issues/PR/actions)
- Colab (déploiements orchestrés)

Points ouverts
- Normaliser import paths des scripts
- Définir matrice de compatibilité (Python/Rust minimal)
- Intégrer lint/format non bloquant
