# 🎨 Phase 9: Classification Dhātu - Planification

**Date:** 31 Octobre 2025  
**Statut:** 📋 Planning & Design Phase  
**Dépendances:** Phase 8 FUSE (optionnel), Phase 7 API ✅  

---

## 🌟 Vision: Système Dhātu

Intégrer le **système de classification émotionnelle Dhātu** de Pāṇini dans le filesystem, permettant de :

- 🎭 **Classifier les fichiers** par affect émotionnel
- 🏷️ **Tags sémantiques** basés sur le modèle de Panksepp
- 🔍 **Requêtes expressives** par émotion/intention
- 🧠 **Analyse affective** du contenu
- 🌈 **Navigation par résonance** émotionnelle

---

## 📚 Fondements Théoriques

### Système Panksepp (7 émotions primaires)

```
SEEKING (Recherche)    → Curiosité, exploration, anticipation
FEAR (Peur)            → Anxiété, vigilance, évitement
RAGE (Rage)            → Colère, frustration, défense
LUST (Désir)           → Attraction, liaison, connexion
CARE (Soin)            → Nurturance, empathie, protection
PANIC/GRIEF (Panique)  → Séparation, perte, détresse
PLAY (Jeu)             → Ludique, créatif, social
```

### Extension Dhātu (Racines Sanskrites)

Chaque fichier/concept possède une ou plusieurs **racines Dhātu** qui définissent sa nature affective :

```
√BHŪ  (devenir)     → Transformation, émergence
√KṚ   (faire)       → Création, action
√JÑĀ  (connaître)   → Cognition, compréhension
√STHĀ (se tenir)    → Stabilité, présence
√GAM  (aller)       → Mouvement, progression
√DAD  (donner)      → Générosité, partage
√SMAR (se souvenir) → Mémoire, réminiscence
```

---

## 🎯 Objectifs Phase 9

### 9.1: Modèle de Données Dhātu
- [ ] Définir structure `DhatuTag`
- [ ] Créer taxonomie des émotions Panksepp
- [ ] Mapper racines sanskrites → affects
- [ ] Système de scoring affectif (0.0-1.0)

### 9.2: Classification Automatique
- [ ] Analyser contenu textuel pour indices émotionnels
- [ ] NLP basique pour extraction de sentiment
- [ ] Heuristiques pour types de fichiers
- [ ] ML (optionnel) pour classification avancée

### 9.3: API Dhātu
- [ ] Endpoints REST pour tags émotionnels
- [ ] Requêtes par affect: `GET /api/dhatu/search?emotion=SEEKING`
- [ ] Statistiques affectives: `GET /api/dhatu/stats`
- [ ] Suggestions de tags: `POST /api/dhatu/suggest`

### 9.4: Interface FUSE Dhātu
- [ ] Répertoire `/dhatu/` dans filesystem
- [ ] Navigation par émotion: `/dhatu/SEEKING/`, `/dhatu/CARE/`
- [ ] Filtres combinés: `/dhatu/SEEKING+PLAY/`
- [ ] Liens symboliques vers fichiers classifiés

### 9.5: Visualisation Web
- [ ] Dashboard Dhātu avec graphiques émotionnels
- [ ] Radar chart des 7 émotions
- [ ] Timeline affective
- [ ] Heatmap de résonance

---

## 🏗️ Architecture Proposée

### Structure des Crates

```
Panini-FS/
├── crates/
│   ├── panini-core/
│   │   └── src/
│   │       └── dhatu/              (NOUVEAU)
│   │           ├── mod.rs
│   │           ├── emotion.rs      ← Modèle Panksepp
│   │           ├── root.rs         ← Racines sanskrites
│   │           ├── classifier.rs   ← Classification automatique
│   │           └── scorer.rs       ← Scoring affectif
│   │
│   ├── panini-api/
│   │   └── src/
│   │       └── dhatu_handlers.rs   (NOUVEAU)
│   │
│   └── panini-fuse/
│       └── src/
│           └── dhatu_fs.rs         (NOUVEAU)
```

### Modèle de Données

```rust
// crates/panini-core/src/dhatu/emotion.rs

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum PankseppEmotion {
    Seeking,
    Fear,
    Rage,
    Lust,
    Care,
    PanicGrief,
    Play,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DhatuRoot {
    pub sanskrit: String,      // "√BHŪ"
    pub transliteration: String, // "bhū"
    pub meaning: String,       // "devenir"
    pub emotion: PankseppEmotion,
    pub intensity: f32,        // 0.0 - 1.0
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DhatuTag {
    pub roots: Vec<DhatuRoot>,
    pub primary_emotion: PankseppEmotion,
    pub emotional_profile: EmotionalProfile,
    pub confidence: f32,
    pub classified_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EmotionalProfile {
    pub seeking: f32,
    pub fear: f32,
    pub rage: f32,
    pub lust: f32,
    pub care: f32,
    pub panic_grief: f32,
    pub play: f32,
}

impl EmotionalProfile {
    pub fn dominant(&self) -> PankseppEmotion {
        // Retourne l'émotion avec le score le plus élevé
    }
    
    pub fn resonance(&self, other: &EmotionalProfile) -> f32 {
        // Calcule la similarité entre deux profils (cosine similarity)
    }
}
```

### API Endpoints

```rust
// GET /api/dhatu/emotions - Liste des émotions supportées
// Response: { "emotions": ["SEEKING", "FEAR", ...] }

// GET /api/dhatu/roots - Liste des racines sanskrites
// Response: { "roots": [{"sanskrit": "√BHŪ", "meaning": "devenir", ...}, ...] }

// POST /api/dhatu/classify - Classifier un fichier
// Request: { "content": "...", "filename": "..." }
// Response: { "tag": {...}, "confidence": 0.85 }

// GET /api/dhatu/search?emotion=SEEKING&threshold=0.5
// Response: { "files": [...], "total": 42 }

// GET /api/dhatu/stats - Statistiques affectives globales
// Response: { "distribution": {...}, "most_common": "SEEKING" }

// GET /api/dhatu/resonance/:hash1/:hash2
// Response: { "similarity": 0.73, "shared_roots": [...] }
```

### Filesystem Dhātu

```
/mnt/panini-fs/
└── dhatu/
    ├── emotions/
    │   ├── SEEKING/
    │   │   ├── file1.txt -> ../../concepts/.../file1.txt
    │   │   └── file2.md  -> ../../concepts/.../file2.md
    │   ├── CARE/
    │   ├── PLAY/
    │   └── ...
    │
    ├── roots/
    │   ├── BHU/          (√BHŪ - devenir)
    │   ├── KR/           (√KṚ - faire)
    │   └── ...
    │
    ├── profiles/
    │   ├── contemplative/  (high SEEKING, low RAGE)
    │   ├── nurturing/      (high CARE, low FEAR)
    │   └── dynamic/        (high PLAY, high SEEKING)
    │
    └── resonance/
        └── <file-hash>/
            └── similar/    (fichiers avec profil similaire)
```

---

## 🧠 Classification Automatique

### Heuristiques de Base

#### Par Type de Fichier
```rust
match file_extension {
    "md" | "txt" | "rst" => {
        // Analyser contenu textuel
        if contains_questions() => SEEKING + 0.7
        if contains_exclamations() => RAGE or PLAY
        if contains_empathy_words() => CARE + 0.6
    }
    "rs" | "py" | "js" => {
        // Code = création
        SEEKING + 0.8  // Exploration technique
        PLAY + 0.5     // Créativité
    }
    "jpg" | "png" => {
        // Images = expression visuelle
        PLAY + 0.6
        LUST + 0.4  // Attraction esthétique
    }
}
```

#### Par Contenu Textuel

**Keywords Émotionnels:**
```rust
SEEKING: ["recherche", "explorer", "découvrir", "pourquoi", "comment"]
FEAR: ["danger", "risque", "attention", "prudent", "éviter"]
RAGE: ["erreur", "bug", "frustrant", "FIXME", "TODO"]
CARE: ["aide", "support", "guide", "tutoriel", "explication"]
PLAY: ["fun", "créatif", "expérience", "test", "prototype"]
```

### NLP Avancé (Phase 9.2+)

```rust
use sentencepiece; // Tokenization
use onnx_runtime;  // ML inference

pub struct DhatuClassifier {
    tokenizer: SentencePieceProcessor,
    model: OnnxModel,
}

impl DhatuClassifier {
    pub fn classify(&self, text: &str) -> EmotionalProfile {
        let tokens = self.tokenizer.encode(text);
        let embeddings = self.model.infer(tokens);
        
        EmotionalProfile {
            seeking: embeddings[0],
            fear: embeddings[1],
            rage: embeddings[2],
            lust: embeddings[3],
            care: embeddings[4],
            panic_grief: embeddings[5],
            play: embeddings[6],
        }
    }
}
```

---

## 🎨 Visualisation Web

### Dashboard Dhātu

**Page:** `http://localhost:5173/dhatu-dashboard`

**Features:**
- 📊 **Radar Chart:** 7 émotions Panksepp
- 🔥 **Heatmap:** Résonance entre fichiers
- 📈 **Timeline:** Évolution affective dans le temps
- 🏷️ **Tag Cloud:** Racines sanskrites les plus utilisées
- 🔍 **Search:** Recherche par profil émotionnel

**Composants React:**
```typescript
// EmotionalRadarChart.tsx
interface RadarData {
    seeking: number;
    fear: number;
    rage: number;
    lust: number;
    care: number;
    panicGrief: number;
    play: number;
}

// ResonanceHeatmap.tsx
interface ResonanceCell {
    fileA: string;
    fileB: string;
    similarity: number;
}

// DhatuTimeline.tsx
interface EmotionalEvent {
    timestamp: Date;
    emotion: PankseppEmotion;
    intensity: number;
}
```

---

## 🧪 Use Cases

### Use Case 1: Trouver du Contenu Créatif
```bash
# API
curl "http://localhost:3000/api/dhatu/search?emotion=PLAY&threshold=0.7"

# FUSE
ls /mnt/panini-fs/dhatu/emotions/PLAY/
```

### Use Case 2: Analyser un Nouveau Fichier
```bash
# Upload et classification automatique
curl -F "file=@article.md" http://localhost:3000/api/dhatu/classify

# Response:
{
  "tag": {
    "primary_emotion": "SEEKING",
    "emotional_profile": {
      "seeking": 0.85,
      "play": 0.4,
      "care": 0.3,
      ...
    },
    "roots": [
      {"sanskrit": "√JÑĀ", "meaning": "connaître", "intensity": 0.8}
    ]
  }
}
```

### Use Case 3: Trouver des Fichiers Similaires
```bash
# Par résonance émotionnelle
curl "http://localhost:3000/api/dhatu/resonance/<hash1>/<hash2>"

# FUSE
ls /mnt/panini-fs/dhatu/resonance/<hash>/similar/
```

### Use Case 4: Profils Personnalisés
```bash
# Créer un profil "contemplative"
curl -X POST http://localhost:3000/api/dhatu/profiles \
  -d '{"name": "contemplative", "weights": {"seeking": 0.9, "rage": 0.1}}'

# Recherche par profil
ls /mnt/panini-fs/dhatu/profiles/contemplative/
```

---

## 📊 Métriques Phase 9

### Code Estimé
- **panini-core/dhatu/**: ~500 lignes
  - emotion.rs: ~100 lignes
  - root.rs: ~80 lignes
  - classifier.rs: ~200 lignes
  - scorer.rs: ~120 lignes

- **panini-api/dhatu_handlers.rs**: ~300 lignes
  - 6 nouveaux endpoints

- **panini-fuse/dhatu_fs.rs**: ~250 lignes
  - Génération arbre /dhatu/
  - Navigation par émotion

- **Frontend React**: ~800 lignes
  - EmotionalRadarChart: ~200 lignes
  - ResonanceHeatmap: ~250 lignes
  - DhatuTimeline: ~200 lignes
  - DhatuSearch: ~150 lignes

**Total Estimé:** ~1,850 lignes

### Endpoints API
- 6 nouveaux endpoints Dhātu
- Total API: 11 endpoints (5 dedup + 6 dhatu)

### Répertoires FUSE
- `/dhatu/emotions/` (7 sous-répertoires)
- `/dhatu/roots/` (20+ racines sanskrites)
- `/dhatu/profiles/` (customizable)
- `/dhatu/resonance/` (dynamique)

---

## 🎯 Roadmap Détaillée

### Phase 9.1: Fondations (3-4h)
- [x] Planification complète
- [ ] Créer module `dhatu` dans panini-core
- [ ] Implémenter `PankseppEmotion` enum
- [ ] Implémenter `DhatuRoot` struct
- [ ] Implémenter `EmotionalProfile`
- [ ] Tests unitaires

### Phase 9.2: Classification (4-5h)
- [ ] Classifier basique par type de fichier
- [ ] Keywords émotionnels
- [ ] Analyse de contenu textuel
- [ ] Scoring heuristique
- [ ] Tests avec fichiers réels

### Phase 9.3: API (3-4h)
- [ ] 6 endpoints Dhātu
- [ ] Handlers dans panini-api
- [ ] Intégration avec CAS
- [ ] Tests curl

### Phase 9.4: FUSE (4-5h)
- [ ] Génération arbre `/dhatu/`
- [ ] Navigation par émotion
- [ ] Symlinks vers fichiers
- [ ] Tests mount/ls

### Phase 9.5: Web UI (5-6h)
- [ ] Radar chart Recharts
- [ ] Heatmap de résonance
- [ ] Timeline affective
- [ ] Search par profil
- [ ] Intégration avec API

### Phase 9.6: Documentation (2h)
- [ ] Guide d'utilisation Dhātu
- [ ] Exemples de classification
- [ ] API reference
- [ ] Philosophie du système

**Total Estimé:** 21-26 heures

---

## 🌟 Philosophie Dhātu

> "Chaque fichier possède une essence émotionnelle, une résonance affective qui transcende son contenu binaire. Le système Dhātu permet de naviguer non pas par structure logique, mais par résonance émotionnelle."

### Principes Fondamentaux

1. **Affect > Structure**
   - La classification émotionnelle complète (mais ne remplace pas) la hiérarchie traditionnelle

2. **Résonance > Similarité**
   - Les fichiers sont liés par affinité émotionnelle, pas seulement par contenu

3. **Intention > Fonction**
   - Un fichier est défini par l'intention qui l'a créé

4. **Dhātu comme Racine**
   - Les racines sanskrites capturent l'essence verbale de l'action/émotion

---

## 🎉 Vision Finale

Imaginez:

```bash
# Trouver tous les fichiers créatifs et ludiques
ls /mnt/panini-fs/dhatu/profiles/creative/

# Comparer la résonance entre deux documents
panini-dhatu compare article1.md article2.md
# Output: 73% emotional resonance (shared: SEEKING, PLAY)

# Timeline de mon humeur à travers mes fichiers
panini-dhatu timeline --from 2025-10-01 --to 2025-10-31
# Output: Graph ASCII montrant l'évolution des émotions

# Recommandations basées sur mon état actuel
panini-dhatu recommend --feeling SEEKING+CARE
# Output: Liste de fichiers qui résonnent avec cet état
```

**Phase 9 = Panini-FS devient un système de fichiers conscient de l'affect !** 🎨🧠✨

---

**Statut:** 📋 Plan Complet  
**Prêt pour:** Implémentation après Phase 8  
**Estimation:** 1,850 lignes de code, 21-26h  
**Dépendances:** Phase 7 ✅, Phase 8 (optionnel)
