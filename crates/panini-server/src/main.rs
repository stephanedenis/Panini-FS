//! Panini Server - REST API for knowledge graph access

use axum::{routing::get, Router};
use std::net::SocketAddr;
use tracing::info;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Initialize tracing
    tracing_subscriber::fmt::init();
    
    // Build our application with routes
    let app = Router::new()
        .route("/", get(root))
        .route("/health", get(health));
    
    // Run server
    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    info!("🚀 Panini Server starting on http://{}", addr);
    info!("⏳ Full API implementation coming in Phase 2.0.6!");
    
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await?;
    
    Ok(())
}

async fn root() -> &'static str {
    "Panini-FS Server v2.0.0-alpha\nGit-native distributed knowledge graph\n\nAPI coming soon!"
}

async fn health() -> &'static str {
    "OK"
}
