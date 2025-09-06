# 📁 STRATÉGIE MIGRATION MDWIKI → MKDOCS
## Transition vers documentation moderne pour PaniniFS

### 🎯 OBJECTIFS
- **Modernisation** de l'infrastructure documentaire
- **Performance** optimisée (SSG vs client-side)
- **SEO** amélioré pour la visibilité
- **Maintenance** simplifiée et sécurisée

### 📊 COMPARATIF TECHNIQUE

| Aspect | MDwiki (Actuel) | MkDocs (Cible) |
|--------|-----------------|----------------|
| **Technologie** | JavaScript client-side | Python SSG |
| **Performance** | Rendering à la demande | Pre-rendered static |
| **SEO** | Limité (SPA) | Excellent (static) |
| **Sécurité** | Dépendances jQuery | Minimal dependencies |
| **Thèmes** | Bootstrap 3 | Material Design moderne |
| **Plugins** | Limités | Écosystème riche |
| **Maintenance** | Abandonné (2014) | Activement maintenu |

### 🚀 PLAN DE MIGRATION

#### Phase 1 : Préparation
- [x] Audit du contenu MDwiki existant
- [x] Identification des assets (timbre Panini, images)
- [ ] Vérification droits d'auteur (image Wikipédia)
- [ ] Setup MkDocs avec thème Material

#### Phase 2 : Migration du contenu
- [ ] Conversion navigation.md → mkdocs.yml
- [ ] Migration pages markdown existantes
- [ ] Optimisation assets et images
- [ ] Configuration domaines multiples

#### Phase 3 : Amélioration
- [ ] Intégration recherche
- [ ] Configuration SEO avancée
- [ ] Automatisation déploiement
- [ ] Tests performance

### 📂 STRUCTURE CIBLE MKDOCS

```yaml
# mkdocs.yml
site_name: "Pāṇini File System"
site_description: "Metalinguistic information processing and storage"
site_url: "https://paninifs.com"

theme:
  name: material
  palette:
    - scheme: default
      primary: blue
      accent: blue
  features:
    - navigation.tabs
    - navigation.sections
    - search.highlight
    - content.code.copy

plugins:
  - search
  - git-revision-date-localized
  - social

nav:
  - Accueil: index.md
  - Architecture: arch/index.md
  - Domaines: domains.md
  - Monitoring: dashboard.md
```

### 🎨 GESTION ASSETS

#### Timbre Panini
- **Source actuelle** : Probablement Wikipédia
- **Action requise** : Vérification licence
- **Alternative** : Création asset original
- **Format optimisé** : WebP + PNG fallback

#### Logo et branding
- **Nom correct** : "Pāṇini File System" (avec macron)
- **Tagline** : "Metalinguistic information processing and storage"
- **Couleurs** : Palette cohérente #3498db

### 🔧 CONFIGURATION TECHNIQUE

#### Requirements.txt
```
mkdocs>=1.5.0
mkdocs-material>=9.0.0
mkdocs-git-revision-date-localized-plugin
mkdocs-social-plugin
```

#### GitHub Actions
```yaml
name: Deploy MkDocs
on:
  push:
    branches: [master]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.x
      - run: pip install -r requirements.txt
      - run: mkdocs gh-deploy --force
```

### ⚖️ DROITS D'AUTEUR - TIMBRE

#### Vérifications requises
1. **Source image Wikipédia** : Licence Creative Commons ?
2. **Usage commercial** : Autorisé pour écosystème PaniniFS ?
3. **Attribution** : Crédits requis ?

#### Alternatives si problème
1. **Recréation graphique** : Design original inspiré
2. **Achat licence** : Stock photo ou commission
3. **Symbole abstrait** : Représentation stylisée

### 📈 BÉNÉFICES ATTENDUS

#### Performance
- **Temps de chargement** : -70% (static vs SPA)
- **SEO score** : +40% (content indexable)
- **Mobile performance** : +50% (Material responsive)

#### Maintenance
- **Sécurité** : Élimination dépendances obsolètes
- **Updates** : Écosystème Python actif
- **Debugging** : Logs et erreurs clairs

#### Fonctionnalités
- **Recherche** : Index intégré performant
- **Navigation** : Tabs et sections organisées
- **Social** : Cards automatiques pour partage

### 🎯 DÉCISION RECOMMANDÉE

**✅ MIGRATION VERS MKDOCS**

**Justifications principales :**
1. **MDwiki abandonné** depuis 2014 = risque sécurité
2. **Performance critique** pour l'écosystème professionnel
3. **SEO essentiel** pour visibilité paninifs.com
4. **Alignement tech stack** Python (cohérence avec FCM/monitoring)

**Timing :** Migration en parallèle du déploiement domaines
**Effort :** 2-3 heures pour migration complète
**ROI :** Amélioration immédiate performance + maintenabilité long terme
