# 🥖 Panini-FS v2.0

**Système de graphe de connaissances distribué avec Git**

[![Tests](https://img.shields.io/badge/tests-149%2F149%20passing-brightgreen)](TEST_RESULTS.md)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/stephanedenis/Panini-FS)
[![Rust](https://img.shields.io/badge/rust-1.88%2B-orange)](https://www.rust-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## 🎯 En Bref

Panini-FS est un système de **gestion de connaissances** qui combine:

- 🌳 **Git** pour le versionning distribué
- 📝 **Markdown + YAML** pour le format lisible
- 🔍 **RocksDB + Tantivy** pour l'indexation rapide
- 🔗 **Graphe de connaissances** pour relier les concepts
- 💻 **CLI moderne** en Rust

```bash
# Créer votre base de connaissances en 30 secondes
panini init mon-savoir
cd mon-savoir
panini create rust --title "Rust Programming"
panini list
```

---

## ✨ Fonctionnalités

- ✅ **Git-native**: Chaque concept est versionné, branché, fusionné
- ✅ **Format ouvert**: Markdown + YAML = éditable partout
- ✅ **Recherche rapide**: Tantivy pour recherche fulltext 20+ langues
- ✅ **Relations typées**: IsA, PartOf, RelatedTo, Causes, Requires...
- ✅ **Local-first**: Pas de cloud requis, fonctionne offline
- ✅ **Distribué**: Push/pull comme Git
- ✅ **100% testé**: 149 tests automatisés

---

## 🚀 Installation

### Prérequis

- Rust 1.75+ ([rustup.rs](https://rustup.rs/))
- Git

### Build

```bash
git clone https://github.com/stephanedenis/Panini-FS.git
cd Panini-FS
cargo build --release
sudo cp target/release/panini /usr/local/bin/
```

### Vérification

```bash
panini --version
# Panini-FS v2.0.0
```

---

## 📖 Documentation

- **[⚡ Démarrage Rapide](QUICKSTART.md)** - 5 minutes pour commencer
- **[📚 Guide Complet](GUIDE_UTILISATION.md)** - Tout ce qu'il faut savoir
- **[🧪 Résultats Tests](TEST_RESULTS.md)** - 149/149 tests passing
- **[🏗️ Architecture](docs/ARCHITECTURE.md)** - Design technique

---

## 💡 Exemples

### Créer une Base de Connaissances Personnelle

```bash
panini init ~/knowledge
cd ~/knowledge

# Ajouter des concepts
panini create rust-ownership \
  --title "Rust Ownership System" \
  --tags "rust,memory-safety"

panini create borrowing \
  --title "Borrowing Rules" \
  --tags "rust,memory-safety"

# Relier les concepts
panini add-relation borrowing \
  --rel-type part_of \
  rust-ownership \
  --confidence 1.0

# Explorer
panini relations rust-ownership
panini search "memory safety"
```

### Documentation de Projet

```bash
cd mon-projet/
panini init docs/knowledge

# Structure de documentation
panini create architecture --title "System Architecture"
panini create api --title "API Design"
panini create deployment --title "Deployment Guide"

# Relations
panini add-relation api --rel-type part_of architecture
panini add-relation deployment --rel-type requires architecture
```

### Zettelkasten / Notes Atomiques

```bash
# Notes avec timestamp
panini create $(date +%Y%m%d%H%M) \
  --title "Learning: Rust Lifetimes" \
  --tags "til,rust,learning"

# Liens entre notes
panini add-relation 202510301430 \
  --rel-type related_to 202510301445
```

---

## 🏗️ Architecture

```
Panini-FS
│
├── Git Repository          # Storage backend
│   └── knowledge/         # Markdown + YAML files
│
├── Index Layer
│   ├── RocksDB            # Metadata & relations
│   └── Tantivy            # Fulltext search
│
├── Core Library           # Business logic
│   ├── Concepts           # CRUD operations
│   ├── Relations          # Graph operations
│   ├── Query Engine       # Unified search
│   └── Git Integration    # Version control
│
└── CLI                    # User interface
    └── 12 commands        # init, create, read, ...
```

---

## 🎨 Format des Fichiers

Les concepts sont stockés en **Markdown lisible**:

```markdown
---
id: rust-ownership
type: Concept
title: Rust Ownership System
tags: [rust, memory-safety]
relations:
  - rel_type: PartOf
    target: rust-lang
    confidence: 1.0
---

# Rust Ownership System

L'ownership est la fonctionnalité phare de Rust...

## Règles

1. Chaque valeur a un owner
2. Un seul owner à la fois
3. Quand le owner sort du scope, la valeur est droppée
```

**Compatible avec**: Obsidian, Logseq, VS Code, tout éditeur Markdown!

---

## 🧪 Qualité

- ✅ **149 tests** automatisés (100% passing)
- ✅ **0 erreurs** de compilation
- ✅ **112 tests** core library
- ✅ **12 tests** CLI
- ✅ **25 tests** intégration
- ✅ **Binary release** 7.4 MB fonctionnel

Voir [TEST_RESULTS.md](TEST_RESULTS.md) pour les détails.

---

## 🛣️ Roadmap

### v2.0 ✅ (Actuel)
- [x] Git-native storage
- [x] RocksDB + Tantivy indexing
- [x] CLI complet (12 commandes)
- [x] Relations typées
- [x] Recherche fulltext

### v2.1 🚧 (Prochain)
- [ ] `panini sync` - Synchronisation distribuée
- [ ] `panini status` - État du dépôt
- [ ] `panini graph` - Visualisation
- [ ] `panini export` - Export HTML/PDF
- [ ] API REST (panini-server)

### v2.2 🔮 (Futur)
- [ ] Import Notion/Obsidian
- [ ] Collaboration temps réel
- [ ] S3-compatible storage
- [ ] Web UI

---

## 🤝 Contribution

Les contributions sont bienvenues! Voir [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
# Development
cargo build
cargo test --all
cargo run -- init test-repo

# Format
cargo fmt
cargo clippy
```

---

## 📊 Statistiques

- **~10,000** lignes de code production
- **~3,500** lignes de documentation
- **149** tests automatisés
- **38** commits depuis le début
- **6** modules core
- **12** commandes CLI

---

## 📜 Licence

MIT License - Voir [LICENSE](LICENSE)

---

## 🙏 Remerciements

- [Git](https://git-scm.com/) pour le stockage distribué
- [Tantivy](https://github.com/quickwit-oss/tantivy) pour la recherche
- [RocksDB](https://rocksdb.org/) pour l'indexation
- [Rust](https://www.rust-lang.org/) pour la performance et sûreté

---

## 📞 Contact

- **Issues**: https://github.com/stephanedenis/Panini-FS/issues
- **Discussions**: https://github.com/stephanedenis/Panini-FS/discussions

---

<div align="center">

**Fait avec ❤️ pour les passionnés de gestion des connaissances**

[⭐ Star sur GitHub](https://github.com/stephanedenis/Panini-FS) | [📖 Documentation](GUIDE_UTILISATION.md) | [🚀 Démarrage Rapide](QUICKSTART.md)

</div>
