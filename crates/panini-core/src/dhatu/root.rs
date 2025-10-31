//! Sanskrit Dhātu (Root) System
//!
//! Dhātus are the fundamental verbal roots in Sanskrit grammar.
//! Each carries semantic and emotional resonance.

use serde::{Deserialize, Serialize};
use super::emotion::PankseppEmotion;
use std::collections::HashMap;

/// Sanskrit verbal root (dhātu)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DhatuRoot {
    /// Root in IAST transliteration
    pub root: String,
    
    /// Devanagari script
    pub devanagari: String,
    
    /// Primary meaning
    pub meaning: String,
    
    /// Associated Panksepp emotion
    pub emotion: PankseppEmotion,
    
    /// Emotional intensity (0.0 - 1.0)
    pub intensity: f64,
    
    /// Secondary meanings
    pub secondary_meanings: Vec<String>,
    
    /// Example words derived from this root
    pub derived_words: Vec<String>,
    
    /// Optional metadata
    #[serde(default)]
    pub metadata: HashMap<String, String>,
}

impl DhatuRoot {
    pub fn new(
        root: impl Into<String>,
        devanagari: impl Into<String>,
        meaning: impl Into<String>,
        emotion: PankseppEmotion,
        intensity: f64,
    ) -> Self {
        Self {
            root: root.into(),
            devanagari: devanagari.into(),
            meaning: meaning.into(),
            emotion,
            intensity: intensity.clamp(0.0, 1.0),
            secondary_meanings: Vec::new(),
            derived_words: Vec::new(),
            metadata: HashMap::new(),
        }
    }
    
    pub fn with_secondary(mut self, meanings: Vec<String>) -> Self {
        self.secondary_meanings = meanings;
        self
    }
    
    pub fn with_derived(mut self, words: Vec<String>) -> Self {
        self.derived_words = words;
        self
    }
}

/// Collection of canonical dhātu roots
pub struct DhatuCatalog {
    roots: HashMap<String, DhatuRoot>,
}

impl DhatuCatalog {
    pub fn new() -> Self {
        let mut catalog = Self {
            roots: HashMap::new(),
        };
        catalog.load_canonical_roots();
        catalog
    }
    
    /// Load canonical Sanskrit roots with emotional mapping
    fn load_canonical_roots(&mut self) {
        // SEEKING roots
        self.add(DhatuRoot::new(
            "iṣ", "इष्", "to desire, to wish", 
            PankseppEmotion::Seeking, 0.9
        ).with_derived(vec!["icchā".into(), "īṣṭa".into()]));
        
        self.add(DhatuRoot::new(
            "eṣ", "एष्", "to seek, to search", 
            PankseppEmotion::Seeking, 0.85
        ));
        
        self.add(DhatuRoot::new(
            "gav", "गव्", "to desire, to strive", 
            PankseppEmotion::Seeking, 0.8
        ));
        
        // FEAR roots
        self.add(DhatuRoot::new(
            "bhī", "भी", "to fear, to be afraid", 
            PankseppEmotion::Fear, 0.95
        ).with_derived(vec!["bhaya".into(), "bhīti".into()]));
        
        self.add(DhatuRoot::new(
            "tras", "त्रस्", "to tremble, to be frightened", 
            PankseppEmotion::Fear, 0.85
        ).with_derived(vec!["trāsa".into(), "trasta".into()]));
        
        // RAGE roots
        self.add(DhatuRoot::new(
            "krudh", "क्रुध्", "to be angry", 
            PankseppEmotion::Rage, 0.95
        ).with_derived(vec!["krodha".into(), "kruddha".into()]));
        
        self.add(DhatuRoot::new(
            "man", "मन्", "to be angry, to resent", 
            PankseppEmotion::Rage, 0.8
        ).with_derived(vec!["manyū".into(), "manyate".into()]));
        
        // LUST roots
        self.add(DhatuRoot::new(
            "kam", "कम्", "to desire, to love", 
            PankseppEmotion::Lust, 0.9
        ).with_derived(vec!["kāma".into(), "kānti".into()]));
        
        self.add(DhatuRoot::new(
            "ram", "रम्", "to delight, to enjoy", 
            PankseppEmotion::Lust, 0.85
        ).with_derived(vec!["rati".into(), "ramana".into()]));
        
        // CARE roots
        self.add(DhatuRoot::new(
            "kṛp", "कृप्", "to compassionate, to pity", 
            PankseppEmotion::Care, 0.95
        ).with_derived(vec!["karuṇā".into(), "kṛpā".into()]));
        
        self.add(DhatuRoot::new(
            "snih", "स्निह्", "to be affectionate", 
            PankseppEmotion::Care, 0.9
        ).with_derived(vec!["sneha".into(), "snigdha".into()]));
        
        // PANIC/GRIEF roots
        self.add(DhatuRoot::new(
            "śuc", "शुच्", "to grieve, to mourn", 
            PankseppEmotion::PanicGrief, 0.95
        ).with_derived(vec!["śoka".into(), "śucita".into()]));
        
        self.add(DhatuRoot::new(
            "viṣad", "विषद्", "to despond, to be dejected", 
            PankseppEmotion::PanicGrief, 0.9
        ).with_derived(vec!["viṣāda".into(), "viṣaṇṇa".into()]));
        
        // PLAY roots
        self.add(DhatuRoot::new(
            "krīḍ", "क्रीड्", "to play, to sport", 
            PankseppEmotion::Play, 0.95
        ).with_derived(vec!["krīḍā".into(), "krīḍita".into()]));
        
        self.add(DhatuRoot::new(
            "līl", "लील्", "to play, to sport freely", 
            PankseppEmotion::Play, 0.9
        ).with_derived(vec!["līlā".into(), "līlita".into()]));
    }
    
    fn add(&mut self, root: DhatuRoot) {
        self.roots.insert(root.root.clone(), root);
    }
    
    pub fn get(&self, root: &str) -> Option<&DhatuRoot> {
        self.roots.get(root)
    }
    
    pub fn get_by_emotion(&self, emotion: PankseppEmotion) -> Vec<&DhatuRoot> {
        self.roots.values()
            .filter(|r| r.emotion == emotion)
            .collect()
    }
    
    pub fn all(&self) -> Vec<&DhatuRoot> {
        self.roots.values().collect()
    }
    
    pub fn search(&self, query: &str) -> Vec<&DhatuRoot> {
        let query_lower = query.to_lowercase();
        self.roots.values()
            .filter(|r| {
                r.root.to_lowercase().contains(&query_lower)
                    || r.meaning.to_lowercase().contains(&query_lower)
                    || r.secondary_meanings.iter()
                        .any(|m| m.to_lowercase().contains(&query_lower))
            })
            .collect()
    }
}

impl Default for DhatuCatalog {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dhatu_catalog() {
        let catalog = DhatuCatalog::new();
        assert!(!catalog.all().is_empty());
        
        let seeking_roots = catalog.get_by_emotion(PankseppEmotion::Seeking);
        assert!(!seeking_roots.is_empty());
    }

    #[test]
    fn test_dhatu_search() {
        let catalog = DhatuCatalog::new();
        let results = catalog.search("desire");
        assert!(!results.is_empty());
    }
}
