# ⚡ Démarrage Rapide - Panini-FS

**En 5 minutes, créez votre première base de connaissances!**

---

## Installation (1 min)

```bash
cd Panini-FS
cargo build --release
sudo cp target/release/panini /usr/local/bin/
```

---

## Premiers Pas (4 min)

### 1. Initialiser 🎬

```bash
mkdir mon-savoir && cd mon-savoir
panini init .
```

### 2. Créer des Concepts 📝

```bash
# Créer 3 concepts
panini create rust --title "Rust Programming"
panini create cargo --title "Cargo Build System"
panini create ownership --title "Ownership Model"
```

### 3. Ajouter des Relations 🔗

```bash
# Établir les liens
panini add-relation cargo --rel-type part_of rust
panini add-relation ownership --rel-type part_of rust
```

### 4. Explorer 🔍

```bash
# Lister tous les concepts
panini list

# Voir un concept
panini read rust

# Voir les relations
panini relations rust
```

### 5. Rechercher ��

```bash
# Recherche fulltext
panini search "ownership"

# Recherche par tag
panini create rust --tags "programming,systems"
panini search "tag:programming"
```

---

## Commandes Essentielles

```bash
panini init <dir>                    # Initialiser
panini create <id> --title <titre>   # Créer concept
panini read <id>                     # Lire concept
panini update <id> --title <titre>   # Modifier
panini delete <id>                   # Supprimer
panini list                          # Lister tout
panini add-relation <src> --rel-type <type> <target>  # Relier
panini relations <id>                # Voir relations
panini search <query>                # Rechercher
```

---

## Structure Créée

```
mon-savoir/
├── .git/              # Version control
├── .panini/           # Index & config
└── knowledge/         # Vos concepts (Markdown)
    ├── rust.md
    ├── cargo.md
    └── ownership.md
```

---

## Prochaines Étapes

📖 Lire le [Guide Complet](GUIDE_UTILISATION.md)  
🔧 Voir les [Exemples Avancés](GUIDE_UTILISATION.md#-workflows-avancés)  
🚀 Personnaliser avec [Configuration](GUIDE_UTILISATION.md#-configuration)

---

**C'est tout! Vous êtes prêt! 🎉**
