# Guide multi-repo PaniniFS

Objectif: rester en multi-repo pour séparer recherche sémantique, développement FS et documentation, tout en harmonisant les workflows et l’expérience VS Code.

## Sous-modules et cohérence
- Initialiser/MAJ: `git submodule sync --recursive && git submodule update --init --recursive`
- Auditer: `scripts/devops/audit_submodules.sh`
- Branches par défaut: aligner sur `main` et mettre à jour `.gitmodules` si nécessaire.

## Workspaces VS Code dédiés
- Semantic research: `.vscode/semantic-research.code-workspace`
- Filesystem dev: `.vscode/filesystem-dev.code-workspace`
- Docs site: `.vscode/docs-site.code-workspace`

## Coordination Copilotage
- Général: ce repo (PaniniFS) reste la “tour de contrôle” (docs, gouvernance, pages).
- Spécialisé: chaque module suit ses CI/workflows propres; synchronisation via submodules et publications.
- Diagnostics/déploiement: workflows GitHub Actions ajoutés pour Pages et Docs.

## Bonnes pratiques
- Commits atomiques par module; PR par repo/module.
- Versionner les consommations inter-modules (tags/releases).
- Garder les submodules légers (docs dans module, index agrégé ici via MkDocs).
