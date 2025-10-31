//! Panksepp Emotional System
//!
//! Based on Jaak Panksepp's affective neuroscience research.
//! Seven primary emotional systems found across all mammals.

use serde::{Deserialize, Serialize};
use std::fmt;

/// Panksepp's seven primary emotional systems
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum PankseppEmotion {
    /// SEEKING: Exploration, curiosity, desire, dopamine-driven
    /// Sanskrit: icchā (इच्छा), kāṅkṣā (काङ्क्षा)
    Seeking,
    
    /// FEAR: Anxiety, vigilance, freezing, flight
    /// Sanskrit: bhaya (भय), bhīti (भीति)
    Fear,
    
    /// RAGE: Anger, frustration, irritation, assertion
    /// Sanskrit: krodha (क्रोध), manyū (मन्यू)
    Rage,
    
    /// LUST: Sexual desire, erotic arousal, reproduction
    /// Sanskrit: kāma (काम), rati (रति)
    Lust,
    
    /// CARE: Nurturing, compassion, maternal instinct, bonding
    /// Sanskrit: karuṇā (करुणा), sneha (स्नेह)
    Care,
    
    /// PANIC/GRIEF: Separation distress, loneliness, sadness
    /// Sanskrit: śoka (शोक), viṣāda (विषाद)
    PanicGrief,
    
    /// PLAY: Joyful engagement, roughhousing, social bonding
    /// Sanskrit: krīḍā (क्रीडा), līlā (लीला)
    Play,
}

impl PankseppEmotion {
    /// Get all seven emotions
    pub fn all() -> Vec<Self> {
        vec![
            Self::Seeking,
            Self::Fear,
            Self::Rage,
            Self::Lust,
            Self::Care,
            Self::PanicGrief,
            Self::Play,
        ]
    }
    
    /// Get Sanskrit name (primary)
    pub fn sanskrit_name(&self) -> &'static str {
        match self {
            Self::Seeking => "icchā",
            Self::Fear => "bhaya",
            Self::Rage => "krodha",
            Self::Lust => "kāma",
            Self::Care => "karuṇā",
            Self::PanicGrief => "śoka",
            Self::Play => "krīḍā",
        }
    }
    
    /// Get Devanagari script
    pub fn devanagari(&self) -> &'static str {
        match self {
            Self::Seeking => "इच्छा",
            Self::Fear => "भय",
            Self::Rage => "क्रोध",
            Self::Lust => "काम",
            Self::Care => "करुणा",
            Self::PanicGrief => "शोक",
            Self::Play => "क्रीडा",
        }
    }
    
    /// Get description
    pub fn description(&self) -> &'static str {
        match self {
            Self::Seeking => "Exploration, curiosity, desire, anticipation",
            Self::Fear => "Anxiety, vigilance, threat avoidance",
            Self::Rage => "Anger, frustration, assertion",
            Self::Lust => "Sexual desire, erotic arousal",
            Self::Care => "Nurturing, compassion, bonding",
            Self::PanicGrief => "Separation distress, loneliness",
            Self::Play => "Joyful engagement, social bonding",
        }
    }
    
    /// Get associated neurotransmitter
    pub fn neurotransmitter(&self) -> &'static str {
        match self {
            Self::Seeking => "Dopamine",
            Self::Fear => "Glutamate",
            Self::Rage => "Substance P",
            Self::Lust => "Testosterone/Estrogen",
            Self::Care => "Oxytocin",
            Self::PanicGrief => "Opioids (withdrawal)",
            Self::Play => "Endorphins",
        }
    }
    
    /// Get color for visualization (hex)
    pub fn color(&self) -> &'static str {
        match self {
            Self::Seeking => "#FFD700", // Gold
            Self::Fear => "#4B0082",    // Indigo
            Self::Rage => "#DC143C",    // Crimson
            Self::Lust => "#FF1493",    // Deep pink
            Self::Care => "#32CD32",    // Lime green
            Self::PanicGrief => "#4169E1", // Royal blue
            Self::Play => "#FF8C00",    // Dark orange
        }
    }
}

impl fmt::Display for PankseppEmotion {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:?}", self)
    }
}

/// Emotional intensity score (0.0 - 1.0)
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct EmotionalIntensity {
    pub seeking: f64,
    pub fear: f64,
    pub rage: f64,
    pub lust: f64,
    pub care: f64,
    pub panic_grief: f64,
    pub play: f64,
}

impl EmotionalIntensity {
    pub fn new() -> Self {
        Self {
            seeking: 0.0,
            fear: 0.0,
            rage: 0.0,
            lust: 0.0,
            care: 0.0,
            panic_grief: 0.0,
            play: 0.0,
        }
    }
    
    pub fn get(&self, emotion: PankseppEmotion) -> f64 {
        match emotion {
            PankseppEmotion::Seeking => self.seeking,
            PankseppEmotion::Fear => self.fear,
            PankseppEmotion::Rage => self.rage,
            PankseppEmotion::Lust => self.lust,
            PankseppEmotion::Care => self.care,
            PankseppEmotion::PanicGrief => self.panic_grief,
            PankseppEmotion::Play => self.play,
        }
    }
    
    pub fn set(&mut self, emotion: PankseppEmotion, value: f64) {
        let value = value.clamp(0.0, 1.0);
        match emotion {
            PankseppEmotion::Seeking => self.seeking = value,
            PankseppEmotion::Fear => self.fear = value,
            PankseppEmotion::Rage => self.rage = value,
            PankseppEmotion::Lust => self.lust = value,
            PankseppEmotion::Care => self.care = value,
            PankseppEmotion::PanicGrief => self.panic_grief = value,
            PankseppEmotion::Play => self.play = value,
        }
    }
    
    /// Get dominant emotion (highest intensity)
    pub fn dominant(&self) -> Option<PankseppEmotion> {
        let emotions = vec![
            (PankseppEmotion::Seeking, self.seeking),
            (PankseppEmotion::Fear, self.fear),
            (PankseppEmotion::Rage, self.rage),
            (PankseppEmotion::Lust, self.lust),
            (PankseppEmotion::Care, self.care),
            (PankseppEmotion::PanicGrief, self.panic_grief),
            (PankseppEmotion::Play, self.play),
        ];
        
        emotions.into_iter()
            .max_by(|a, b| a.1.partial_cmp(&b.1).unwrap())
            .filter(|(_, intensity)| *intensity > 0.0)
            .map(|(emotion, _)| emotion)
    }
    
    /// Overall emotional arousal (sum of all intensities)
    pub fn arousal(&self) -> f64 {
        self.seeking + self.fear + self.rage + self.lust 
            + self.care + self.panic_grief + self.play
    }
}

impl Default for EmotionalIntensity {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_all_emotions() {
        assert_eq!(PankseppEmotion::all().len(), 7);
    }

    #[test]
    fn test_emotional_intensity() {
        let mut intensity = EmotionalIntensity::new();
        intensity.set(PankseppEmotion::Seeking, 0.8);
        intensity.set(PankseppEmotion::Fear, 0.3);
        
        assert_eq!(intensity.dominant(), Some(PankseppEmotion::Seeking));
        assert_eq!(intensity.arousal(), 1.1);
    }
}
