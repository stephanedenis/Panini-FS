# 🔐 SETUP SECRETS GOOGLE COLAB

# Pour utiliser les secrets dans Colab, ajoutez ces cellules:

## 1. Configuration secrets manuels (développement)
```python
import os
from google.colab import userdata

# Optionnel: Récupération depuis Colab Secrets
try:
    os.environ['GOOGLE_DRIVE_CREDENTIALS'] = userdata.get('GOOGLE_DRIVE_CREDENTIALS')
    os.environ['ARXIV_API_KEY'] = userdata.get('ARXIV_API_KEY')
    print("✅ Secrets Colab chargés")
except:
    print("⚠️ Secrets Colab non configurés - mode dégradé activé")
```

## 2. Mode automatique depuis GitHub
```python
# Les secrets sont automatiquement disponibles si lancé via GitHub Actions
# Aucune configuration manuelle requise
```

## 3. Test configuration
```python
from Copilotage.scripts.headless_env_loader import HeadlessEnvLoader

loader = HeadlessEnvLoader()
print("🔐 État secrets:", {
    'headless': loader.is_headless_mode(),
    'github': bool(loader.get_github_token()),
    'gdrive': bool(loader.get_google_drive_credentials())
})
```
