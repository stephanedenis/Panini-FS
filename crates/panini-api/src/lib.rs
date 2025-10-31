//! Panini-FS REST API Server
//!
//! Provides HTTP endpoints for:
//! - Concepts and versions
//! - Time-travel queries
//! - Snapshots
//! - Timeline events
//! - Atomic storage operations
//! - Deduplication analysis

pub mod dedup_handlers;
pub mod handlers;
pub mod routes;
pub mod server;
pub mod state;

pub use server::ApiServer;
pub use state::AppState;
