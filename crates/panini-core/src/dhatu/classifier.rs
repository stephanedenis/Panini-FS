//! Emotional Classification System
//!
//! Automatically classify files and content by emotional resonance

use super::emotion::{EmotionalIntensity, PankseppEmotion};
use super::root::{DhatuCatalog, DhatuRoot};
use anyhow::Result;
use std::path::Path;

/// Emotional classifier for files and content
pub struct DhatuClassifier {
    catalog: DhatuCatalog,
    keywords: KeywordMap,
}

/// Keyword mapping for emotional classification
struct KeywordMap {
    seeking: Vec<String>,
    fear: Vec<String>,
    rage: Vec<String>,
    lust: Vec<String>,
    care: Vec<String>,
    panic_grief: Vec<String>,
    play: Vec<String>,
}

impl KeywordMap {
    fn new() -> Self {
        Self {
            seeking: vec![
                "explore", "discover", "search", "quest", "adventure", "curiosity",
                "goal", "achieve", "progress", "develop", "create", "build",
                "research", "investigate", "analyze", "study", "learn",
            ].into_iter().map(String::from).collect(),
            
            fear: vec![
                "danger", "threat", "risk", "unsafe", "warning", "alert",
                "security", "vulnerability", "attack", "defense", "protect",
                "caution", "careful", "anxious", "worry", "concern",
            ].into_iter().map(String::from).collect(),
            
            rage: vec![
                "angry", "frustrate", "annoy", "irritate", "conflict", "fight",
                "battle", "war", "aggressive", "hostile", "attack", "destroy",
                "hate", "rage", "furious", "mad",
            ].into_iter().map(String::from).collect(),
            
            lust: vec![
                "desire", "want", "passion", "love", "romantic", "intimate",
                "sexual", "erotic", "pleasure", "sensual", "attraction",
                "beautiful", "gorgeous", "sexy",
            ].into_iter().map(String::from).collect(),
            
            care: vec![
                "care", "nurture", "support", "help", "assist", "compassion",
                "kindness", "gentle", "tender", "protect", "guardian",
                "parent", "child", "family", "community", "together",
            ].into_iter().map(String::from).collect(),
            
            panic_grief: vec![
                "sad", "grief", "loss", "mourn", "sorrow", "pain",
                "alone", "lonely", "isolate", "separate", "miss", "absence",
                "cry", "tears", "despair", "depression", "melancholy",
            ].into_iter().map(String::from).collect(),
            
            play: vec![
                "play", "fun", "game", "joy", "happy", "laugh",
                "entertainment", "enjoy", "party", "celebrate", "festival",
                "humor", "joke", "comedy", "silly", "playful",
            ].into_iter().map(String::from).collect(),
        }
    }
    
    fn get(&self, emotion: PankseppEmotion) -> &Vec<String> {
        match emotion {
            PankseppEmotion::Seeking => &self.seeking,
            PankseppEmotion::Fear => &self.fear,
            PankseppEmotion::Rage => &self.rage,
            PankseppEmotion::Lust => &self.lust,
            PankseppEmotion::Care => &self.care,
            PankseppEmotion::PanicGrief => &self.panic_grief,
            PankseppEmotion::Play => &self.play,
        }
    }
}

impl DhatuClassifier {
    pub fn new() -> Self {
        Self {
            catalog: DhatuCatalog::new(),
            keywords: KeywordMap::new(),
        }
    }
    
    /// Classify content by emotional resonance
    pub fn classify_content(&self, content: &str) -> EmotionalIntensity {
        let content_lower = content.to_lowercase();
        let mut intensity = EmotionalIntensity::new();
        
        // Count keyword matches for each emotion
        for emotion in PankseppEmotion::all() {
            let keywords = self.keywords.get(emotion);
            let matches = keywords.iter()
                .filter(|kw| content_lower.contains(kw.as_str()))
                .count();
            
            // Normalize by content length and keyword count
            let score = (matches as f64 / keywords.len() as f64)
                .min(1.0);
            
            intensity.set(emotion, score);
        }
        
        intensity
    }
    
    /// Classify file by name, extension, and path
    pub fn classify_file(&self, path: &Path) -> EmotionalIntensity {
        let mut intensity = EmotionalIntensity::new();
        
        // Extract components
        let filename = path.file_name()
            .and_then(|n| n.to_str())
            .unwrap_or("");
        let extension = path.extension()
            .and_then(|e| e.to_str())
            .unwrap_or("");
        let path_str = path.to_str().unwrap_or("");
        
        let combined = format!("{} {} {}", filename, extension, path_str)
            .to_lowercase();
        
        // File type heuristics
        match extension {
            // Code/development -> SEEKING
            "rs" | "py" | "js" | "ts" | "java" | "c" | "cpp" | "go" => {
                intensity.set(PankseppEmotion::Seeking, 0.7);
            }
            
            // Security/crypto -> FEAR
            "key" | "cert" | "pem" | "sec" => {
                intensity.set(PankseppEmotion::Fear, 0.8);
            }
            
            // Logs/errors -> RAGE
            "log" | "err" => {
                if combined.contains("error") || combined.contains("fail") {
                    intensity.set(PankseppEmotion::Rage, 0.6);
                }
            }
            
            // Media -> PLAY or LUST
            "jpg" | "png" | "gif" | "mp4" | "mp3" | "wav" => {
                intensity.set(PankseppEmotion::Play, 0.5);
            }
            
            // Docs -> CARE (knowledge sharing)
            "md" | "txt" | "pdf" | "doc" => {
                intensity.set(PankseppEmotion::Care, 0.4);
            }
            
            _ => {}
        }
        
        // Path-based classification
        if combined.contains("test") || combined.contains("spec") {
            intensity.set(PankseppEmotion::Seeking, 0.6);
        }
        
        if combined.contains("backup") || combined.contains("archive") {
            intensity.set(PankseppEmotion::Care, 0.7);
        }
        
        if combined.contains("tmp") || combined.contains("cache") {
            intensity.set(PankseppEmotion::Fear, 0.3);
        }
        
        intensity
    }
    
    /// Get dhātu roots for a given emotion
    pub fn get_roots(&self, emotion: PankseppEmotion) -> Vec<&DhatuRoot> {
        self.catalog.get_by_emotion(emotion)
    }
    
    /// Search for dhātu roots
    pub fn search_roots(&self, query: &str) -> Vec<&DhatuRoot> {
        self.catalog.search(query)
    }
}

impl Default for DhatuClassifier {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_classify_content() {
        let classifier = DhatuClassifier::new();
        
        let text = "We are exploring new discoveries with curiosity and research";
        let intensity = classifier.classify_content(text);
        
        assert!(intensity.seeking > 0.0);
        assert_eq!(intensity.dominant(), Some(PankseppEmotion::Seeking));
    }

    #[test]
    fn test_classify_file() {
        let classifier = DhatuClassifier::new();
        
        let path = Path::new("/home/user/project/src/main.rs");
        let intensity = classifier.classify_file(path);
        
        assert!(intensity.seeking > 0.0);
    }
}
