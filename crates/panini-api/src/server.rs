//! API server implementation

use anyhow::Result;
use std::net::SocketAddr;
use tracing::{info, warn};

use crate::{routes::create_router, state::AppState};

/// Main API server
pub struct ApiServer {
    addr: SocketAddr,
    state: AppState,
}

impl ApiServer {
    /// Create a new API server
    pub fn new(addr: SocketAddr, state: AppState) -> Self {
        Self { addr, state }
    }

    /// Run the server
    pub async fn run(self) -> Result<()> {
        info!("Starting Panini-FS API server on {}", self.addr);
        
        let router = create_router(self.state);
        
        info!("API endpoints available:");
        info!("  GET  /api/health");
        info!("  GET  /api/concepts");
        info!("  GET  /api/concepts/:id");
        info!("  GET  /api/concepts/:id/versions/:version_id");
        info!("  GET  /api/concepts/:id/diff?from=v1&to=v2");
        info!("  GET  /api/timeline?start=...&end=...");
        info!("  GET  /api/snapshots");
        info!("  GET  /api/snapshots/:id");
        info!("  GET  /api/time-travel?timestamp=...");
        info!("  GET  /api/stats");
        
        let listener = tokio::net::TcpListener::bind(self.addr).await?;
        
        axum::serve(listener, router)
            .await
            .map_err(|e| anyhow::anyhow!("Server error: {}", e))?;
        
        warn!("API server stopped");
        
        Ok(())
    }
}
