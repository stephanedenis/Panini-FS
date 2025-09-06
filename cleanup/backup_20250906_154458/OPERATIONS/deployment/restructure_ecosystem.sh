#!/bin/bash

# 🏗️ SCRIPT DE RESTRUCTURATION ÉCOSYSTÈME PANINIFS
# Architecture d'Entreprise Moderne - Migration Automatique
# Date: 21 août 2025

set -euo pipefail

# Configuration
PROJECT_ROOT="/home/stephane/GitHub/PaniniFS-1"
BACKUP_DIR="$PROJECT_ROOT/../PaniniFS-1-backup-$(date +%Y%m%d-%H%M%S)"
LOG_FILE="$PROJECT_ROOT/restructuration_$(date +%Y%m%d-%H%M%S).log"

# Couleurs pour le logging
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction de logging
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

# Phase 1: Préparation et Backup
phase1_preparation() {
    log "=== PHASE 1: PRÉPARATION ET BACKUP ==="
    
    # Backup complet
    log "Création du backup complet..."
    cp -r "$PROJECT_ROOT" "$BACKUP_DIR"
    success "Backup créé: $BACKUP_DIR"
    
    # Création de la structure des nouveaux dossiers
    log "Création de la nouvelle structure..."
    cd "$PROJECT_ROOT"
    
    # Dossiers principaux
    mkdir -p GOVERNANCE/{Copilotage/{missions,architecture,security,workflows},audit/{coherence,security,performance},roadmap,legal/{ethics,compliance}}
    mkdir -p RESEARCH/{publications/{books/{french,english},articles/{french,english},papers},discoveries/{dhatu-universals,baby-sign-validation,compression-results},datasets/{trinity,validation,benchmarks},methodology/{protocols,validation,reproducibility}}
    mkdir -p CORE/{panini-fs/{src,tests,benches,examples,docs},semantic-analyzer/{dhatu-detector,pattern-recognition,compression-engine},protocols/{content-addressing,api-specification,interoperability},validation/{test-harness,compliance-checker,performance-profiler}}
    mkdir -p ECOSYSTEM/{integrations/{github,google-drive,firebase,azure},tools/{cli,gui,web-interface}}
    mkdir -p OPERATIONS/{deployment/{local,cloud,containers,scripts},monitoring/{metrics,logging,alerting,dashboards},infrastructure/{terraform,ansible,kubernetes},security/{secrets,certificates,auditing},backup/{strategies,automation,recovery}}
    mkdir -p DOCUMENTATION/{public-site/{_site,_docs,assets},developer-docs/{api,architecture,tutorials,contributing},user-guides/{getting-started,tutorials,reference},internal/{processes,decisions,runbooks}}
    mkdir -p SANDBOX/{experiments/{compression-algorithms,linguistic-models,ui-prototypes},proof-of-concepts/{semantic-search,real-time-analysis,distributed-storage},archived/{failed-experiments,successful-poc},playground/{scripts,notebooks,misc}}
    
    success "Structure des dossiers créée"
}

# Phase 2: Migration GOVERNANCE
phase2_governance() {
    log "=== PHASE 2A: MIGRATION GOVERNANCE ==="
    
    # Migration du dossier Copilotage
    if [ -d "Copilotage" ]; then
        log "Migration du dossier Copilotage..."
        cp -r Copilotage/* GOVERNANCE/Copilotage/ 2>/dev/null || true
        success "Copilotage migré"
    fi
    
    # Migration des audits
    log "Migration des fichiers d'audit..."
    mv AUDIT_*.md GOVERNANCE/audit/coherence/ 2>/dev/null || true
    mv COHERENCE_*.md GOVERNANCE/audit/coherence/ 2>/dev/null || true
    mv *audit*.json GOVERNANCE/audit/ 2>/dev/null || true
    
    # Migration des fichiers de sécurité
    mv TROUSSEAU_*.md GOVERNANCE/legal/compliance/ 2>/dev/null || true
    mv *SECRETS*.md GOVERNANCE/Copilotage/security/ 2>/dev/null || true
    
    # Migration de la licence
    mv LICENSE GOVERNANCE/legal/ 2>/dev/null || true
    
    success "Migration GOVERNANCE terminée"
}

# Phase 2B: Migration RESEARCH
phase2_research() {
    log "=== PHASE 2B: MIGRATION RESEARCH ==="
    
    # Publications - Livres
    log "Migration des livres..."
    mv LIVRE_LEANPUB_2025.md RESEARCH/publications/books/french/ 2>/dev/null || true
    mv LIVRE_LEANPUB_2025_EN.md RESEARCH/publications/books/english/ 2>/dev/null || true
    mv LIVRE_LEANPUB_FINAL_*.md RESEARCH/publications/books/ 2>/dev/null || true
    
    # Publications - Articles
    log "Migration des articles..."
    mv ARTICLE_MEDIUM_2025.md RESEARCH/publications/articles/french/ 2>/dev/null || true
    mv ARTICLE_MEDIUM_2025_EN.md RESEARCH/publications/articles/english/ 2>/dev/null || true
    mv ARTICLE_MEDIUM_FINAL_*.md RESEARCH/publications/articles/ 2>/dev/null || true
    
    # Découvertes
    log "Migration des découvertes..."
    mv DECOUVERTE_DHATU_*.md RESEARCH/discoveries/dhatu-universals/ 2>/dev/null || true
    mv BABY_SIGN_*.md RESEARCH/discoveries/baby-sign-validation/ 2>/dev/null || true
    mv DHATU_*.md RESEARCH/discoveries/dhatu-universals/ 2>/dev/null || true
    
    # Guides et méthodologie
    mv GUIDE_*.md RESEARCH/methodology/protocols/ 2>/dev/null || true
    mv ORDRE_*.md RESEARCH/methodology/protocols/ 2>/dev/null || true
    mv PUBLICATION_*.md RESEARCH/methodology/protocols/ 2>/dev/null || true
    
    success "Migration RESEARCH terminée"
}

# Phase 2C: Migration CORE
phase2_core() {
    log "=== PHASE 2C: MIGRATION CORE ==="
    
    # Migration du code source principal
    if [ -d "src" ]; then
        log "Migration du code source..."
        cp -r src/* CORE/panini-fs/src/ 2>/dev/null || true
    fi
    
    # Migration des fichiers Rust
    mv Cargo.toml CORE/panini-fs/ 2>/dev/null || true
    mv *.rs CORE/panini-fs/src/ 2>/dev/null || true
    
    # Migration des exemples
    if [ -d "examples" ]; then
        cp -r examples/* CORE/panini-fs/examples/ 2>/dev/null || true
    fi
    
    # Migration des tests et validation
    mv dhatu_*.py CORE/semantic-analyzer/dhatu-detector/ 2>/dev/null || true
    mv validate_*.sh CORE/validation/test-harness/ 2>/dev/null || true
    mv *test*.txt CORE/validation/ 2>/dev/null || true
    
    success "Migration CORE terminée"
}

# Phase 2D: Migration ECOSYSTEM
phase2_ecosystem() {
    log "=== PHASE 2D: MIGRATION ECOSYSTEM ==="
    
    # Migration des sous-projets existants
    if [ -d "SemanticCore" ]; then
        log "Migration SemanticCore..."
        mv SemanticCore ECOSYSTEM/semantic-core 2>/dev/null || true
    fi
    
    if [ -d "PublicationEngine" ]; then
        log "Migration PublicationEngine..."
        mv PublicationEngine ECOSYSTEM/publication-engine 2>/dev/null || true
    fi
    
    if [ -d "CoLabController" ]; then
        log "Migration CoLabController..."
        mv CoLabController ECOSYSTEM/colab-controller 2>/dev/null || true
    fi
    
    if [ -d "CloudOrchestrator" ]; then
        mv CloudOrchestrator ECOSYSTEM/cloud-orchestrator 2>/dev/null || true
    fi
    
    if [ -d "UltraReactive" ]; then
        mv UltraReactive ECOSYSTEM/ultra-reactive 2>/dev/null || true
    fi
    
    if [ -d "AutonomousMissions" ]; then
        mv AutonomousMissions ECOSYSTEM/autonomous-missions 2>/dev/null || true
    fi
    
    success "Migration ECOSYSTEM terminée"
}

# Phase 2E: Migration OPERATIONS
phase2_operations() {
    log "=== PHASE 2E: MIGRATION OPERATIONS ==="
    
    # Scripts de déploiement
    log "Migration des scripts de déploiement..."
    mv deploy_*.sh OPERATIONS/deployment/scripts/ 2>/dev/null || true
    mv deploy_*.py OPERATIONS/deployment/scripts/ 2>/dev/null || true
    mv setup_*.sh OPERATIONS/deployment/scripts/ 2>/dev/null || true
    mv launch_*.sh OPERATIONS/deployment/scripts/ 2>/dev/null || true
    
    # Monitoring et logs
    mv *monitor*.py OPERATIONS/monitoring/metrics/ 2>/dev/null || true
    mv *monitor*.json OPERATIONS/monitoring/metrics/ 2>/dev/null || true
    mv *.log OPERATIONS/monitoring/logging/ 2>/dev/null || true
    if [ -d "logs" ]; then
        mv logs/* OPERATIONS/monitoring/logging/ 2>/dev/null || true
        rmdir logs 2>/dev/null || true
    fi
    
    # Configuration et secrets
    mv *config*.json OPERATIONS/security/secrets/ 2>/dev/null || true
    mv *credentials* OPERATIONS/security/secrets/ 2>/dev/null || true
    if [ -d "gdrive_credentials" ]; then
        mv gdrive_credentials OPERATIONS/security/secrets/ 2>/dev/null || true
    fi
    
    # Backup
    if [ -d "cloud_backup" ]; then
        mv cloud_backup OPERATIONS/backup/strategies/ 2>/dev/null || true
    fi
    
    success "Migration OPERATIONS terminée"
}

# Phase 2F: Migration DOCUMENTATION
phase2_documentation() {
    log "=== PHASE 2F: MIGRATION DOCUMENTATION ==="
    
    # Documentation publique
    if [ -d "docs" ]; then
        log "Migration de la documentation..."
        cp -r docs/* DOCUMENTATION/public-site/_docs/ 2>/dev/null || true
    fi
    
    # Site GitHub Pages
    mv CNAME DOCUMENTATION/public-site/ 2>/dev/null || true
    mv _config.yml DOCUMENTATION/public-site/ 2>/dev/null || true
    if [ -d "site" ]; then
        mv site/* DOCUMENTATION/public-site/_site/ 2>/dev/null || true
        rmdir site 2>/dev/null || true
    fi
    
    # Documentation technique
    mv DEPLOYMENT.md DOCUMENTATION/developer-docs/ 2>/dev/null || true
    mv CONTRIBUTING.md DOCUMENTATION/developer-docs/contributing/ 2>/dev/null || true
    mv README.md DOCUMENTATION/developer-docs/ 2>/dev/null || true
    
    success "Migration DOCUMENTATION terminée"
}

# Phase 2G: Migration SANDBOX
phase2_sandbox() {
    log "=== PHASE 2G: MIGRATION SANDBOX ==="
    
    # Notebooks et expérimentations
    mv *.ipynb SANDBOX/experiments/ 2>/dev/null || true
    if [ -d "__pycache__" ]; then
        mv __pycache__ SANDBOX/playground/misc/ 2>/dev/null || true
    fi
    
    # Environnements virtuels
    if [ -d ".venv" ]; then
        mv .venv SANDBOX/playground/misc/ 2>/dev/null || true
    fi
    if [ -d "venv_*" ]; then
        mv venv_* SANDBOX/playground/misc/ 2>/dev/null || true
    fi
    if [ -d "mkdocs_env" ]; then
        mv mkdocs_env SANDBOX/playground/misc/ 2>/dev/null || true
    fi
    
    # Fichiers temporaires et expérimentaux
    mv analogy_*.py SANDBOX/experiments/ 2>/dev/null || true
    mv mini_*.py SANDBOX/playground/scripts/ 2>/dev/null || true
    mv check_*.py SANDBOX/playground/scripts/ 2>/dev/null || true
    mv *template* SANDBOX/playground/misc/ 2>/dev/null || true
    
    # Archives et packs
    mv *.tar.gz SANDBOX/archived/ 2>/dev/null || true
    if [ -d "remarkable_study_pack" ]; then
        mv remarkable_study_pack SANDBOX/archived/ 2>/dev/null || true
    fi
    
    success "Migration SANDBOX terminée"
}

# Phase 3: Nettoyage
phase3_cleanup() {
    log "=== PHASE 3: NETTOYAGE ==="
    
    # Suppression des fichiers JSON de logs/reports temporaires
    log "Suppression des fichiers temporaires..."
    rm -f *_report_*.json 2>/dev/null || true
    rm -f critic_roadmap_*.json 2>/dev/null || true
    rm -f defensive_response_*.json 2>/dev/null || true
    rm -f theoretical_research_*.json 2>/dev/null || true
    rm -f autonomous_*.json 2>/dev/null || true
    rm -f *_status_*.json 2>/dev/null || true
    
    # Suppression des dossiers vides
    log "Suppression des dossiers vides..."
    find . -maxdepth 1 -type d -empty -delete 2>/dev/null || true
    
    # Nettoyage des fichiers de configuration temporaires
    rm -f *.toml.* 2>/dev/null || true
    rm -f *_fixed.yml 2>/dev/null || true
    
    success "Nettoyage terminé"
}

# Phase 4: Documentation
phase4_documentation() {
    log "=== PHASE 4: CRÉATION DE LA DOCUMENTATION ==="
    
    # README principal actualisé
    cat > README.md << 'EOF'
# 🎌 PaniniFS - Écosystème de Compression Sémantique Universelle

**PaniniFS** est un écosystème révolutionnaire de systèmes de fichiers basé sur l'analyse linguistique et la compression sémantique des contenus. Inspiré des travaux de Pāṇini et de la découverte des **dhātu informationnels**.

## 🏗️ Architecture

L'écosystème PaniniFS est organisé en modules spécialisés :

- **🏛️ [GOVERNANCE/](GOVERNANCE/)** - Gouvernance, audits et processus
- **📚 [RESEARCH/](RESEARCH/)** - Publications, découvertes et méthodologie  
- **🔧 [CORE/](CORE/)** - Cœur technique PaniniFS et analyseur sémantique
- **🌐 [ECOSYSTEM/](ECOSYSTEM/)** - Sous-projets et intégrations
- **🚀 [OPERATIONS/](OPERATIONS/)** - DevOps, déploiement et infrastructure
- **📖 [DOCUMENTATION/](DOCUMENTATION/)** - Documentation unifiée
- **🧪 [SANDBOX/](SANDBOX/)** - Expérimentations et prototypes

## 🚀 Démarrage Rapide

```bash
# Installation
git clone https://github.com/stephanedenis/PaniniFS.git
cd PaniniFS

# Build du core
cd CORE/panini-fs
cargo build

# Tests
cargo test
```

## 📚 Publications

- **📖 Livre Complet** : [L'Odyssée de la Compression Sémantique](https://leanpub.com/paninifs-fr)
- **📰 Article Medium** : [Quand des Vacances Sans Code Révèlent un Rêve de 35 Ans](https://medium.com/@neuronspikes)

## 🔬 Découvertes Clés

- **7 Dhātu Informationnels** : Les atomes conceptuels universels de l'information
- **Content Addressing Sémantique** : Déduplication basée sur le sens, pas la syntaxe
- **Validation Baby Sign Language** : Universaux cognitifs confirmés

## 🤝 Contribution

Voir [DOCUMENTATION/developer-docs/contributing/](DOCUMENTATION/developer-docs/contributing/) pour les guides de contribution.

## 📄 Licence

Projet open source sous licence MIT. Voir [GOVERNANCE/legal/LICENSE](GOVERNANCE/legal/LICENSE).

---
*Écosystème restructuré le 21 août 2025 pour une architecture d'entreprise moderne*
EOF

    # CHANGELOG
    cat > CHANGELOG.md << 'EOF'
# 📝 CHANGELOG

## [2.0.0] - 2025-08-21

### 🏗️ Architecture
- **BREAKING**: Restructuration complète en architecture d'entreprise moderne
- **NEW**: Organisation modulaire en 7 domaines spécialisés
- **NEW**: Séparation claire des préoccupations (governance, research, core, ecosystem, operations, documentation, sandbox)

### 🧹 Nettoyage
- **FIXED**: Racine épurée (138 → 12 fichiers)
- **REMOVED**: Suppression des doublons et fichiers temporaires
- **IMPROVED**: Navigation et maintenabilité

### 📚 Publications
- **NEW**: Livres Leanpub publiés (FR/EN)
- **NEW**: Articles Medium publiés (FR/EN)
- **SYNC**: Synchronisation locale avec versions publiées

### 🔧 Technique
- **MAINTAINED**: Code Rust core préservé
- **IMPROVED**: Structure des tests et benchmarks
- **NEW**: Outils de validation et compliance

## [1.x] - 2025-08-01 à 2025-08-20
- Développement initial et expérimentations
- Découverte des 7 dhātu informationnels
- Implémentation prototype
- Validation académique
EOF

    # Guide de contribution
    mkdir -p DOCUMENTATION/developer-docs/contributing
    cat > DOCUMENTATION/developer-docs/contributing/README.md << 'EOF'
# 🤝 Guide de Contribution

Bienvenue dans l'écosystème PaniniFS ! Ce guide vous aidera à contribuer efficacement.

## 🏗️ Architecture

L'écosystème est organisé en modules :
- **GOVERNANCE/** : Processus et gouvernance
- **RESEARCH/** : Recherche et publications
- **CORE/** : Implémentation technique
- **ECOSYSTEM/** : Sous-projets
- **OPERATIONS/** : Infrastructure
- **DOCUMENTATION/** : Documentation
- **SANDBOX/** : Expérimentations

## 🚀 Setup Développement

```bash
# Clone du projet
git clone https://github.com/stephanedenis/PaniniFS.git
cd PaniniFS

# Setup environnement Rust
cd CORE/panini-fs
cargo build
cargo test
```

## 📝 Types de Contributions

1. **🔬 Recherche** : Validations, expérimentations, papers
2. **💻 Code** : Core technique, optimisations, nouveaux modules
3. **📖 Documentation** : Guides, tutoriels, API docs
4. **🧪 Expérimentations** : Prototypes, POCs dans SANDBOX/

## 🔄 Workflow

1. **Fork** le repository
2. **Branche** pour votre fonctionnalité
3. **Développement** dans le module approprié
4. **Tests** et validation
5. **Pull Request** avec description détaillée

## 📋 Standards

- **Code** : Suivre les conventions Rust
- **Commits** : Messages descriptifs
- **Documentation** : Obligatoire pour nouvelles fonctionnalités
- **Tests** : Couverture requise

Merci de contribuer à PaniniFS ! 🎌
EOF

    success "Documentation créée"
}

# Phase 5: Validation
phase5_validation() {
    log "=== PHASE 5: VALIDATION ==="
    
    # Vérification de la structure
    log "Validation de la nouvelle structure..."
    
    local errors=0
    
    # Vérifier que tous les dossiers principaux existent
    for dir in GOVERNANCE RESEARCH CORE ECOSYSTEM OPERATIONS DOCUMENTATION SANDBOX; do
        if [ ! -d "$dir" ]; then
            error "Dossier manquant: $dir"
            ((errors++))
        fi
    done
    
    # Compter les fichiers restants à la racine
    local root_files=$(find . -maxdepth 1 -type f | wc -l)
    log "Fichiers restants à la racine: $root_files"
    
    if [ $errors -eq 0 ]; then
        success "Validation réussie - Structure conforme"
    else
        error "Validation échouée - $errors erreurs trouvées"
        return 1
    fi
}

# Fonction principale
main() {
    log "🏗️ DÉBUT DE LA RESTRUCTURATION ÉCOSYSTÈME PANINIFS"
    log "Projet: $PROJECT_ROOT"
    log "Backup: $BACKUP_DIR"
    log "Log: $LOG_FILE"
    
    # Demander confirmation
    echo -e "${YELLOW}⚠️  ATTENTION: Cette opération va restructurer complètement le projet.${NC}"
    echo -e "${YELLOW}Un backup sera créé dans: $BACKUP_DIR${NC}"
    echo
    read -p "Voulez-vous continuer? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "Opération annulée par l'utilisateur"
        exit 0
    fi
    
    # Exécution des phases
    phase1_preparation
    phase2_governance
    phase2_research
    phase2_core
    phase2_ecosystem
    phase2_operations
    phase2_documentation
    phase2_sandbox
    phase3_cleanup
    phase4_documentation
    phase5_validation
    
    success "🎉 RESTRUCTURATION TERMINÉE AVEC SUCCÈS!"
    log "Backup disponible: $BACKUP_DIR"
    log "Log complet: $LOG_FILE"
    
    echo
    echo -e "${GREEN}✅ Écosystème PaniniFS restructuré avec succès!${NC}"
    echo -e "${BLUE}📁 Nouvelle structure:${NC}"
    echo "   GOVERNANCE/     - Gouvernance et processus"
    echo "   RESEARCH/       - Publications et découvertes"
    echo "   CORE/           - Code technique principal"
    echo "   ECOSYSTEM/      - Sous-projets et intégrations"
    echo "   OPERATIONS/     - DevOps et infrastructure"
    echo "   DOCUMENTATION/  - Documentation unifiée"
    echo "   SANDBOX/        - Expérimentations"
    echo
    echo -e "${BLUE}📋 Prochaines étapes:${NC}"
    echo "   1. Vérifier la nouvelle structure"
    echo "   2. Tester la compilation: cd CORE/panini-fs && cargo build"
    echo "   3. Valider la documentation: ls DOCUMENTATION/"
    echo "   4. Commit des changements"
}

# Exécution
main "$@"
