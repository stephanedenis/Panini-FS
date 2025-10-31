//! Handlers pour la déduplication et l'analyse des atomes

use axum::{
    extract::{multipart::Multipart, Path, Query, State},
    http::StatusCode,
    Json,
};
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
    State(_state): State<AppState>,
) -> Result<Json<DedupStats>, StatusCode> {
    // TODO: Calculer depuis le CAS réel
    // Pour l'instant, retourne des données de test basées sur validation
    
    let stats = DedupStats {
        total_files: 400360,
        total_size: 9624887296, // 8.96 GB
        total_atoms: 491240,
        unique_atoms: 126177,
        dedup_ratio: 0.743,
        storage_saved: 7149823488, // 6.66 GB
        avg_reuse: 3.96,
        top_atoms: vec![
            TopAtom {
                hash: "63e1de009344e8347f154d1e3d71e2e7a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6".to_string(),
                usage_count: 380,
                size: 65536,
            },
            TopAtom {
                hash: "59a726f169f1c8d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d7".to_string(),
                usage_count: 180,
                size: 65536,
            },
            TopAtom {
                hash: "085bbcee4e02f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0".to_string(),
                usage_count: 150,
                size: 65536,
            },
            TopAtom {
                hash: "27c72988bdc2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8".to_string(),
                usage_count: 150,
                size: 65536,
            },
            TopAtom {
                hash: "7bc47ea09473f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5".to_string(),
                usage_count: 150,
                size: 65536,
            },
        ],
    };

    Ok(Json(stats))
}

/// GET /api/atoms/search?q=<query>
/// Recherche des atomes par hash
pub async fn search_atoms(
    Query(params): Query<SearchQuery>,
    State(_state): State<AppState>,
) -> Result<Json<AtomSearchResult>, StatusCode> {
    let query = params.q.to_lowercase();
    
    if query.len() < 3 {
        return Ok(Json(AtomSearchResult {
            atoms: vec![],
            total: 0,
        }));
    }

    // TODO: Recherche réelle dans le CAS
    // Pour l'instant, retourne des résultats de test
    let test_atoms = vec![
        AtomSummary {
            hash: "63e1de009344e8347f154d1e3d71e2e7a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6".to_string(),
            size: 65536,
            atom_type: "Container".to_string(),
            created_at: chrono::Utc::now().to_rfc3339(),
            usage_count: 380,
        },
        AtomSummary {
            hash: "59a726f169f1c8d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d7".to_string(),
            size: 65536,
            atom_type: "Container".to_string(),
            created_at: chrono::Utc::now().to_rfc3339(),
            usage_count: 180,
        },
    ];

    let filtered: Vec<_> = test_atoms
        .into_iter()
        .filter(|atom| atom.hash.to_lowercase().contains(&query))
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
    State(_state): State<AppState>,
) -> Result<Json<AtomDetails>, StatusCode> {
    // TODO: Récupérer depuis le CAS réel
    
    // Simuler recherche
    if hash.len() < 10 {
        return Err(StatusCode::BAD_REQUEST);
    }

    let details = AtomDetails {
        hash: hash.clone(),
        size: 65536,
        atom_type: "Container".to_string(),
        created_at: chrono::Utc::now().to_rfc3339(),
        usage_count: 380,
        files: vec![
            "/path/to/file1.html".to_string(),
            "/path/to/file2.html".to_string(),
            "/path/to/file3.html".to_string(),
        ],
    };

    Ok(Json(details))
}

/// POST /api/files/analyze
/// Upload et analyse un fichier
pub async fn analyze_file(
    State(_state): State<AppState>,
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
    
    // Découper en chunks de 64KB
    let chunk_size = 64 * 1024;
    let chunks: Vec<_> = file_data.chunks(chunk_size).collect();
    let atoms_created = chunks.len();
    
    // Pour la démo, simuler quelques atomes réutilisés
    let atoms_reused = (atoms_created as f64 * 0.3) as usize;
    let storage_saved = (file_size as f64 * 0.3) as u64;
    let dedup_ratio = atoms_reused as f64 / atoms_created as f64;
    
    // Hash du fichier complet
    let mut hasher = Sha256::new();
    hasher.update(&file_data);
    let file_hash = format!("{:x}", hasher.finalize());

    let processing_time = start.elapsed().as_millis();

    Ok(Json(AnalysisResult {
        filename,
        size: file_size,
        atoms_created,
        atoms_reused,
        dedup_ratio,
        storage_saved,
        hash: file_hash,
        processing_time_ms: processing_time,
    }))
}

/// GET /api/files/<hash>/atoms
/// Récupère la liste des atomes d'un fichier
pub async fn get_file_atoms(
    Path(hash): Path<String>,
    State(_state): State<AppState>,
) -> Result<Json<FileAtomsResponse>, StatusCode> {
    // TODO: Récupérer depuis le CAS réel
    
    if hash.len() < 10 {
        return Err(StatusCode::BAD_REQUEST);
    }

    // Simuler quelques atomes
    let atoms = vec![
        AtomInfo {
            hash: "63e1de009344e834...".to_string(),
            size: 65536,
            is_new: false,
            reuse_count: 380,
        },
        AtomInfo {
            hash: "59a726f169f1c8d2...".to_string(),
            size: 65536,
            is_new: false,
            reuse_count: 180,
        },
        AtomInfo {
            hash: "a1b2c3d4e5f6a7b8...".to_string(),
            size: 32768,
            is_new: true,
            reuse_count: 1,
        },
    ];

    Ok(Json(FileAtomsResponse { atoms }))
}
