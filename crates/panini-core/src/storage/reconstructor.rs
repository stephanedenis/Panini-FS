//! Binary format reconstructor - rebuilds files from atoms

use crate::error::Result;
use crate::storage::atom::Atom;

/// Binary format reconstructor
pub struct Reconstructor;

impl Reconstructor {
    /// Reconstruct binary file from atoms
    pub fn reconstruct(atoms: &[Atom], atoms_data: Vec<Vec<u8>>) -> Result<Vec<u8>> {
        if atoms.len() != atoms_data.len() {
            return Err(crate::error::Error::generic(
                "Atom count mismatch with data".to_string(),
            ));
        }
        
        // Simple concatenation in order
        let mut reconstructed = Vec::new();
        for data in atoms_data {
            reconstructed.extend_from_slice(&data);
        }
        
        Ok(reconstructed)
    }

    /// Reconstruct with verification
    pub fn reconstruct_verified(
        atoms: &[Atom],
        atoms_data: Vec<Vec<u8>>,
    ) -> Result<Vec<u8>> {
        if atoms.len() != atoms_data.len() {
            return Err(crate::error::Error::generic(
                "Atom count mismatch with data".to_string(),
            ));
        }
        
        // Verify each atom hash matches its data
        for (atom, data) in atoms.iter().zip(atoms_data.iter()) {
            let computed_hash = Atom::compute_hash(data);
            if computed_hash != atom.hash {
                return Err(crate::error::Error::generic(format!(
                    "Hash mismatch: expected {}, got {}",
                    atom.hash, computed_hash
                )));
            }
        }
        
        // Reconstruct
        Self::reconstruct(atoms, atoms_data)
    }

    /// Get total size of reconstructed file
    pub fn total_size(atoms: &[Atom]) -> u64 {
        atoms.iter().map(|a| a.size).sum()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::storage::atom::AtomType;

    #[test]
    fn test_reconstruct_simple() {
        let atom1 = Atom::new(b"part1", AtomType::Container);
        let atom2 = Atom::new(b"part2", AtomType::Raw);
        let atoms = vec![atom1, atom2];
        
        let data = vec![b"part1".to_vec(), b"part2".to_vec()];
        let reconstructed = Reconstructor::reconstruct(&atoms, data).unwrap();
        
        assert_eq!(reconstructed, b"part1part2");
    }

    #[test]
    fn test_reconstruct_verified() {
        let atom1 = Atom::new(b"verified1", AtomType::Container);
        let atom2 = Atom::new(b"verified2", AtomType::Raw);
        let atoms = vec![atom1, atom2];
        
        let data = vec![b"verified1".to_vec(), b"verified2".to_vec()];
        let reconstructed = Reconstructor::reconstruct_verified(&atoms, data).unwrap();
        
        assert_eq!(reconstructed, b"verified1verified2");
    }

    #[test]
    fn test_reconstruct_hash_mismatch() {
        let atom = Atom::new(b"original", AtomType::Container);
        let atoms = vec![atom];
        
        // Wrong data
        let data = vec![b"corrupted".to_vec()];
        let result = Reconstructor::reconstruct_verified(&atoms, data);
        
        assert!(result.is_err());
    }

    #[test]
    fn test_total_size() {
        let atoms = vec![
            Atom::new(b"12345", AtomType::Container),
            Atom::new(b"67890", AtomType::Raw),
            Atom::new(b"ABC", AtomType::ImageData),
        ];
        
        assert_eq!(Reconstructor::total_size(&atoms), 13);
    }
}
