//! Panini Server - Complete REST API

use axum::{
    extract::{Path, State},
    http::StatusCode,
    response::{IntoResponse, Json},
    routing::{delete, get, post, put},
    Router,
};
use panini_core::git::repo::PaniniRepo;
use panini_core::schema::concept::Concept;
use panini_core::schema::crud::*;
use panini_core::schema::relations::*;
use panini_core::schema::relation::RelationType;
use serde::Deserialize;
use std::net::SocketAddr;
use std::sync::Arc;
use tower_http::cors::CorsLayer;

#[derive(Clone)]
struct AppState {
    repo: Arc<PaniniRepo>,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt::init();
    
    let repo = PaniniRepo::open(".").expect("Failed to open repository");
    let state = AppState { repo: Arc::new(repo) };
    
    let app = Router::new()
        .route("/", get(root))
        .route("/health", get(health))
        .route("/concepts", get(list_all).post(create_new))
        .route("/concepts/:id", get(get_one).put(update_one).delete(delete_one))
        .route("/concepts/:id/relations", get(get_rels).post(add_rel))
        .layer(CorsLayer::permissive())
        .with_state(state);
    
    let addr = SocketAddr::from(([0, 0, 0, 0], 3000));
    println!("🚀 Panini Server on http://{}", addr);
    
    let listener = tokio::net::TcpListener::bind(&addr).await?;
    axum::serve(listener, app)
        .await?;
    
    Ok(())
}

async fn root() -> &'static str {
    "Panini-FS v2.0.0 - Git-native knowledge graph"
}

async fn health() -> &'static str {
    "OK"
}

async fn list_all(State(state): State<AppState>) -> impl IntoResponse {
    match list_concepts(&state.repo) {
        Ok(ids) => (StatusCode::OK, Json(ids)).into_response(),
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
    }
}

async fn create_new(State(state): State<AppState>, Json(concept): Json<Concept>) -> impl IntoResponse {
    match create_concept(&state.repo, &concept) {
        Ok(_) => (StatusCode::CREATED, Json(concept)).into_response(),
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
    }
}

async fn get_one(State(state): State<AppState>, Path(id): Path<String>) -> impl IntoResponse {
    match read_concept(&state.repo, &id) {
        Ok(c) => (StatusCode::OK, Json(c)).into_response(),
        Err(_) => (StatusCode::NOT_FOUND, "Not found".to_string()).into_response(),
    }
}

async fn update_one(State(state): State<AppState>, Path(id): Path<String>, Json(concept): Json<Concept>) -> impl IntoResponse {
    if id != concept.id {
        return (StatusCode::BAD_REQUEST, "ID mismatch".to_string()).into_response();
    }
    match update_concept(&state.repo, &concept) {
        Ok(_) => (StatusCode::OK, Json(concept)).into_response(),
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
    }
}

async fn delete_one(State(state): State<AppState>, Path(id): Path<String>) -> impl IntoResponse {
    match delete_concept(&state.repo, &id) {
        Ok(_) => (StatusCode::NO_CONTENT, "").into_response(),
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
    }
}

async fn get_rels(State(state): State<AppState>, Path(id): Path<String>) -> impl IntoResponse {
    match get_relations(&state.repo, &id) {
        Ok(rels) => (StatusCode::OK, Json(rels)).into_response(),
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
    }
}

#[derive(Deserialize)]
struct AddRelReq {
    rel_type: String,
    target: String,
    confidence: Option<f32>,
}

async fn add_rel(State(state): State<AppState>, Path(id): Path<String>, Json(req): Json<AddRelReq>) -> impl IntoResponse {
    let rt = match req.rel_type.to_lowercase().as_str() {
        "is_a" => RelationType::IsA,
        "part_of" => RelationType::PartOf,
        "causes" => RelationType::Causes,
        "contradicts" => RelationType::Contradicts,
        "supports" => RelationType::Supports,
        "derives_from" => RelationType::DerivesFrom,
        "used_by" => RelationType::UsedBy,
        "related_to" => RelationType::RelatedTo,
        _ => return (StatusCode::BAD_REQUEST, "Invalid type".to_string()).into_response(),
    };
    
    match add_relation(&state.repo, &id, rt, &req.target, req.confidence) {
        Ok(_) => (StatusCode::CREATED, "").into_response(),
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
    }
}
