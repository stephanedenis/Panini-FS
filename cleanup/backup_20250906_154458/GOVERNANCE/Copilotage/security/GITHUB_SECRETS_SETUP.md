# 🔐 GITHUB SECRETS CONFIGURATION POUR AUTONOMIE HEADLESS

## Secrets requis dans GitHub Repository Settings > Secrets and variables > Actions

### 1. GITHUB_TOKEN (automatique)
- ✅ Fourni automatiquement par GitHub Actions
- Permissions: Read/Write repository, Issues, Pull requests

### 2. GOOGLE_DRIVE_CREDENTIALS
```json
{
  "web": {
    "client_id": "YOUR_GOOGLE_CLIENT_ID",
    "project_id": "paninifs-autonomous", 
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_secret": "YOUR_GOOGLE_CLIENT_SECRET",
    "redirect_uris": ["http://localhost:8080/callback"]
  }
}
```

### 3. ARXIV_API_KEY (optionnel)
- Clé API ArXiv pour recherche théorique avancée
- Obtenir sur: https://arxiv.org/help/api

### 4. SEMANTIC_SCHOLAR_API_KEY (optionnel) 
- Clé API Semantic Scholar pour recherche académique
- Obtenir sur: https://www.semanticscholar.org/product/api

## Instructions Configuration Headless

### 1. Via GitHub CLI (si disponible)
```bash
# GitHub token (automatique dans Actions)
gh secret set GOOGLE_DRIVE_CREDENTIALS < gdrive_credentials/credentials.json

# APIs optionnelles
gh secret set ARXIV_API_KEY --body "YOUR_ARXIV_KEY"
gh secret set SEMANTIC_SCHOLAR_API_KEY --body "YOUR_SEMANTIC_KEY"
```

### 2. Via Interface Web GitHub
1. Aller sur: https://github.com/stephanedenis/PaniniFS/settings/secrets/actions
2. Cliquer "New repository secret"
3. Ajouter chaque secret individuellement

### 3. Pour Tests Locaux (Colab)
- Les secrets seront accessibles via variables d'environnement
- Fallback sur mode dégradé si secrets manquants

## Stratégie Mode Dégradé Autonome

Si secrets manquants, le système fonctionne quand même :
- ✅ GitHub monitoring : Token automatique GitHub Actions
- ✅ Recherche théorique : APIs publiques sans clé  
- ✅ Critique adverse : Analyse locale sans APIs
- ⚠️ Google Drive : Mode local uniquement
- ✅ Publications : GitHub repository comme stockage

## Sécurité Headless

- ❌ Aucun secret dans le code source
- ✅ Secrets chiffrés dans GitHub
- ✅ Accès via variables d'environnement uniquement
- ✅ Logs sans exposition de secrets
- ✅ Rotation automatique possible
