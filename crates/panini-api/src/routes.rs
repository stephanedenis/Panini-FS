//! Routing configuration for Panini-FS API

use axum::{
    routing::{get, post},
    Router,
};
use tower_http::cors::CorsLayer;

use crate::{handlers, state::AppState};

/// Create the main API router with all endpoints
pub fn create_router(state: AppState) -> Router {
    // API routes
    let api_routes = Router::new()
        // Health check
        .route("/health", get(handlers::health_check))
        
        // Concept endpoints
        .route("/concepts", get(handlers::list_concepts))
        .route("/concepts/:id", get(handlers::get_concept))
        .route(
            "/concepts/:id/versions/:version_id",
            get(handlers::get_version),
        )
        .route("/concepts/:id/diff", get(handlers::get_diff))
        
        // Timeline endpoint
        .route("/timeline", get(handlers::get_timeline))
        
        // Snapshot endpoints
        .route("/snapshots", get(handlers::list_snapshots))
        .route("/snapshots/:id", get(handlers::get_snapshot))
        
        // Time-travel endpoint
        .route("/time-travel", get(handlers::time_travel))
        
        // Stats endpoint
        .route("/stats", get(handlers::get_stats));

    // Main router with /api prefix
    Router::new()
        .nest("/api", api_routes)
        .layer(CorsLayer::permissive()) // Allow CORS for Web UI
        .with_state(state)
}
