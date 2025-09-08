# Copilotage

Ce dossier regroupe la configuration et les assets de copilotage pour l'écosystème PaniniFS.

## Structure

- `config.yml`: Configuration locale du repository principal
- `shared/`: Sous-module Git pointant vers `PaniniFS-CopilotageShared` (configuration partagée)

## Configuration partagée

Le submodule `shared/` contient :
- **Règles** : Conventional commits, standards de code, pull requests
- **Workflows** : Templates CI/CD réutilisables
- **Templates** : Issues et PR templates GitHub

## Synchronisation avec les modules

Utilisez le script `scripts/sync_copilotage.py` pour synchroniser la configuration partagée vers tous les modules :

```bash
python3 scripts/sync_copilotage.py
```

Cette commande :
1. Met à jour la configuration copilotage dans chaque module actif
2. Crée les fichiers `copilotage/config.yml` et `copilotage/README.md`
3. Configure l'héritage depuis la configuration partagée

## Mise à jour de la configuration partagée

1. **Modifier les règles** : Éditer les fichiers dans `shared/rules/`
2. **Modifier les workflows** : Éditer les fichiers dans `shared/workflows/`
3. **Committer dans le submodule** :
   ```bash
   cd copilotage/shared
   git add .
   git commit -m "feat: update copilotage rules"
   git push origin main
   ```
4. **Synchroniser vers les modules** :
   ```bash
   cd ../..
   python3 scripts/sync_copilotage.py
   ```

## Standards appliqués

- **Commits** : Conventional Commits en français
- **Pull Requests** : Maximum 15 fichiers, description obligatoire
- **Code** : Formatage automatique (Black, Prettier)
- **Tests** : Couverture minimum 70%
- **Review** : Au moins 1 approbation requise

## Vérification d'indépendance

Le script `scripts/check_copilotage_independence.py` vérifie que le code de production ne dépend pas de la configuration copilotage (séparation des préoccupations).

```bash
python3 scripts/check_copilotage_independence.py
```
