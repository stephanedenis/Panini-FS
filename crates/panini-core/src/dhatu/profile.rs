//! Emotional Profile System
//!
//! Track emotional characteristics of files, directories, and projects

use super::emotion::{EmotionalIntensity, PankseppEmotion};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use chrono::{DateTime, Utc};

/// Emotional profile for a file or directory
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EmotionalProfile {
    /// File or directory path
    pub path: String,
    
    /// Content hash (SHA-256)
    pub content_hash: Option<String>,
    
    /// Emotional intensity scores
    pub intensity: EmotionalIntensity,
    
    /// Dominant emotion
    pub dominant_emotion: Option<PankseppEmotion>,
    
    /// Classification confidence (0.0 - 1.0)
    pub confidence: f64,
    
    /// Manual tags added by user
    pub manual_tags: Vec<String>,
    
    /// Dhātu roots associated
    pub dhatu_roots: Vec<String>,
    
    /// Timestamp of classification
    pub classified_at: DateTime<Utc>,
    
    /// Optional metadata
    #[serde(default)]
    pub metadata: HashMap<String, String>,
}

impl EmotionalProfile {
    pub fn new(path: String, intensity: EmotionalIntensity) -> Self {
        let dominant_emotion = intensity.dominant();
        let confidence = if let Some(emotion) = dominant_emotion {
            intensity.get(emotion)
        } else {
            0.0
        };
        
        Self {
            path,
            content_hash: None,
            intensity,
            dominant_emotion,
            confidence,
            manual_tags: Vec::new(),
            dhatu_roots: Vec::new(),
            classified_at: Utc::now(),
            metadata: HashMap::new(),
        }
    }
    
    pub fn with_hash(mut self, hash: String) -> Self {
        self.content_hash = Some(hash);
        self
    }
    
    pub fn with_tags(mut self, tags: Vec<String>) -> Self {
        self.manual_tags = tags;
        self
    }
    
    pub fn with_roots(mut self, roots: Vec<String>) -> Self {
        self.dhatu_roots = roots;
        self
    }
    
    pub fn add_tag(&mut self, tag: String) {
        if !self.manual_tags.contains(&tag) {
            self.manual_tags.push(tag);
        }
    }
    
    pub fn add_root(&mut self, root: String) {
        if !self.dhatu_roots.contains(&root) {
            self.dhatu_roots.push(root);
        }
    }
}

/// Resonance between two emotional profiles
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EmotionalResonance {
    /// Path A
    pub path_a: String,
    
    /// Path B
    pub path_b: String,
    
    /// Resonance score (0.0 - 1.0)
    pub score: f64,
    
    /// Shared emotions
    pub shared_emotions: Vec<PankseppEmotion>,
    
    /// Resonance type
    pub resonance_type: ResonanceType,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum ResonanceType {
    /// Both have similar dominant emotion
    Harmonic,
    
    /// Complementary emotions (e.g., SEEKING + CARE)
    Complementary,
    
    /// Opposing emotions (e.g., RAGE + CARE)
    Dissonant,
}

impl EmotionalResonance {
    /// Calculate resonance between two profiles
    pub fn calculate(a: &EmotionalProfile, b: &EmotionalProfile) -> Self {
        let mut score = 0.0;
        let mut shared_emotions = Vec::new();
        
        // Calculate cosine similarity of intensity vectors
        for emotion in PankseppEmotion::all() {
            let a_val = a.intensity.get(emotion);
            let b_val = b.intensity.get(emotion);
            
            if a_val > 0.0 && b_val > 0.0 {
                shared_emotions.push(emotion);
            }
            
            score += a_val * b_val;
        }
        
        // Normalize
        let a_norm = a.intensity.arousal();
        let b_norm = b.intensity.arousal();
        if a_norm > 0.0 && b_norm > 0.0 {
            score /= (a_norm * b_norm).sqrt();
        }
        
        // Determine resonance type
        let resonance_type = if a.dominant_emotion == b.dominant_emotion {
            ResonanceType::Harmonic
        } else if score > 0.5 {
            ResonanceType::Complementary
        } else {
            ResonanceType::Dissonant
        };
        
        Self {
            path_a: a.path.clone(),
            path_b: b.path.clone(),
            score: score.clamp(0.0, 1.0),
            shared_emotions,
            resonance_type,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_emotional_profile() {
        let mut intensity = EmotionalIntensity::new();
        intensity.set(PankseppEmotion::Seeking, 0.8);
        
        let profile = EmotionalProfile::new("/test/file.rs".to_string(), intensity);
        
        assert_eq!(profile.dominant_emotion, Some(PankseppEmotion::Seeking));
        assert_eq!(profile.confidence, 0.8);
    }

    #[test]
    fn test_resonance() {
        let mut intensity_a = EmotionalIntensity::new();
        intensity_a.set(PankseppEmotion::Seeking, 0.8);
        let profile_a = EmotionalProfile::new("/a".to_string(), intensity_a);
        
        let mut intensity_b = EmotionalIntensity::new();
        intensity_b.set(PankseppEmotion::Seeking, 0.7);
        let profile_b = EmotionalProfile::new("/b".to_string(), intensity_b);
        
        let resonance = EmotionalResonance::calculate(&profile_a, &profile_b);
        
        assert_eq!(resonance.resonance_type, ResonanceType::Harmonic);
        assert!(resonance.score > 0.0);
    }
}
