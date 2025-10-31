//! Application state shared across handlers

use crate::dhatu_handlers::DhatuState;
use panini_core::storage::{
    backends::localfs::LocalFsBackend,
    cas::ContentAddressedStorage,
    immutable::TemporalIndex,
};
use std::sync::{Arc, RwLock};

/// Shared application state
#[derive(Clone)]
pub struct AppState {
    /// Temporal index for time-travel queries
    pub temporal_index: Arc<RwLock<TemporalIndex>>,
    
    /// Content-addressed storage
    pub cas: Arc<ContentAddressedStorage<LocalFsBackend>>,
    
    /// Dhātu emotional classification system
    pub dhatu: Arc<DhatuState>,
}

impl AppState {
    /// Create new application state
    pub fn new(
        temporal_index: Arc<RwLock<TemporalIndex>>,
        cas: Arc<ContentAddressedStorage<LocalFsBackend>>,
    ) -> Self {
        Self {
            temporal_index,
            cas,
            dhatu: DhatuState::new(),
        }
    }
}
