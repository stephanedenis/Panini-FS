# Guide de gestion du copilotage PaniniFS

## Vue d'ensemble

Le système de copilotage PaniniFS utilise une architecture de **configuration partagée** via submodules Git pour standardiser les pratiques de développement à travers l'écosystème.

## Architecture

```
PaniniFS/
├── copilotage/
│   ├── config.yml                    # Config locale
│   └── shared/                       # Submodule → PaniniFS-CopilotageShared
│       ├── config.yml                # Config de base
│       ├── rules/                    # Règles partagées
│       │   ├── conventional-commits.yml
│       │   ├── pull-requests.yml
│       │   └── code-standards.yml
│       └── workflows/                # Templates CI/CD
│           └── ci-standard.yml
└── modules/
    ├── module1/copilotage/           # Config héritée
    ├── module2/copilotage/           # Config héritée
    └── ...
```

## Workflow de mise à jour

### 1. Modifier la configuration partagée

```bash
cd copilotage/shared
# Éditer les fichiers rules/*.yml ou workflows/*.yml
git add .
git commit -m "feat: update coding standards"
git push origin main
```

### 2. Synchroniser vers tous les modules

```bash
cd ../..
python3 scripts/sync_copilotage.py
```

### 3. Committer les changements

```bash
git add modules/*/copilotage/
git commit -m "chore: sync copilotage config to all modules"
git push origin main
```

## Standards appliqués

### Commits
- **Format** : Conventional Commits
- **Langue** : Français accepté
- **Scopes** : `core`, `api`, `ui`, `docs`, `test`, `build`, `ci`, `deps`

### Pull Requests
- **Taille** : Max 15 fichiers, 500 lignes
- **Description** : Obligatoire (min 50 caractères)
- **Review** : 1 approbation minimum
- **Merge** : Squash obligatoire

### Code
- **Python** : Black + Ruff + MyPy
- **TypeScript/JS** : Prettier + ESLint + TSC
- **Tests** : Couverture minimum 70%
- **Documentation** : README + Changelog obligatoires

## Commandes utiles

### Vérifier l'indépendance
```bash
python3 scripts/check_copilotage_independence.py
```

### Voir l'état des submodules
```bash
git submodule status
```

### Mettre à jour tous les submodules
```bash
git submodule update --remote
```

## Dépannage

### Submodule non initialisé
```bash
git submodule update --init --recursive
```

### Conflit de merge dans submodule
```bash
cd copilotage/shared
git fetch origin
git merge origin/main
```

### Réinitialiser la configuration d'un module
```bash
rm -rf modules/MODULE_NAME/copilotage
python3 scripts/sync_copilotage.py
```
