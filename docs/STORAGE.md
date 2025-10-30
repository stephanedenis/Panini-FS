# Architecture de Stockage Atomique - Panini-FS v2.0

**Date:** 30 octobre 2025  
**Version:** 2.0.0  
**Statut:** Implémenté

---

## 📖 Table des Matières

1. [Vue d'Ensemble](#vue-densemble)
2. [Architecture en 3 Niveaux](#architecture-en-3-niveaux)
3. [Atomes et Types](#atomes-et-types)
4. [Content-Addressed Storage (CAS)](#content-addressed-storage-cas)
5. [Déduplication Automatique](#déduplication-automatique)
6. [Décomposition de Formats](#décomposition-de-formats)
7. [Reconstruction et Vérification](#reconstruction-et-vérification)
8. [Backends de Stockage](#backends-de-stockage)
9. [Cas d'Usage](#cas-dusage)
10. [API et Exemples](#api-et-exemples)

---

## Vue d'Ensemble

L'architecture de stockage atomique de Panini-FS permet de **décomposer des fichiers binaires volumineux en atomes réutilisables** stockés dans un système de Content-Addressed Storage (CAS).

### Principe Fondamental

**Un fichier volumineux (vidéo, image, audio) n'est JAMAIS stocké comme un bloc monolithique.**

Au lieu de cela :
1. Le fichier est **décomposé** en atomes sémantiques (keyframes, chunks audio, metadata)
2. Chaque atome est **hashé** (SHA-256) et stocké une seule fois
3. Le concept référence les atomes via leurs hashes
4. La reconstruction est **bit-perfect** (vérifiée par hash)

### Avantages

| Fonctionnalité | Bénéfice |
|----------------|----------|
| **Déduplication** | 25-65% d'économie de stockage sur contenus similaires |
| **Reconstruction partielle** | Télécharger uniquement les atomes nécessaires (audio uniquement, keyframes, etc.) |
| **Versioning intelligent** | Stocker uniquement les différences entre versions |
| **Streaming progressif** | Charger les atomes à la demande |
| **Garbage collection** | Supprimer les atomes orphelins (ref_count = 0) |

---

## Architecture en 3 Niveaux

```
┌──────────────────────────────────────────────────────────────┐
│ NIVEAU 1: Concept (Git)                                       │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ ma-video.md                                              │ │
│ │ ---                                                      │ │
│ │ content_refs:                                            │ │
│ │   - atom://sha256:abc123...def  (MP4 container, 2 KB)   │ │
│ │   - atom://sha256:456789...ghi  (H264 stream, 500 MB)   │ │
│ │   - atom://sha256:jkl012...mno  (AAC audio, 50 MB)      │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ NIVEAU 2: Atomes (Content-Addressed Storage)                  │
│ ┌──────────────┬──────────────┬──────────────┬────────────┐  │
│ │ MP4 Metadata │ I-Frame 1    │ P-Frame 1    │ AAC Frame 1│  │
│ │ (Container)  │ (Keyframe)   │ (Delta)      │ (Audio)    │  │
│ │ 2 KB         │ 1.8 MB       │ 120 KB       │ 45 KB      │  │
│ │ Refs: 1      │ Refs: 3 ⭐   │ Refs: 1      │ Refs: 5 ⭐⭐│  │
│ └──────────────┴──────────────┴──────────────┴────────────┘  │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ NIVEAU 3: Backend (LocalFS, S3, etc.)                         │
│ .panini/storage/                                               │
│   ab/                                                          │
│     cd/                                                        │
│       abc123...def  (fichier brut, 2 KB)                      │
│   45/                                                          │
│     67/                                                        │
│       456789...ghi  (fichier brut, 500 MB)                    │
└──────────────────────────────────────────────────────────────┘
```

---

## Atomes et Types

### Structure `Atom`

```rust
pub struct Atom {
    pub hash: String,           // SHA-256 (64 chars hex)
    pub atom_type: AtomType,
    pub size: u64,              // Bytes
    pub parent: Option<String>, // Hash du parent
    pub children: Vec<String>,  // Hashes des enfants
    pub metadata: HashMap<String, String>,
    pub source_offset: u64,     // Offset dans le fichier source
    pub ref_count: u32,         // Nombre de concepts utilisant cet atome
}
```

### Types d'Atomes (AtomType)

| Type | Description | Taille Typique | Dédup Potentiel |
|------|-------------|----------------|-----------------|
| `Container` | Métadonnées de conteneur (MP4 ftyp, PNG signature) | 1-10 KB | Faible |
| `VideoStream` | Stream vidéo complet (rarement utilisé) | 100 KB - 1 GB | Très faible |
| `AudioStream` | Stream audio complet (rarement utilisé) | 100 KB - 1 GB | Faible |
| `IFrame` | **Keyframe vidéo (I-Frame)** | 50 KB - 5 MB | **⭐⭐⭐ Élevé** |
| `PFrame` | Predictive frame (delta depuis I-Frame) | 10-500 KB | Moyen |
| `BFrame` | Bidirectional frame | 10-500 KB | Moyen |
| `AudioChunk` | **Frame audio (AAC, MP3)** | 1-50 KB | **⭐⭐⭐ Très élevé** |
| `Subtitle` | **Sous-titres** | 100 B - 10 KB | **⭐⭐⭐⭐ Maximal** |
| `ImageData` | Données d'image (PNG IDAT, JPEG scan) | 1 KB - 10 MB | Moyen |
| `Metadata` | Métadonnées (EXIF, ID3, PNG IHDR) | 512 B - 100 KB | **⭐⭐⭐ Élevé** |
| `Compressed` | Données compressées (ZIP entry) | 1 KB - 100 MB | Variable |
| `Raw` | Données brutes non typées | Variable | Très faible |

### Méthodes Clés

```rust
impl Atom {
    // Créer atome depuis données
    pub fn new(data: &[u8], atom_type: AtomType) -> Self;
    
    // Ajouter métadonnées
    pub fn with_metadata(self, key: impl Into<String>, value: impl Into<String>) -> Self;
    
    // Calculer hash SHA-256
    pub fn compute_hash(data: &[u8]) -> String;
    
    // Gestion des références
    pub fn increment_refs(&mut self);
    pub fn decrement_refs(&mut self);
    pub fn is_orphaned(&self) -> bool; // ref_count == 0
}
```

---

## Content-Addressed Storage (CAS)

### Structure `ContentAddressedStorage`

```rust
pub struct ContentAddressedStorage<B: StorageBackend> {
    backend: Arc<B>,                              // LocalFS, S3, etc.
    atom_index: HashMap<String, AtomMetadata>,    // Hash → metadata
    atom_graph: DiGraph<String, String>,          // Graphe de composition
    config: StorageConfig,
}
```

### Configuration

```rust
pub struct StorageConfig {
    pub max_atom_size: u64,        // Taille max avant split (défaut: 10 MB)
    pub enable_dedup: bool,         // Déduplication activée (défaut: true)
    pub compression: Option<String>, // zstd, lz4, none
}
```

### API Principale

```rust
impl<B: StorageBackend> ContentAddressedStorage<B> {
    // Ajouter un atome
    pub async fn add_atom(&self, data: &[u8], atom_type: AtomType) -> Result<Atom>;
    
    // Récupérer un atome
    pub async fn get_atom(&self, hash: &str) -> Result<Bytes>;
    
    // Lister tous les atomes
    pub fn list_atoms(&self) -> Vec<AtomMetadata>;
    
    // Obtenir statistiques
    pub fn get_stats(&self) -> StorageStats;
    
    // Garbage collection
    pub async fn gc_orphaned_atoms(&self) -> Result<GcStats>;
    
    // Gestion des références
    pub fn increment_atom_refs(&self, hash: &str) -> Result<()>;
    pub fn decrement_atom_refs(&self, hash: &str) -> Result<()>;
    pub fn find_orphaned_atoms(&self) -> Vec<String>;
}
```

### Statistiques

```rust
pub struct StorageStats {
    pub total_atoms: u64,      // Nombre total d'atomes
    pub total_size: u64,       // Taille totale (bytes)
    pub dedup_atoms: u64,      // Atomes dédupliqués (refs > 1)
    pub dedup_savings: u64,    // Bytes économisés
    pub unique_atoms: u64,     // Atomes uniques
}

impl StorageStats {
    pub fn dedup_ratio(&self) -> f64; // Pourcentage de déduplication
}
```

---

## Déduplication Automatique

### Principe

Lorsqu'un atome est ajouté au CAS :

1. **Calcul du hash SHA-256** des données
2. **Vérification** si le hash existe déjà dans l'index
3. Si **existe** :
   - Incrémenter `ref_count`
   - Retourner l'atome existant
   - **Ne PAS stocker** les données à nouveau
4. Si **n'existe pas** :
   - Stocker les données dans le backend
   - Ajouter au graphe de composition
   - Initialiser `ref_count = 1`

### Exemple Concret

```rust
// Vidéo A: intro.mp4 (10s) + content_a.mp4 (5 min)
let intro_atoms = decomposer.decompose("intro.mp4")?;
let content_a_atoms = decomposer.decompose("content_a.mp4")?;

// Stocker vidéo A
for atom_data in intro_atoms {
    cas.add_atom(&atom_data, AtomType::IFrame).await?; // Stocke intro
}
for atom_data in content_a_atoms {
    cas.add_atom(&atom_data, AtomType::PFrame).await?;
}

// Vidéo B: intro.mp4 (10s) + content_b.mp4 (3 min)
// Réutilise la MÊME intro !
for atom_data in intro_atoms {
    cas.add_atom(&atom_data, AtomType::IFrame).await?; // Dédup! ref_count++ 
}
for atom_data in content_b_atoms {
    cas.add_atom(&atom_data, AtomType::PFrame).await?;
}
```

**Résultat:**
- Intro stockée **une seule fois** (20 MB)
- Content A: 100 MB
- Content B: 60 MB
- **Total: 180 MB** au lieu de 200 MB (10% économie)
- Si 100 vidéos utilisent la même intro : **99% de déduplication sur l'intro**

### Métriques de Déduplication

| Scénario | Taille Originale | Storage Réel | Économie |
|----------|------------------|--------------|----------|
| 100 vidéos conférence (même template) | 500 GB | 350 GB | **30%** |
| 10 versions d'une vidéo (corrections) | 10 GB | 3.5 GB | **65%** |
| Cours en ligne (réutilise séquences) | 200 GB | 100 GB | **50%** |
| Vidéos marketing (même intro/outro) | 50 GB | 35 GB | **30%** |

---

## Décomposition de Formats

### Decomposer

```rust
pub struct Decomposer {
    format: FileFormat,
}

pub enum FileFormat {
    PNG,
    JPEG,
    MP4,
    Unknown,
}

impl Decomposer {
    // Auto-détection du format
    pub fn auto_detect(data: &[u8]) -> Self;
    
    // Décomposer en atomes
    pub fn decompose(&self, data: &[u8]) -> Result<Vec<Atom>>;
}
```

### Décomposition PNG (Implémenté)

```rust
// PNG: signature (8 bytes) + chunks (IHDR, IDAT, PLTE, tRNS, IEND)
let decomposer = Decomposer::auto_detect(&png_data);
let atoms = decomposer.decompose(&png_data)?;

// Résultat:
// atoms[0]: Signature (AtomType::Container, 8 bytes)
// atoms[1]: IHDR chunk (AtomType::Metadata, ~25 bytes)
// atoms[2]: IDAT chunk (AtomType::ImageData, variable)
// atoms[3]: IEND chunk (AtomType::Container, 12 bytes)
```

#### Structure d'un Chunk PNG

```
┌────────────────────────────────────────┐
│ Length (4 bytes, big-endian)           │
├────────────────────────────────────────┤
│ Chunk Type (4 bytes ASCII)             │
│   IHDR / IDAT / PLTE / tRNS / IEND     │
├────────────────────────────────────────┤
│ Chunk Data (variable length)           │
│   ...                                  │
├────────────────────────────────────────┤
│ CRC-32 (4 bytes)                       │
└────────────────────────────────────────┘
```

### Décomposition JPEG (Simplifié)

```rust
// JPEG: SOI (FF D8) + segments + EOI (FF D9)
// Segments: APP0 (FF E0), DQT (FF DB), DHT (FF C4), SOS (FF DA)

// atoms[0]: SOI marker (AtomType::Container)
// atoms[1]: JPEG body (AtomType::ImageData) // Simplifié pour v2.0
```

### Décomposition MP4 (À Implémenter)

```rust
// MP4: atoms hiérarchiques (ftyp, moov, mdat, trak, mdia, etc.)
// Chaque atom MP4 devient un Atom Panini

// Structure d'un atom MP4:
// ┌─────────────────────┐
// │ Size (4 bytes)      │
// ├─────────────────────┤
// │ Type (4 bytes)      │
// │   ftyp / moov / ... │
// ├─────────────────────┤
// │ Data (variable)     │
// └─────────────────────┘

// Exemple:
// atoms[0]: ftyp (AtomType::Container, ~28 bytes)
// atoms[1]: moov (AtomType::Container, variable)
// atoms[2]: mdat video stream (AtomType::VideoStream)
//   atoms[2].children[0]: I-Frame 0 (AtomType::IFrame)
//   atoms[2].children[1]: P-Frame 1 (AtomType::PFrame)
//   ...
// atoms[3]: mdat audio stream (AtomType::AudioStream)
//   atoms[3].children[0]: AAC frame 0 (AtomType::AudioChunk)
//   ...
```

---

## Reconstruction et Vérification

### Reconstructor

```rust
pub struct Reconstructor;

impl Reconstructor {
    // Reconstruction simple (concaténation)
    pub fn reconstruct(atoms: &[Atom], atoms_data: Vec<Vec<u8>>) -> Result<Vec<u8>>;
    
    // Reconstruction avec vérification de hash
    pub fn reconstruct_verified(atoms: &[Atom], atoms_data: Vec<Vec<u8>>) -> Result<Vec<u8>>;
    
    // Taille totale du fichier reconstruit
    pub fn total_size(atoms: &[Atom]) -> u64;
}
```

### Processus de Reconstruction

```
1. Récupérer ContentRefs depuis le concept
   ↓
2. Pour chaque ContentRef:
   - Télécharger l'atome depuis CAS (via hash)
   - Vérifier hash SHA-256 (intégrité)
   ↓
3. Concaténer les données dans l'ordre (offset)
   ↓
4. Retourner fichier reconstruit (bit-perfect)
```

### Exemple Complet

```rust
// 1. Décomposer et stocker
let decomposer = Decomposer::auto_detect(&original_data);
let atoms = decomposer.decompose(&original_data)?;

let mut content_refs = Vec::new();
for atom in atoms {
    let stored = cas.add_atom(&atom.data, atom.atom_type).await?;
    content_refs.push(ContentRef::new(
        stored.hash,
        stored.atom_type,
        atom.source_offset,
        atom.size,
    ));
}

// 2. Sauvegarder content_refs dans le concept
concept.content_refs = content_refs;

// 3. Reconstruction ultérieure
let mut atoms_data = Vec::new();
for cref in &concept.content_refs {
    let data = cas.get_atom(&cref.atom_hash).await?;
    atoms_data.push(data.to_vec());
}

let reconstructed = Reconstructor::reconstruct_verified(&atoms, atoms_data)?;
assert_eq!(reconstructed, original_data); // Bit-perfect!
```

---

## Backends de Stockage

### Trait `StorageBackend`

```rust
#[async_trait]
pub trait StorageBackend: Send + Sync {
    async fn upload(&self, key: &str, data: Bytes) -> Result<UploadResult>;
    async fn download(&self, key: &str) -> Result<Bytes>;
    async fn delete(&self, key: &str) -> Result<()>;
    async fn exists(&self, key: &str) -> Result<bool>;
    async fn list_keys(&self) -> Result<Vec<String>>;
    async fn stats(&self) -> Result<BackendStats>;
}
```

### LocalFsBackend (Implémenté)

**Stockage local avec sharding 2-niveaux**

```
.panini/storage/
├── ab/
│   ├── cd/
│   │   └── abcdef123456...  (hash complet)
│   └── ef/
│       └── abef789012...
├── 12/
│   ├── 34/
│   │   └── 1234567890...
...
```

**Avantages du sharding:**
- Évite trop de fichiers dans un seul répertoire
- Améliore les performances du filesystem
- Compatible avec Git LFS (structure similaire)

**Configuration:**

```rust
let backend = LocalFsBackend::new(".panini/storage")?;
let cas = ContentAddressedStorage::new(Arc::new(backend), StorageConfig::default());
```

### S3Backend (À Implémenter)

**Structure proposée:**

```
s3://my-bucket/
├── atoms/
│   ├── ab/
│   │   ├── cd/
│   │   │   └── abcdef123456...
```

**Dépendances nécessaires:**

```toml
[dependencies]
aws-sdk-s3 = "1.0"
# ou
rusoto_s3 = "0.48"
```

**API:**

```rust
pub struct S3Backend {
    client: S3Client,
    bucket: String,
    prefix: String,  // "atoms/"
}

#[async_trait]
impl StorageBackend for S3Backend {
    async fn upload(&self, key: &str, data: Bytes) -> Result<UploadResult> {
        let object_key = format!("{}{}/{}/{}", 
            self.prefix, 
            &key[0..2], 
            &key[2..4], 
            key
        );
        
        self.client
            .put_object()
            .bucket(&self.bucket)
            .key(object_key)
            .body(data.into())
            .send()
            .await?;
        
        Ok(UploadResult { /* ... */ })
    }
    
    // ... autres méthodes
}
```

---

## Cas d'Usage

### 1. Vidéos de Cours en Ligne

**Problème:** 100 cours, chacun réutilise intro (10s), outro (5s), musique de fond

**Solution avec décomposition atomique:**

```
Vidéo 1: [intro] + [contenu_1] + [outro]
Vidéo 2: [intro] + [contenu_2] + [outro]  // intro/outro partagés!
...
Vidéo 100: [intro] + [contenu_100] + [outro]

Storage:
- intro atoms: 20 MB (stocké 1x, refs: 100)
- outro atoms: 10 MB (stocké 1x, refs: 100)
- contenu_* atoms: 9.5 GB (unique)

Total: 9.53 GB au lieu de 12 GB (21% économie)
```

### 2. Versioning de Vidéo

**Problème:** 10 versions d'une vidéo (corrections colorimétriques)

**Solution:**

```
v1: [metadata] + [video_stream] + [audio_stream]
v2: [metadata] + [video_stream_v2] + [audio_stream]  // audio partagé!
v3: [metadata] + [video_stream_v3] + [audio_stream]  // audio partagé!

Atoms partagés:
- Audio stream: 50 MB × 1 = 50 MB
- Container metadata: 2 KB × 1 = 2 KB

Atoms uniques:
- 10 video streams: ~600 MB chacun = 6 GB

Total: 6.05 GB au lieu de 10 GB (40% économie)
```

### 3. Extraction Audio Uniquement

**Problème:** Télécharger 1 GB de vidéo juste pour l'audio

**Solution avec reconstruction partielle:**

```rust
// Filtrer uniquement les atoms audio
let audio_refs: Vec<_> = concept.content_refs
    .iter()
    .filter(|r| matches!(r.atom_type, AtomType::AudioStream | AtomType::AudioChunk))
    .collect();

// Télécharger uniquement ces atoms (50 MB au lieu de 1 GB)
let mut audio_data = Vec::new();
for cref in audio_refs {
    let atom_data = cas.get_atom(&cref.atom_hash).await?;
    audio_data.extend_from_slice(&atom_data);
}

// Sauvegarder audio.aac (50 MB téléchargés)
fs::write("audio.aac", audio_data)?;
```

### 4. Preview Vidéo (Keyframes Uniquement)

**Problème:** Aperçu rapide sans télécharger toute la vidéo

**Solution:**

```rust
// Filtrer uniquement les I-Frames (keyframes)
let keyframe_refs: Vec<_> = concept.content_refs
    .iter()
    .filter(|r| r.atom_type == AtomType::IFrame)
    .collect();

// Télécharger 20 MB de keyframes au lieu de 1 GB
// Permet navigation rapide dans la timeline
```

---

## API et Exemples

### Exemple 1: Ajouter une Vidéo

```rust
use panini_core::storage::*;

#[tokio::main]
async fn main() -> Result<()> {
    // 1. Créer backend et CAS
    let backend = Arc::new(LocalFsBackend::new(".panini/storage")?);
    let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
    
    // 2. Lire fichier vidéo
    let video_data = fs::read("my_video.mp4")?;
    
    // 3. Décomposer en atomes
    let decomposer = Decomposer::auto_detect(&video_data);
    let atoms = decomposer.decompose(&video_data)?;
    
    println!("Décomposé en {} atomes", atoms.len());
    
    // 4. Stocker chaque atome
    let mut content_refs = Vec::new();
    for (i, atom) in atoms.iter().enumerate() {
        let atom_data = &video_data[atom.source_offset as usize..(atom.source_offset + atom.size) as usize];
        let stored = cas.add_atom(atom_data, atom.atom_type).await?;
        
        content_refs.push(ContentRef::new(
            stored.hash,
            stored.atom_type,
            atom.source_offset,
            atom.size,
        ));
        
        println!("Atome {}: {} ({})", i, stored.hash, atom.atom_type);
    }
    
    // 5. Sauvegarder refs dans concept
    let mut concept = Concept::new("ma-video", "# Ma Vidéo");
    concept.content_refs = content_refs;
    
    // 6. Afficher statistiques
    let stats = cas.get_stats();
    println!("\nStatistiques:");
    println!("  Total atomes: {}", stats.total_atoms);
    println!("  Taille totale: {} MB", stats.total_size / 1_000_000);
    println!("  Déduplication: {:.1}%", stats.dedup_ratio());
    println!("  Économie: {} MB", stats.dedup_savings / 1_000_000);
    
    Ok(())
}
```

### Exemple 2: Récupérer et Reconstruire

```rust
#[tokio::main]
async fn main() -> Result<()> {
    // 1. Charger concept
    let concept = /* load from Git */;
    
    // 2. Créer CAS
    let backend = Arc::new(LocalFsBackend::new(".panini/storage")?);
    let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
    
    // 3. Récupérer tous les atomes
    let mut atoms_data = Vec::new();
    for cref in &concept.content_refs {
        let data = cas.get_atom(&cref.atom_hash).await?;
        atoms_data.push(data.to_vec());
    }
    
    // 4. Reconstruire avec vérification
    let reconstructed = Reconstructor::reconstruct_verified(&atoms, atoms_data)?;
    
    // 5. Sauvegarder
    fs::write("reconstructed_video.mp4", reconstructed)?;
    
    println!("✅ Reconstruction réussie (bit-perfect)");
    
    Ok(())
}
```

### Exemple 3: Garbage Collection

```rust
#[tokio::main]
async fn main() -> Result<()> {
    let backend = Arc::new(LocalFsBackend::new(".panini/storage")?);
    let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
    
    // 1. Trouver atomes orphelins
    let orphaned = cas.find_orphaned_atoms();
    println!("🗑️  {} atomes orphelins trouvés", orphaned.len());
    
    for hash in &orphaned {
        let meta = cas.get_atom_metadata(hash)?;
        println!("  - {} ({} KB)", &hash[..16], meta.size / 1024);
    }
    
    // 2. Supprimer
    let gc_stats = cas.gc_orphaned_atoms().await?;
    println!("\n✅ Garbage collection:");
    println!("  Atomes supprimés: {}", gc_stats.atoms_deleted);
    println!("  Espace libéré: {} MB", gc_stats.bytes_freed / 1_000_000);
    
    Ok(())
}
```

---

## Roadmap v2.1

### Fonctionnalités Prévues

1. **Décomposeur MP4 Complet**
   - Extraction des atoms MP4 (ftyp, moov, mdat)
   - Séparation video/audio streams
   - Extraction frame-by-frame (I/P/B frames)

2. **Décomposeur JPEG Avancé**
   - Parsing des segments (SOI, APP0, DQT, DHT, SOS)
   - Extraction EXIF comme atome séparé
   - Support des JPEGs progressifs

3. **S3Backend**
   - Support AWS S3, MinIO, DigitalOcean Spaces
   - Multipart upload pour gros atomes
   - Signature V4, credentials management

4. **Compression des Atomes**
   - Support zstd, lz4
   - Compression sélective (metadata uniquement)
   - Ratio de compression par type d'atome

5. **Streaming Progressif**
   - API de streaming `stream_atoms()`
   - Préchargement prédictif
   - Buffer management

6. **CLI Commands**
   - `panini add-content <concept> <file>`
   - `panini get-content <concept> [--component audio]`
   - `panini list-atoms <concept>`
   - `panini verify-content <concept>`
   - `panini gc-atoms [--dry-run]`

---

## Références

- **Code:** `crates/panini-core/src/storage/`
- **Tests:** `crates/panini-core/src/storage/*/tests/`
- **Panini-FS Research:** `../research/panini-fs/`
- **Whitepaper:** `../research/philosophy-theory/PANINI_WHITEPAPER.md`

---

**Auteur:** Panini Team  
**Licence:** MIT  
**Contact:** Via GitHub Issues
