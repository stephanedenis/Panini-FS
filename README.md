# 🎌 PaniniFS - Écosystème de Compression Sémantique Universelle

[![Build Docs](https://github.com/stephanedenis/PaniniFS/actions/workflows/docs-build.yml/badge.svg)](https://github.com/stephanedenis/PaniniFS/actions/workflows/docs-build.yml)
[![Modules Index](https://github.com/stephanedenis/PaniniFS/actions/workflows/update-modules-index.yml/badge.svg)](https://github.com/stephanedenis/PaniniFS/actions/workflows/update-modules-index.yml)

> Contribution et workflow: voir `Copilotage/CONTRIBUTING.md` et `Copilotage/COPILOTAGE_WORKFLOW.md`.

**PaniniFS** est un écosystème révolutionnaire de systèmes de fichiers basé sur l'analyse linguistique et la compression sémantique des contenus. Inspiré des travaux de Pāṇini et de la découverte des **dhātu informationnels** - les atomes conceptuels universels de l'information.

## 🏗️ Architecture d'Entreprise Moderne

L'écosystème PaniniFS est organisé en modules spécialisés pour une architecture scalable et maintenable :

```
🏛️ GOVERNANCE/     - Gouvernance, audits et processus
📚 RESEARCH/       - Publications, découvertes et méthodologie  
🔧 CORE/           - Cœur technique PaniniFS et analyseur sémantique
🌐 ECOSYSTEM/      - Sous-projets et intégrations externes
🚀 OPERATIONS/     - DevOps, déploiement et infrastructure
📖 DOCUMENTATION/  - Documentation unifiée et sites publics
🧪 SANDBOX/        - Expérimentations et prototypes
```

### � **CORE/** - Cœur Technique
- **`panini-fs/`** : Implémentation principale en Rust
- **`semantic-analyzer/`** : Analyseur des 7 dhātu informationnels
- **`protocols/`** : Content addressing sémantique
- **`validation/`** : Outils de test et conformité

### 🌐 **ECOSYSTEM/** - Modules Spécialisés
- **`semantic-core/`** : Core de traitement sémantique
- **`publication-engine/`** : Générateur de publications
- **`execution-orchestrator/`** : Orchestrateur unique avec drivers (local/colab/cloud) et catalogue `missions/`
- **`integrations/`** : GitHub, Firebase, Azure...

### 📚 **RESEARCH/** - Découvertes Scientifiques
- **`publications/`** : Livres Leanpub et articles Medium
- **`discoveries/`** : Les 7 dhātu universels, validation baby sign
- **`datasets/`** : Trinity dataset (Gutenberg, Wikipedia, Archive)
- **`methodology/`** : Protocoles et reproductibilité

## 🚀 Démarrage Rapide

### Installation
```bash
git clone https://github.com/stephanedenis/PaniniFS.git
cd PaniniFS
```

### Build du Core
```bash
cd CORE/panini-fs
cargo build
cargo test
```

### Documentation
```bash
cd DOCUMENTATION/public-site
# Voir les guides dans developer-docs/
```

## 🔬 Découvertes Clés

### 🧬 **Les 7 Dhātu Informationnels**
Les atomes conceptuels universels présents dans toute information :

| Dhātu | Concept | Exemples |
|-------|---------|----------|
| **COMM** | Communiquer | print, API, "parler" |
| **ITER** | Répéter | boucles, "encore" |
| **TRANS** | Transformer | filter, "changer" |
| **DECIDE** | Décider | if/else, "choisir" |
| **LOCATE** | Localiser | search, "où" |
| **GROUP** | Rassembler | arrays, "même" |
| **SEQ** | Séquencer | order, "premier" |

### 🌍 **Content Addressing Sémantique**
Révolution : déduplication basée sur le **sens**, pas la syntaxe.

```
"Hello world" → [COMM] → Hash sémantique
"Bonjour monde" → [COMM] → Même hash !
```

### 👶 **Validation Baby Sign Language**
Les dhātu correspondent aux gestes primitifs des bébés, confirmant leur universalité cognitive.

## 📚 Publications

### 📖 **Livres Complets** (Leanpub)
- **Français** : [L'Odyssée de la Compression Sémantique](https://leanpub.com/paninifs-fr)
- **English** : [The Odyssey of Semantic Compression](https://leanpub.com/paninifs-en)

### 📰 **Articles** (Medium)
- **Français** : [Quand des Vacances Sans Code Révèlent un Rêve de 35 Ans](https://medium.com/@neuronspikes/quand-des-vacances-sans-code-r%C3%A9v%C3%A8lent-un-r%C3%AAve-de-35-ans-29246234239c)
- **English** : [When Code-Free Vacations Reveal a 35-Year Dream](https://medium.com/@neuronspikes/when-code-free-vacations-reveal-a-35-year-dream-e17e0f1823da)

## 🤝 Contribution

### 🎯 **Types de Contributions**
1. **🔬 Recherche** : Validations académiques, expérimentations
2. **💻 Code** : Core technique, optimisations, nouveaux modules  
3. **📖 Documentation** : Guides, tutoriels, API docs
4. **🧪 Expérimentations** : Prototypes dans SANDBOX/

### 🔄 **Workflow**
1. Fork le repository
2. Créer une branche pour votre contribution
3. Développer dans le module approprié
4. Tests et validation
5. Pull Request avec description détaillée

Voir [DOCUMENTATION/developer-docs/contributing/](DOCUMENTATION/developer-docs/contributing/) pour les détails.

## 🌟 Écosystème

### 🎓 **Académiques**
Linguistes, cognitivistes, informaticiens - vos expertises valident et étendent les concepts.

### 🔧 **Développeurs**  
Makers, inventeurs - votre pragmatisme transforme les idées en réalité.

### 🌍 **Citoyens du Monde**
Toute personne qui croit que l'information doit être librement accessible et que la collaboration transcende les frontières.

## 📄 Licence & Éthique

- **Licence** : MIT (voir [GOVERNANCE/legal/LICENSE](GOVERNANCE/legal/LICENSE))
- **Éthique** : Respecte la [Déclaration de Montréal](GOVERNANCE/legal/ethics/) pour un développement responsable de l'IA
- **Philosophie** : "La connaissance appartient à l'humanité"

## 📊 Métriques de Réussite

- **Compression sémantique** : +58% vs compression classique
- **Universalité** : 100% des fichiers contiennent les 7 dhātu
- **Langages supportés** : Python, JavaScript, Bash, Markdown
- **Langues validées** : Français, Anglais (+ Baby Sign Language!)

---

## 🏛️ **Architecture Restructurée**

**Version 2.0.0** - 21 août 2025  
*Transition de 138 fichiers racine → Architecture d'entreprise moderne*

### 🎯 **Gains**

### 🔄 **Migration**
Backup complet disponible, tous les assets préservés et relocalisés intelligemment.


Note submodules: les répertoires déclarés dans `.gitmodules` (modules/*, copilotage/shared, RESEARCH, etc.) sont édités indépendamment dans leurs dépôts respectifs. Voir `CONTRIBUTING.md` → section "Submodules — principe d’édition indépendante" et le template d’issue « Submodule change request ».

*© 2025 - Recherche ouverte sous Creative Commons*  
*"Quand des vacances sans code révèlent un rêve de 35 ans"*

**Stéphane Denis** - Développeur depuis 30 ans, ex-professeur, patenteux dans l'âme.  
Passionné par les intersections entre linguistique, cognition et informatique.
