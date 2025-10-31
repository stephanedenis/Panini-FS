//! HTTP request handlers for Panini-FS API

use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    Json,
};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

use crate::state::AppState;
use panini_core::storage::immutable::{Concept, ConceptVersion, Snapshot, TimelineEvent};

// ============================================================================
// Response Types
// ============================================================================

#[derive(Debug, Serialize)]
pub struct ApiResponse<T> {
    pub success: bool,
    pub data: Option<T>,
    pub error: Option<String>,
}

impl<T> ApiResponse<T> {
    pub fn success(data: T) -> Self {
        Self {
            success: true,
            data: Some(data),
            error: None,
        }
    }

    pub fn error(message: String) -> Self {
        Self {
            success: false,
            data: None,
            error: Some(message),
        }
    }
}

#[derive(Debug, Serialize)]
pub struct ConceptListResponse {
    pub concepts: Vec<ConceptSummary>,
    pub total: usize,
}

#[derive(Debug, Serialize)]
pub struct ConceptSummary {
    pub id: String,
    pub name: String,
    pub current_version: String,
    pub version_count: usize,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

#[derive(Debug, Serialize)]
pub struct ConceptDetail {
    pub id: String,
    pub name: String,
    pub current_version: String,
    pub versions: Vec<VersionSummary>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
    pub metadata: HashMap<String, String>,
}

#[derive(Debug, Serialize)]
pub struct VersionSummary {
    pub version_id: String,
    pub parent: Option<String>,
    pub timestamp: DateTime<Utc>,
    pub author: String,
    pub message: String,
    pub size: u64,
    pub atom_count: usize,
}

#[derive(Debug, Serialize)]
pub struct VersionDetail {
    pub version_id: String,
    pub parent: Option<String>,
    pub atoms: Vec<String>,
    pub size: u64,
    pub content_hash: String,
    pub timestamp: DateTime<Utc>,
    pub author: String,
    pub message: String,
    pub metadata: HashMap<String, String>,
}

#[derive(Debug, Serialize)]
pub struct TimelineResponse {
    pub events: Vec<TimelineEventResponse>,
    pub total: usize,
}

#[derive(Debug, Serialize)]
#[serde(tag = "type")]
pub enum TimelineEventResponse {
    ConceptCreated {
        timestamp: DateTime<Utc>,
        concept_id: String,
        concept_name: String,
        version_id: String,
    },
    ConceptModified {
        timestamp: DateTime<Utc>,
        concept_id: String,
        concept_name: String,
        version_id: String,
        previous_version: String,
    },
    SnapshotCreated {
        timestamp: DateTime<Utc>,
        snapshot_id: String,
        snapshot_name: String,
    },
}

#[derive(Debug, Serialize)]
pub struct SnapshotListResponse {
    pub snapshots: Vec<SnapshotSummary>,
    pub total: usize,
}

#[derive(Debug, Serialize)]
pub struct SnapshotSummary {
    pub id: String,
    pub name: String,
    pub timestamp: DateTime<Utc>,
    pub concept_count: usize,
}

#[derive(Debug, Serialize)]
pub struct SnapshotDetail {
    pub id: String,
    pub name: String,
    pub timestamp: DateTime<Utc>,
    pub concepts: HashMap<String, String>, // concept_id -> version_id
    pub metadata: HashMap<String, String>,
}

#[derive(Debug, Serialize)]
pub struct DiffResponse {
    pub from: String,
    pub to: String,
    pub added_atoms: Vec<String>,
    pub removed_atoms: Vec<String>,
    pub size_change: i64,
}

#[derive(Debug, Serialize)]
pub struct TimeTravelResponse {
    pub timestamp: DateTime<Utc>,
    pub concepts: HashMap<String, String>, // concept_id -> version_id
}

#[derive(Debug, Serialize)]
pub struct StatsResponse {
    pub total_concepts: usize,
    pub total_versions: usize,
    pub total_snapshots: usize,
    pub total_atoms: u64,
    pub total_size: u64,
    pub dedup_savings: u64,
}

// ============================================================================
// Query Parameters
// ============================================================================

#[derive(Debug, Deserialize)]
pub struct TimelineQuery {
    pub start: Option<DateTime<Utc>>,
    pub end: Option<DateTime<Utc>>,
}

#[derive(Debug, Deserialize)]
pub struct TimeTravelQuery {
    pub timestamp: DateTime<Utc>,
}

#[derive(Debug, Deserialize)]
pub struct DiffQuery {
    pub from: String,
    pub to: String,
}

// ============================================================================
// Handlers
// ============================================================================

/// GET /api/health - Health check
pub async fn health_check() -> Json<ApiResponse<String>> {
    Json(ApiResponse::success("OK".to_string()))
}

/// GET /api/concepts - List all concepts
pub async fn list_concepts(
    State(state): State<AppState>,
) -> Result<Json<ApiResponse<ConceptListResponse>>, StatusCode> {
    let index = state.temporal_index.read().unwrap();
    let concepts = index.get_all_concepts();
    
    let summaries: Vec<ConceptSummary> = concepts
        .iter()
        .map(|c| ConceptSummary {
            id: c.id.clone(),
            name: c.name.clone(),
            current_version: c.current_version.clone(),
            version_count: c.versions.len(),
            created_at: c.created_at,
            updated_at: c.updated_at,
        })
        .collect();
    
    let response = ConceptListResponse {
        total: summaries.len(),
        concepts: summaries,
    };
    
    Ok(Json(ApiResponse::success(response)))
}

/// GET /api/concepts/:id - Get concept details
pub async fn get_concept(
    State(state): State<AppState>,
    Path(id): Path<String>,
) -> Result<Json<ApiResponse<ConceptDetail>>, StatusCode> {
    let index = state.temporal_index.read().unwrap();
    
    match index.get_concept(&id) {
        Some(concept) => {
            let versions: Vec<VersionSummary> = concept
                .versions
                .values()
                .map(|v| VersionSummary {
                    version_id: v.version_id.clone(),
                    parent: v.parent.clone(),
                    timestamp: v.timestamp,
                    author: v.author.clone(),
                    message: v.message.clone(),
                    size: v.size,
                    atom_count: v.atoms.len(),
                })
                .collect();
            
            let detail = ConceptDetail {
                id: concept.id.clone(),
                name: concept.name.clone(),
                current_version: concept.current_version.clone(),
                versions,
                created_at: concept.created_at,
                updated_at: concept.updated_at,
                metadata: concept.metadata.clone(),
            };
            
            Ok(Json(ApiResponse::success(detail)))
        }
        None => Err(StatusCode::NOT_FOUND),
    }
}

/// GET /api/concepts/:id/versions/:version_id - Get version details
pub async fn get_version(
    State(state): State<AppState>,
    Path((id, version_id)): Path<(String, String)>,
) -> Result<Json<ApiResponse<VersionDetail>>, StatusCode> {
    let index = state.temporal_index.read().unwrap();
    
    match index.get_concept(&id) {
        Some(concept) => match concept.get_version(&version_id) {
            Some(version) => {
                let detail = VersionDetail {
                    version_id: version.version_id.clone(),
                    parent: version.parent.clone(),
                    atoms: version.atoms.clone(),
                    size: version.size,
                    content_hash: version.content_hash.clone(),
                    timestamp: version.timestamp,
                    author: version.author.clone(),
                    message: version.message.clone(),
                    metadata: version.metadata.clone(),
                };
                
                Ok(Json(ApiResponse::success(detail)))
            }
            None => Err(StatusCode::NOT_FOUND),
        },
        None => Err(StatusCode::NOT_FOUND),
    }
}

/// GET /api/timeline - Get timeline of events
pub async fn get_timeline(
    State(state): State<AppState>,
    Query(params): Query<TimelineQuery>,
) -> Result<Json<ApiResponse<TimelineResponse>>, StatusCode> {
    let index = state.temporal_index.read().unwrap();
    
    let start = params.start.unwrap_or_else(|| Utc::now() - chrono::Duration::days(30));
    let end = params.end.unwrap_or_else(|| Utc::now());
    
    let timeline = index.get_timeline_range(start, end);
    
    let mut events = Vec::new();
    for (timestamp, event) in timeline {
        match event {
            TimelineEvent::ConceptCreated { concept_id, version_id } => {
                if let Some(concept) = index.get_concept(concept_id) {
                    events.push(TimelineEventResponse::ConceptCreated {
                        timestamp: *timestamp,
                        concept_id: concept_id.clone(),
                        concept_name: concept.name.clone(),
                        version_id: version_id.clone(),
                    });
                }
            }
            TimelineEvent::ConceptModified {
                concept_id,
                version_id,
                previous_version,
            } => {
                if let Some(concept) = index.get_concept(concept_id) {
                    events.push(TimelineEventResponse::ConceptModified {
                        timestamp: *timestamp,
                        concept_id: concept_id.clone(),
                        concept_name: concept.name.clone(),
                        version_id: version_id.clone(),
                        previous_version: previous_version.clone(),
                    });
                }
            }
            TimelineEvent::SnapshotCreated { snapshot_id } => {
                events.push(TimelineEventResponse::SnapshotCreated {
                    timestamp: *timestamp,
                    snapshot_id: snapshot_id.clone(),
                    snapshot_name: snapshot_id.clone(), // TODO: Get actual name
                });
            }
        }
    }
    
    let response = TimelineResponse {
        total: events.len(),
        events,
    };
    
    Ok(Json(ApiResponse::success(response)))
}

/// GET /api/snapshots - List all snapshots
pub async fn list_snapshots(
    State(state): State<AppState>,
) -> Result<Json<ApiResponse<SnapshotListResponse>>, StatusCode> {
    let index = state.temporal_index.read().unwrap();
    let snapshots = index.get_snapshots();
    
    let summaries: Vec<SnapshotSummary> = snapshots
        .iter()
        .map(|s| SnapshotSummary {
            id: s.id.clone(),
            name: s.name.clone(),
            timestamp: s.timestamp,
            concept_count: s.concepts.len(),
        })
        .collect();
    
    let response = SnapshotListResponse {
        total: summaries.len(),
        snapshots: summaries,
    };
    
    Ok(Json(ApiResponse::success(response)))
}

/// GET /api/snapshots/:id - Get snapshot details
pub async fn get_snapshot(
    State(state): State<AppState>,
    Path(id): Path<String>,
) -> Result<Json<ApiResponse<SnapshotDetail>>, StatusCode> {
    // TODO: Implement snapshot retrieval from TemporalIndex
    // For now, return not implemented
    Err(StatusCode::NOT_IMPLEMENTED)
}

/// GET /api/time-travel - Get system state at timestamp
pub async fn time_travel(
    State(state): State<AppState>,
    Query(params): Query<TimeTravelQuery>,
) -> Result<Json<ApiResponse<TimeTravelResponse>>, StatusCode> {
    let index = state.temporal_index.read().unwrap();
    let state_at_time = index.get_state_at(params.timestamp);
    
    let response = TimeTravelResponse {
        timestamp: params.timestamp,
        concepts: state_at_time,
    };
    
    Ok(Json(ApiResponse::success(response)))
}

/// GET /api/concepts/:id/diff - Get diff between versions
pub async fn get_diff(
    State(state): State<AppState>,
    Path(id): Path<String>,
    Query(params): Query<DiffQuery>,
) -> Result<Json<ApiResponse<DiffResponse>>, StatusCode> {
    let index = state.temporal_index.read().unwrap();
    
    match index.get_concept(&id) {
        Some(concept) => match concept.diff(&params.from, &params.to) {
            Some(diff) => {
                let response = DiffResponse {
                    from: diff.from,
                    to: diff.to,
                    added_atoms: diff.added_atoms,
                    removed_atoms: diff.removed_atoms,
                    size_change: diff.size_change,
                };
                
                Ok(Json(ApiResponse::success(response)))
            }
            None => Err(StatusCode::NOT_FOUND),
        },
        None => Err(StatusCode::NOT_FOUND),
    }
}

/// GET /api/stats - Get system statistics
pub async fn get_stats(
    State(state): State<AppState>,
) -> Result<Json<ApiResponse<StatsResponse>>, StatusCode> {
    // Get data from temporal index (must drop lock before async call)
    let (total_concepts, total_versions, total_snapshots) = {
        let index = state.temporal_index.read().unwrap();
        let concepts = index.get_all_concepts();
        let total_versions: usize = concepts.iter().map(|c| c.versions.len()).sum();
        let snapshots = index.get_snapshots();
        (concepts.len(), total_versions, snapshots.len())
    }; // Lock dropped here
    
    // Now safe to await
    let cas_stats = state.cas.get_stats().await;
    
    let response = StatsResponse {
        total_concepts,
        total_versions,
        total_snapshots,
        total_atoms: cas_stats.total_atoms,
        total_size: cas_stats.total_size,
        dedup_savings: cas_stats.dedup_savings,
    };
    
    Ok(Json(ApiResponse::success(response)))
}
