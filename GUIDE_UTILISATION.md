# 📖 Guide d'Utilisation - Panini-FS v2.0

**Système de graphe de connaissances distribué avec Git**

---

## 🚀 Installation

### Prérequis
```bash
# Rust 1.75+
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Git
sudo zypper install git  # openSUSE
# ou: sudo apt install git  # Ubuntu/Debian
```

### Compilation
```bash
cd Panini-FS
cargo build --release

# Le binaire est dans target/release/panini
sudo cp target/release/panini /usr/local/bin/
```

### Vérification
```bash
panini --version
# Panini-FS v2.0.0
```

---

## 🎯 Utilisation de Base

### 1. Initialiser un Nouveau Répertoire de Connaissances

```bash
# Créer un nouveau répertoire
panini init mon-savoir

# Ou initialiser dans le répertoire courant
cd mon-savoir
panini init .
```

**Ce qui est créé:**
```
mon-savoir/
├── .git/              # Dépôt Git
├── .panini/           # Configuration + index
│   ├── config.toml
│   └── index/
│       ├── rocks/     # RocksDB (métadonnées)
│       └── tantivy/   # Tantivy (recherche fulltext)
└── knowledge/         # Dossier pour vos concepts
```

---

### 2. Créer des Concepts

#### Création Simple
```bash
panini create rust-lang --title "Rust Programming Language"

# Affiche:
# ✅ Created concept: rust-lang
```

#### Création avec Tags
```bash
panini create docker \
  --title "Docker Containerization" \
  --tags "devops,containers,cloud"
```

#### Création avec Corps de Texte
```bash
panini create kubernetes \
  --title "Kubernetes" \
  --body "Kubernetes est un système d'orchestration de conteneurs open-source..."
```

---

### 3. Lire des Concepts

#### Lecture Formatée (Défaut)
```bash
panini read rust-lang

# Affiche:
# 📄 Rust Programming Language
# 
# ID: rust-lang
# Type: Concept
# Dhatu: TEXT
# Tags: programming, systems
# Created: 2025-10-30 14:30:00
# ...
```

#### Lecture JSON
```bash
panini read rust-lang --format json

# Retourne:
# {
#   "id": "rust-lang",
#   "title": "Rust Programming Language",
#   "type": "Concept",
#   ...
# }
```

---

### 4. Lister les Concepts

#### Liste Simple
```bash
panini list

# Affiche:
# 📚 Concepts (3)
# 
# - rust-lang: Rust Programming Language
# - docker: Docker Containerization  
# - kubernetes: Kubernetes
```

#### Liste JSON
```bash
panini list --format json | jq '.'
```

---

### 5. Modifier des Concepts

```bash
panini update rust-lang \
  --title "Rust: Memory-Safe Systems Programming" \
  --tags "rust,systems,memory-safety"
```

---

### 6. Supprimer des Concepts

```bash
panini delete old-concept

# Demande confirmation
# ⚠️  Delete concept 'old-concept'? [y/N] y
# ✅ Deleted concept: old-concept
```

---

## 🔗 Relations entre Concepts

### Types de Relations Disponibles

| Type | Description | Exemple |
|------|-------------|---------|
| **IsA** | Hiérarchie taxonomique | "Rust IsA ProgrammingLanguage" |
| **PartOf** | Composition | "Chapter1 PartOf Book" |
| **RelatedTo** | Association générale | "Docker RelatedTo Kubernetes" |
| **Causes** | Causalité | "Rain Causes Wetness" |
| **Requires** | Dépendance | "App Requires Database" |
| **Implements** | Implémentation | "RustCompiler Implements Compiler" |

### Ajouter une Relation

#### Relation Simple
```bash
panini add-relation rust-lang \
  --rel-type is_a \
  programming-language

# Affiche:
# ✅ rust-lang --IsA--> programming-language
```

#### Relation avec Confiance
```bash
panini add-relation docker \
  --rel-type related_to \
  kubernetes \
  --confidence 0.95

# La confiance (0.0 à 1.0) indique la force de la relation
```

### Lister les Relations d'un Concept

```bash
panini relations rust-lang

# Affiche:
# 🔗 Relations (2):
#   IsA --> programming-language
#   RelatedTo --> cargo
```

---

## 🔍 Recherche Avancée

### Recherche Fulltext

```bash
# Rechercher dans tous les champs
panini search "memory safety"

# Rechercher avec limite de résultats
panini search "containerization" --limit 10
```

### Recherche par Tag

```bash
# Rechercher tous les concepts avec tag "rust"
panini search "tag:rust"

# Rechercher plusieurs tags
panini search "tag:devops tag:cloud"
```

### Recherche par Type

```bash
panini search "type:concept"
```

---

## 📊 Workflows Avancés

### Créer une Hiérarchie de Connaissances

```bash
# 1. Créer les concepts
panini create computer-science --title "Computer Science"
panini create programming --title "Programming"
panini create rust-lang --title "Rust"
panini create python --title "Python"

# 2. Établir les relations hiérarchiques
panini add-relation programming --rel-type part_of computer-science
panini add-relation rust-lang --rel-type is_a programming
panini add-relation python --rel-type is_a programming

# 3. Visualiser
panini relations computer-science
```

### Documenter un Projet Technique

```bash
# Structure d'un projet microservices
panini create microservices-arch --title "Microservices Architecture" \
  --tags "architecture,distributed-systems"

panini create api-gateway --title "API Gateway Pattern" \
  --body "Point d'entrée unique pour les clients..."

panini create service-discovery --title "Service Discovery" \
  --body "Mécanisme pour localiser les services..."

# Relier les concepts
panini add-relation api-gateway --rel-type part_of microservices-arch
panini add-relation service-discovery --rel-type part_of microservices-arch
panini add-relation api-gateway --rel-type requires service-discovery --confidence 0.9
```

### Capturer des Notes de Lecture

```bash
# Créer un concept pour un livre
panini create designing-data-intensive-apps \
  --title "Designing Data-Intensive Applications" \
  --tags "books,databases,distributed-systems"

# Ajouter des concepts clés
panini create cap-theorem --title "CAP Theorem" \
  --body "Impossible d'avoir simultanément Consistency, Availability, Partition tolerance"

panini add-relation cap-theorem \
  --rel-type part_of \
  designing-data-intensive-apps
```

---

## 🔄 Versionning et Synchronisation Git

### Voir l'Historique

```bash
# Voir l'historique d'un concept
git log knowledge/rust-lang.md

# Voir les changements
git diff HEAD~1 knowledge/rust-lang.md
```

### Synchroniser avec GitHub

```bash
# Ajouter un remote
cd mon-savoir
git remote add origin https://github.com/username/mon-savoir.git

# Pousser vos connaissances
git push -u origin main

# Récupérer depuis un autre ordinateur
git clone https://github.com/username/mon-savoir.git
cd mon-savoir
panini list  # Vos concepts sont là!
```

### Collaborer

```bash
# Personne A ajoute des concepts
panini create concept-a --title "Concept A"
git push

# Personne B récupère et ajoute
git pull
panini create concept-b --title "Concept B"
panini add-relation concept-b --rel-type related_to concept-a
git push
```

---

## 📁 Format des Fichiers

Les concepts sont stockés en **Markdown + YAML frontmatter**:

```markdown
---
id: rust-lang
type: Concept
dhatu: TEXT
title: Rust Programming Language
tags:
  - programming
  - systems
  - memory-safety
created: 2025-10-30T14:30:00Z
updated: 2025-10-30T14:30:00Z
author: stephane
relations:
  - rel_type: IsA
    target: programming-language
    confidence: 1.0
    evidence: []
    created: 2025-10-30T14:30:00Z
    author: stephane
content_refs: []
metadata: {}
---

# Rust Programming Language

Rust est un langage de programmation système qui garantit la sûreté mémoire sans garbage collector...

## Caractéristiques

- Ownership system
- Zero-cost abstractions
- Memory safety
- Concurrency without data races

## Exemples

\`\`\`rust
fn main() {
    println!("Hello, world!");
}
\`\`\`
```

**Vous pouvez éditer ces fichiers directement** avec votre éditeur préféré!

---

## 🛠️ Configuration

### Fichier `.panini/config.toml`

```toml
[repository]
name = "mon-savoir"
description = "Ma base de connaissances personnelle"

[storage]
knowledge_dir = "knowledge"

[index]
rocks_path = ".panini/index/rocks"
tantivy_path = ".panini/index/tantivy"

[sync]
# Configuration future pour la synchronisation distribuée
```

---

## 🎨 Intégration avec d'Autres Outils

### Obsidian / Logseq

Les fichiers Panini-FS sont compatibles avec Obsidian et Logseq! Le frontmatter YAML est supporté.

```bash
# Ouvrir votre base dans Obsidian
# File > Open Vault > mon-savoir/knowledge/
```

### VS Code

```bash
# Ouvrir dans VS Code
code mon-savoir/

# Extensions recommandées:
# - Markdown All in One
# - YAML
# - Git Graph
```

### Scripts Personnalisés

```python
# Lire les concepts en Python
import yaml
import frontmatter

with open('knowledge/rust-lang.md', 'r') as f:
    post = frontmatter.load(f)
    print(post['title'])
    print(post.content)
```

---

## 🚨 Dépannage

### Problème: "Repository not initialized"

```bash
# Solution: Initialiser le répertoire
panini init .
```

### Problème: "Concept not found"

```bash
# Vérifier les concepts existants
panini list

# Vérifier l'ID exact
ls knowledge/
```

### Problème: Index corrompu

```bash
# Reconstruire l'index
rm -rf .panini/index/
panini list  # Reconstruit automatiquement
```

### Problème: Conflit Git

```bash
# Résoudre manuellement
git status
git diff
# Éditer les fichiers en conflit
git add .
git commit -m "Resolve conflict"
```

---

## 📚 Exemples de Cas d'Usage

### 1. Base de Connaissances Personnelle

```bash
panini init ~/knowledge
cd ~/knowledge

# Capturer des apprentissages quotidiens
panini create til-$(date +%Y%m%d) \
  --title "Today I Learned: $(date +%Y-%m-%d)" \
  --tags "til,daily"
```

### 2. Documentation de Projet

```bash
cd mon-projet/
panini init docs/knowledge

panini create architecture --title "System Architecture"
panini create api-spec --title "API Specification"
panini create deployment --title "Deployment Guide"

panini add-relation api-spec --rel-type part_of architecture
panini add-relation deployment --rel-type requires architecture
```

### 3. Notes de Recherche

```bash
panini init ~/research

panini create paper-001 --title "Distributed Consensus Algorithms" \
  --tags "research,consensus,distributed-systems"

panini create raft --title "Raft Consensus Algorithm" \
  --body "Leader-based consensus..."

panini add-relation raft --rel-type part_of paper-001 --confidence 1.0
```

### 4. Zettelkasten

```bash
panini init ~/zettelkasten

# Notes atomiques
panini create 202510301430 --title "Memory Safety in Rust" \
  --tags "rust,memory"

panini create 202510301445 --title "Ownership System" \
  --tags "rust,ownership"

# Relier les notes
panini add-relation 202510301445 --rel-type related_to 202510301430
```

---

## 🎓 Bonnes Pratiques

### Nommage des Concepts

✅ **Bon:**
- `rust-programming-language`
- `docker-compose-tutorial`
- `cap-theorem`

❌ **Éviter:**
- `Concept 1` (trop générique)
- `rust-lang!!!` (caractères spéciaux)
- `this is a very long name with spaces` (espaces)

### Organisation avec Tags

```bash
# Utiliser une hiérarchie de tags
--tags "programming/rust,systems,learning"
--tags "devops/docker,containers,tutorial"
--tags "research/papers,distributed-systems,consensus"
```

### Utiliser les Relations

- **IsA**: Pour la taxonomie (classification)
- **PartOf**: Pour la composition (chapitres, sections)
- **RelatedTo**: Pour les liens conceptuels
- **Requires**: Pour les dépendances techniques
- **Confidence**: Utiliser 1.0 pour les faits, 0.5-0.9 pour les hypothèses

### Commits Git Fréquents

```bash
# Après chaque session de travail
git add knowledge/
git commit -m "feat: Add notes on Rust ownership system"
git push
```

---

## 🔮 Fonctionnalités à Venir

- [ ] `panini sync` - Synchronisation distribuée entre dépôts
- [ ] `panini status` - État du dépôt et index
- [ ] `panini graph` - Visualisation graphique des relations
- [ ] `panini export` - Export en différents formats (HTML, PDF, JSON)
- [ ] `panini import` - Import depuis Notion, Obsidian, etc.
- [ ] API REST (panini-server)

---

## 📞 Support

- **Documentation**: `panini --help`
- **GitHub**: https://github.com/stephanedenis/Panini-FS
- **Issues**: https://github.com/stephanedenis/Panini-FS/issues

---

## 📄 Licence

MIT License - Voir LICENSE pour plus de détails.

---

**Fait avec ❤️ pour les passionnés de gestion des connaissances**
