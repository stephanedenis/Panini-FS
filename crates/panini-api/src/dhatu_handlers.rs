//! Dhātu API Handlers
//!
//! REST endpoints for emotional classification system

use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    Json,
};
use panini_core::dhatu::{
    DhatuClassifier, EmotionalIntensity, EmotionalProfile, 
    EmotionalResonance, PankseppEmotion,
};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use crate::state::AppState;
use tokio::sync::RwLock;

/// Dhātu application state
pub struct DhatuState {
    classifier: DhatuClassifier,
    profiles: RwLock<HashMap<String, EmotionalProfile>>,
}

impl DhatuState {
    pub fn new() -> Arc<Self> {
        Arc::new(Self {
            classifier: DhatuClassifier::new(),
            profiles: RwLock::new(HashMap::new()),
        })
    }
}

/// Response: List of all emotions with metadata
#[derive(Debug, Serialize)]
pub struct EmotionsResponse {
    pub emotions: Vec<EmotionInfo>,
}

#[derive(Debug, Serialize)]
pub struct EmotionInfo {
    pub name: String,
    pub sanskrit: String,
    pub devanagari: String,
    pub description: String,
    pub neurotransmitter: String,
    pub color: String,
}

/// GET /api/dhatu/emotions - List all emotions
pub async fn get_emotions() -> Json<EmotionsResponse> {
    let emotions = PankseppEmotion::all()
        .into_iter()
        .map(|e| EmotionInfo {
            name: format!("{:?}", e),
            sanskrit: e.sanskrit_name().to_string(),
            devanagari: e.devanagari().to_string(),
            description: e.description().to_string(),
            neurotransmitter: e.neurotransmitter().to_string(),
            color: e.color().to_string(),
        })
        .collect();
    
    Json(EmotionsResponse { emotions })
}

/// Response: Dhātu roots for an emotion
#[derive(Debug, Serialize)]
pub struct RootsResponse {
    pub emotion: String,
    pub roots: Vec<RootInfo>,
}

#[derive(Debug, Serialize)]
pub struct RootInfo {
    pub root: String,
    pub devanagari: String,
    pub meaning: String,
    pub intensity: f64,
    pub derived_words: Vec<String>,
}

/// GET /api/dhatu/roots/:emotion - Get roots for emotion
pub async fn get_roots(
    State(state): State<AppState>,
    Path(emotion_str): Path<String>,
) -> Result<Json<RootsResponse>, StatusCode> {
    // Parse emotion
    let emotion = match emotion_str.to_lowercase().as_str() {
        "seeking" => PankseppEmotion::Seeking,
        "fear" => PankseppEmotion::Fear,
        "rage" => PankseppEmotion::Rage,
        "lust" => PankseppEmotion::Lust,
        "care" => PankseppEmotion::Care,
        "panicgrief" | "panic" | "grief" => PankseppEmotion::PanicGrief,
        "play" => PankseppEmotion::Play,
        _ => return Err(StatusCode::BAD_REQUEST),
    };
    
    let roots = state.dhatu.classifier.get_roots(emotion);
    let roots_info: Vec<RootInfo> = roots
        .into_iter()
        .map(|r| RootInfo {
            root: r.root.clone(),
            devanagari: r.devanagari.clone(),
            meaning: r.meaning.clone(),
            intensity: r.intensity,
            derived_words: r.derived_words.clone(),
        })
        .collect();
    
    Ok(Json(RootsResponse {
        emotion: emotion_str,
        roots: roots_info,
    }))
}

/// Request: Classify content
#[derive(Debug, Deserialize)]
pub struct ClassifyRequest {
    pub content: String,
    pub path: Option<String>,
}

/// Response: Classification result
#[derive(Debug, Serialize)]
pub struct ClassifyResponse {
    pub intensity: EmotionalIntensityDto,
    pub dominant: Option<String>,
    pub arousal: f64,
}

#[derive(Debug, Serialize)]
pub struct EmotionalIntensityDto {
    pub seeking: f64,
    pub fear: f64,
    pub rage: f64,
    pub lust: f64,
    pub care: f64,
    pub panic_grief: f64,
    pub play: f64,
}

impl From<EmotionalIntensity> for EmotionalIntensityDto {
    fn from(i: EmotionalIntensity) -> Self {
        Self {
            seeking: i.seeking,
            fear: i.fear,
            rage: i.rage,
            lust: i.lust,
            care: i.care,
            panic_grief: i.panic_grief,
            play: i.play,
        }
    }
}

/// POST /api/dhatu/classify - Classify content
pub async fn classify_content(
    State(state): State<AppState>,
    Json(req): Json<ClassifyRequest>,
) -> Json<ClassifyResponse> {
    let intensity = state.dhatu.classifier.classify_content(&req.content);
    let dominant = intensity.dominant().map(|e| format!("{:?}", e));
    let arousal = intensity.arousal();
    
    // Store profile if path provided
    if let Some(path) = req.path {
        let profile = EmotionalProfile::new(path.clone(), intensity);
        let mut profiles = state.dhatu.profiles.write().await;
        profiles.insert(path, profile);
    }
    
    Json(ClassifyResponse {
        intensity: intensity.into(),
        dominant,
        arousal,
    })
}

/// Query params for search
#[derive(Debug, Deserialize)]
pub struct SearchQuery {
    pub q: String,
    pub limit: Option<usize>,
}

/// Response: Search results
#[derive(Debug, Serialize)]
pub struct SearchResponse {
    pub query: String,
    pub results: Vec<SearchResult>,
}

#[derive(Debug, Serialize)]
pub struct SearchResult {
    pub path: String,
    pub dominant: Option<String>,
    pub confidence: f64,
    pub intensity: EmotionalIntensityDto,
}

/// GET /api/dhatu/search?q=query - Search profiles
pub async fn search_profiles(
    State(state): State<AppState>,
    Query(query): Query<SearchQuery>,
) -> Json<SearchResponse> {
    let profiles = state.dhatu.profiles.read().await;
    let limit = query.limit.unwrap_or(50);
    
    let query_lower = query.q.to_lowercase();
    let mut results: Vec<SearchResult> = profiles
        .values()
        .filter(|p| {
            p.path.to_lowercase().contains(&query_lower)
                || p.manual_tags.iter().any(|t| t.to_lowercase().contains(&query_lower))
                || p.dhatu_roots.iter().any(|r| r.to_lowercase().contains(&query_lower))
        })
        .take(limit)
        .map(|p| SearchResult {
            path: p.path.clone(),
            dominant: p.dominant_emotion.map(|e| format!("{:?}", e)),
            confidence: p.confidence,
            intensity: p.intensity.into(),
        })
        .collect();
    
    // Sort by confidence
    results.sort_by(|a, b| b.confidence.partial_cmp(&a.confidence).unwrap());
    
    Json(SearchResponse {
        query: query.q,
        results,
    })
}

/// Response: Statistics
#[derive(Debug, Serialize)]
pub struct StatsResponse {
    pub total_profiles: usize,
    pub emotion_distribution: HashMap<String, usize>,
    pub average_arousal: f64,
    pub top_emotions: Vec<(String, usize)>,
}

/// GET /api/dhatu/stats - Get statistics
pub async fn get_stats(
    State(state): State<AppState>,
) -> Json<StatsResponse> {
    let profiles = state.dhatu.profiles.read().await;
    
    let mut emotion_counts: HashMap<String, usize> = HashMap::new();
    let mut total_arousal = 0.0;
    
    for profile in profiles.values() {
        if let Some(emotion) = profile.dominant_emotion {
            let key = format!("{:?}", emotion);
            *emotion_counts.entry(key).or_insert(0) += 1;
        }
        total_arousal += profile.intensity.arousal();
    }
    
    let total = profiles.len();
    let average_arousal = if total > 0 {
        total_arousal / total as f64
    } else {
        0.0
    };
    
    let mut top_emotions: Vec<_> = emotion_counts.iter()
        .map(|(k, v)| (k.clone(), *v))
        .collect();
    top_emotions.sort_by(|a, b| b.1.cmp(&a.1));
    
    Json(StatsResponse {
        total_profiles: total,
        emotion_distribution: emotion_counts,
        average_arousal,
        top_emotions,
    })
}

/// Request: Calculate resonance
#[derive(Debug, Deserialize)]
pub struct ResonanceRequest {
    pub path_a: String,
    pub path_b: String,
}

/// Response: Resonance result
#[derive(Debug, Serialize)]
pub struct ResonanceResponse {
    pub path_a: String,
    pub path_b: String,
    pub score: f64,
    pub resonance_type: String,
    pub shared_emotions: Vec<String>,
}

/// POST /api/dhatu/resonance - Calculate emotional resonance
pub async fn calculate_resonance(
    State(state): State<AppState>,
    Json(req): Json<ResonanceRequest>,
) -> Result<Json<ResonanceResponse>, StatusCode> {
    let profiles = state.dhatu.profiles.read().await;
    
    let profile_a = profiles.get(&req.path_a)
        .ok_or(StatusCode::NOT_FOUND)?;
    let profile_b = profiles.get(&req.path_b)
        .ok_or(StatusCode::NOT_FOUND)?;
    
    let resonance = EmotionalResonance::calculate(profile_a, profile_b);
    
    Ok(Json(ResonanceResponse {
        path_a: resonance.path_a,
        path_b: resonance.path_b,
        score: resonance.score,
        resonance_type: format!("{:?}", resonance.resonance_type),
        shared_emotions: resonance.shared_emotions
            .into_iter()
            .map(|e| format!("{:?}", e))
            .collect(),
    }))
}
