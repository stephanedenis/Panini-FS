// PaniniFS - Compression Sémantique Universelle
// Bibliothèque principale

/// Module principal du système PaniniFS
pub mod core;
pub mod semantic;
pub mod storage;
pub mod vfs;
pub mod query;
pub mod validation;
pub mod config;

pub use crate::core::*;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
