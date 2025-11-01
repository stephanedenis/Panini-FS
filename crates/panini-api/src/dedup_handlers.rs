//! Handlers pour la déduplication et l'analyse des atomes

use axum::{
    extract::{multipart::Multipart, Path, Query, State},
    http::StatusCode,
    Json,
};
use bytes::Bytes;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

use crate::state::AppState;

// ============================================================================
// Request/Response Types
// ============================================================================

#[derive(Debug, Serialize)]
pub struct DedupStats {
    pub total_files: usize,
    pub total_size: u64,
    pub total_atoms: usize,
    pub unique_atoms: usize,
    pub dedup_ratio: f64,
    pub storage_saved: u64,
    pub avg_reuse: f64,
    pub top_atoms: Vec<TopAtom>,
}

#[derive(Debug, Serialize)]
pub struct TopAtom {
    pub hash: String,
    pub usage_count: usize,
    pub size: u64,
}

#[derive(Debug, Deserialize)]
pub struct SearchQuery {
    pub q: String,
}

#[derive(Debug, Serialize)]
pub struct AtomSearchResult {
    pub atoms: Vec<AtomSummary>,
    pub total: usize,
}

#[derive(Debug, Serialize)]
pub struct AtomSummary {
    pub hash: String,
    pub size: u64,
    #[serde(rename = "type")]
    pub atom_type: String,
    pub created_at: String,
    pub usage_count: usize,
}

#[derive(Debug, Serialize)]
pub struct AtomDetails {
    pub hash: String,
    pub size: u64,
    #[serde(rename = "type")]
    pub atom_type: String,
    pub created_at: String,
    pub usage_count: usize,
    pub files: Vec<String>,
}

#[derive(Debug, Serialize)]
pub struct AnalysisResult {
    pub filename: String,
    pub size: u64,
    pub atoms_created: usize,
    pub atoms_reused: usize,
    pub dedup_ratio: f64,
    pub storage_saved: u64,
    pub hash: String,
    pub processing_time_ms: u128,
}

#[derive(Debug, Serialize)]
pub struct FileAtomsResponse {
    pub atoms: Vec<AtomInfo>,
}

#[derive(Debug, Serialize)]
pub struct AtomInfo {
    pub hash: String,
    pub size: u64,
    pub is_new: bool,
    pub reuse_count: usize,
}

// ============================================================================
// Handlers
// ============================================================================

/// GET /api/dedup/stats
/// Retourne les statistiques globales de déduplication
pub async fn get_dedup_stats(
    State(state): State<AppState>,
) -> Result<Json<DedupStats>, StatusCode> {
    // Récupérer les vraies statistiques du CAS
    let storage_stats = state.cas.get_stats().await;
    let all_atoms = state.cas.list_atoms();
    
    // Calculer les statistiques de déduplication
    let total_refs: usize = all_atoms.iter().map(|a| a.ref_count as usize).sum();
    let unique_atoms = all_atoms.len();
    let total_size: u64 = all_atoms.iter().map(|a| a.size).sum();
    
    let dedup_ratio = if total_refs > 0 {
        1.0 - (unique_atoms as f64 / total_refs as f64)
    } else {
        0.0
    };
    
    let avg_reuse = if unique_atoms > 0 {
        total_refs as f64 / unique_atoms as f64
    } else {
        0.0
    };
    
    let storage_saved = if dedup_ratio > 0.0 {
        (total_size as f64 * dedup_ratio) as u64
    } else {
        0
    };
    
    // Identifier les top atomes par usage
    let mut sorted_atoms = all_atoms.clone();
    sorted_atoms.sort_by(|a, b| b.ref_count.cmp(&a.ref_count));
    let top_atoms: Vec<TopAtom> = sorted_atoms
        .iter()
        .take(10)
        .filter(|a| a.ref_count > 1)
        .map(|a| TopAtom {
            hash: a.hash.clone(),
            usage_count: a.ref_count as usize,
            size: a.size,
        })
        .collect();
    
    let stats = DedupStats {
        total_files: total_refs,
        total_size: total_size * total_refs as u64 / unique_atoms.max(1) as u64,
        total_atoms: storage_stats.total_atoms as usize,
        unique_atoms,
        dedup_ratio,
        storage_saved,
        avg_reuse,
        top_atoms,
    };

    Ok(Json(stats))
}

/// GET /api/atoms/search?q=<query>
/// Recherche des atomes par hash
pub async fn search_atoms(
    Query(params): Query<SearchQuery>,
    State(state): State<AppState>,
) -> Result<Json<AtomSearchResult>, StatusCode> {
    let query = params.q.to_lowercase();
    
    if query.len() < 3 {
        return Ok(Json(AtomSearchResult {
            atoms: vec![],
            total: 0,
        }));
    }

    // Recherche réelle dans le CAS
    let all_atoms = state.cas.list_atoms();
    
    let filtered: Vec<AtomSummary> = all_atoms
        .iter()
        .filter(|atom| atom.hash.to_lowercase().contains(&query))
        .map(|atom| {
            let dt = chrono::DateTime::from_timestamp(atom.created_at as i64, 0)
                .unwrap_or_else(|| chrono::Utc::now());
            AtomSummary {
                hash: atom.hash.clone(),
                size: atom.size,
                atom_type: format!("{:?}", atom.atom_type),
                created_at: dt.to_rfc3339(),
                usage_count: atom.ref_count as usize,
            }
        })
        .collect();

    let total = filtered.len();

    Ok(Json(AtomSearchResult {
        atoms: filtered,
        total,
    }))
}

/// GET /api/atoms/<hash>
/// Récupère les détails d'un atome spécifique
pub async fn get_atom_details(
    Path(hash): Path<String>,
    State(state): State<AppState>,
) -> Result<Json<AtomDetails>, StatusCode> {
    // Validation
    if hash.len() < 10 {
        return Err(StatusCode::BAD_REQUEST);
    }

    // Récupérer depuis le CAS réel
    match state.cas.get_atom_metadata(&hash) {
        Ok(metadata) => {
            let dt = chrono::DateTime::from_timestamp(metadata.created_at as i64, 0)
                .unwrap_or_else(|| chrono::Utc::now());
            let details = AtomDetails {
                hash: metadata.hash.clone(),
                size: metadata.size,
                atom_type: format!("{:?}", metadata.atom_type),
                created_at: dt.to_rfc3339(),
                usage_count: metadata.ref_count as usize,
                files: vec![
                    // TODO: Track atom->file relationships in index
                    format!("Referenced {} times", metadata.ref_count),
                ],
            };
            Ok(Json(details))
        }
        Err(_) => Err(StatusCode::NOT_FOUND),
    }
}

/// POST /api/files/analyze
/// Upload et analyse un fichier
pub async fn analyze_file(
    State(state): State<AppState>,
    mut multipart: Multipart,
) -> Result<Json<AnalysisResult>, StatusCode> {
    let start = std::time::Instant::now();
    
    let mut filename = String::new();
    let mut file_data = Vec::new();

    // Traiter le multipart
    while let Some(field) = multipart
        .next_field()
        .await
        .map_err(|_| StatusCode::BAD_REQUEST)?
    {
        let field_name = field.name().unwrap_or("").to_string();
        
        if field_name == "file" {
            filename = field
                .file_name()
                .unwrap_or("unknown")
                .to_string();
            
            file_data = field
                .bytes()
                .await
                .map_err(|_| StatusCode::BAD_REQUEST)?
                .to_vec();
        }
    }

    if file_data.is_empty() {
        return Err(StatusCode::BAD_REQUEST);
    }

    let file_size = file_data.len() as u64;
    
    // Hash du fichier complet
    let mut hasher = Sha256::new();
    hasher.update(&file_data);
    let file_hash = format!("{:x}", hasher.finalize());
    
    // Store in CAS as a container atom
    match state.cas.add_atom(&file_data, panini_core::storage::atom::AtomType::Container).await {
        Ok(atom) => {
            // Check if it was deduplicated
            match state.cas.get_atom_metadata(&atom.hash) {
                Ok(metadata) => {
                    let atoms_created = 1;
                    let atoms_reused = if metadata.ref_count > 1 { 1 } else { 0 };
                    let dedup_ratio = atoms_reused as f64 / atoms_created as f64;
                    let storage_saved = if metadata.ref_count > 1 { metadata.size } else { 0 };
                    
                    let processing_time = start.elapsed().as_millis();

                    Ok(Json(AnalysisResult {
                        filename,
                        size: file_size,
                        atoms_created,
                        atoms_reused,
                        dedup_ratio,
                        storage_saved,
                        hash: atom.hash,
                        processing_time_ms: processing_time,
                    }))
                }
                Err(_) => Err(StatusCode::INTERNAL_SERVER_ERROR),
            }
        }
        Err(_) => Err(StatusCode::INTERNAL_SERVER_ERROR),
    }
}

/// GET /api/files/<hash>/atoms
/// Récupère la liste des atomes d'un fichier
pub async fn get_file_atoms(
    Path(hash): Path<String>,
    State(state): State<AppState>,
) -> Result<Json<FileAtomsResponse>, StatusCode> {
    if hash.len() < 10 {
        return Err(StatusCode::BAD_REQUEST);
    }

    // For now, return the atom itself as a single-atom "file"
    // TODO: Implement proper file->atoms mapping when decomposer is integrated
    match state.cas.get_atom_metadata(&hash) {
        Ok(metadata) => {
            let atom = AtomInfo {
                hash: metadata.hash.clone(),
                size: metadata.size,
                is_new: metadata.ref_count == 1,
                reuse_count: metadata.ref_count as usize,
            };
            Ok(Json(FileAtomsResponse { atoms: vec![atom] }))
        }
        Err(_) => Err(StatusCode::NOT_FOUND),
    }
}
