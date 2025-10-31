//! Dhātu: Emotional Classification System
//!
//! Named after Sanskrit धातु (dhātu) - "root" or "element"
//! Combines Panksepp's affective neuroscience with Sanskrit linguistic roots
//! 
//! ## Features
//! - Seven primary emotion classification (Panksepp model)
//! - Sanskrit verbal root (dhātu) association
//! - Automatic file/content emotional profiling
//! - Emotional resonance calculation
//! - Temporal emotional analysis

pub mod emotion;
pub mod root;
pub mod classifier;
pub mod profile;

pub use emotion::{PankseppEmotion, EmotionalIntensity};
pub use root::{DhatuRoot, DhatuCatalog};
pub use classifier::DhatuClassifier;
pub use profile::{EmotionalProfile, EmotionalResonance, ResonanceType};
