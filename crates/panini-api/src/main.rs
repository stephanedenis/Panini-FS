//! Panini-FS API Server
//! 
//! REST API server for temporal filesystem with time-travel capabilities

use anyhow::Result;
use panini_api::{ApiServer, AppState};
use panini_core::storage::{
    backends::localfs::LocalFsBackend,
    cas::{ContentAddressedStorage, StorageConfig},
    immutable::TemporalIndex,
};
use std::{net::SocketAddr, sync::{Arc, RwLock}};
use tracing::{info, Level};
use tracing_subscriber::FmtSubscriber;

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize tracing
    let subscriber = FmtSubscriber::builder()
        .with_max_level(Level::INFO)
        .finish();
    tracing::subscriber::set_global_default(subscriber)?;

    info!("🚀 Panini-FS API Server Starting...");

    // Create storage directories
    let storage_dir = std::env::var("PANINI_STORAGE")
        .unwrap_or_else(|_| "/tmp/panini-storage".to_string());
    
    info!("Storage directory: {}", storage_dir);
    std::fs::create_dir_all(&storage_dir)?;

    // Initialize backend (not async)
    let backend = Arc::new(LocalFsBackend::new(&storage_dir)?);
    info!("✓ Storage backend initialized");

    // Initialize CAS with config
    let config = StorageConfig {
        max_atom_size: 64 * 1024, // 64KB
        enable_dedup: true,
        compression: None,
    };
    let cas = Arc::new(ContentAddressedStorage::new(backend, config));
    info!("✓ Content-Addressed Storage initialized");

    // Initialize temporal index (use std::sync::RwLock, not tokio::sync::RwLock)
    let temporal_index = Arc::new(RwLock::new(TemporalIndex::new()));
    info!("✓ Temporal Index initialized");

    // Create application state
    let state = AppState::new(temporal_index, cas);
    info!("✓ Application state created");

    // Parse server address
    let host = std::env::var("PANINI_HOST").unwrap_or_else(|_| "127.0.0.1".to_string());
    let port = std::env::var("PANINI_PORT")
        .unwrap_or_else(|_| "3000".to_string())
        .parse::<u16>()?;
    let addr: SocketAddr = format!("{}:{}", host, port).parse()?;

    info!("Server address: http://{}", addr);

    // Create and run server
    let server = ApiServer::new(addr, state);
    info!("✓ API server configured");
    
    info!("🎯 Starting HTTP server...");
    server.run().await?;

    Ok(())
}
