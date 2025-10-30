//! Binary format decomposer - extracts atoms from binary files

use crate::error::{Error, Result};
use crate::storage::atom::{Atom, AtomType};
use std::io::Cursor;
use byteorder::{BigEndian, ReadBytesExt};

/// Binary format decomposer
pub struct Decomposer {
    format: FileFormat,
}

/// Supported file formats
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FileFormat {
    PNG,
    JPEG,
    MP4,
    Unknown,
}

impl FileFormat {
    /// Detect format from magic bytes
    pub fn detect(data: &[u8]) -> Self {
        if data.len() < 8 {
            return FileFormat::Unknown;
        }
        
        // PNG: 89 50 4E 47 0D 0A 1A 0A
        if data[0..8] == [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A] {
            return FileFormat::PNG;
        }
        
        // JPEG: FF D8 FF
        if data[0..3] == [0xFF, 0xD8, 0xFF] {
            return FileFormat::JPEG;
        }
        
        // MP4: typically has 'ftyp' at offset 4
        if data.len() >= 12 && &data[4..8] == b"ftyp" {
            return FileFormat::MP4;
        }
        
        FileFormat::Unknown
    }
}

impl Decomposer {
    /// Create new decomposer
    pub fn new(format: FileFormat) -> Self {
        Self { format }
    }

    /// Auto-detect format and create decomposer
    pub fn auto_detect(data: &[u8]) -> Self {
        let format = FileFormat::detect(data);
        Self::new(format)
    }

    /// Decompose binary file into atoms
    pub fn decompose(&self, data: &[u8]) -> Result<Vec<Atom>> {
        match self.format {
            FileFormat::PNG => self.decompose_png(data),
            FileFormat::JPEG => self.decompose_jpeg(data),
            FileFormat::MP4 => self.decompose_mp4(data),
            FileFormat::Unknown => {
                // Fallback: treat as single raw atom
                Ok(vec![Atom::new(data, AtomType::Raw)])
            }
        }
    }

    /// Decompose PNG into atoms
    fn decompose_png(&self, data: &[u8]) -> Result<Vec<Atom>> {
        let mut atoms = Vec::new();
        let mut cursor = Cursor::new(data);
        
        // PNG signature (8 bytes)
        let mut signature = [0u8; 8];
        std::io::Read::read_exact(&mut cursor, &mut signature)
            .map_err(|e| Error::generic(format!("Failed to read PNG signature: {}", e)))?;
        
        let sig_atom = Atom::new(&signature, AtomType::Container)
            .with_metadata("chunk_type", "signature");
        atoms.push(sig_atom);
        
        // Parse chunks
        let mut offset = 8u64;
        while (cursor.position() as usize) < data.len() {
            let chunk_start = cursor.position() as usize;
            
            // Read chunk length (4 bytes, big-endian)
            let length = cursor.read_u32::<BigEndian>()
                .map_err(|_| Error::generic("Failed to read chunk length".to_string()))?;
            
            // Read chunk type (4 bytes)
            let mut chunk_type = [0u8; 4];
            std::io::Read::read_exact(&mut cursor, &mut chunk_type)
                .map_err(|_| Error::generic("Failed to read chunk type".to_string()))?;
            
            let chunk_type_str = String::from_utf8_lossy(&chunk_type).to_string();
            
            // Read chunk data
            let mut chunk_data = vec![0u8; length as usize];
            std::io::Read::read_exact(&mut cursor, &mut chunk_data)
                .map_err(|_| Error::generic("Failed to read chunk data".to_string()))?;
            
            // Read CRC (4 bytes)
            let crc = cursor.read_u32::<BigEndian>()
                .map_err(|_| Error::generic("Failed to read CRC".to_string()))?;
            
            // Determine atom type based on chunk type
            let atom_type = match chunk_type_str.as_str() {
                "IHDR" => AtomType::Metadata,
                "IDAT" => AtomType::ImageData,
                "PLTE" => AtomType::Metadata,
                "tRNS" => AtomType::Metadata,
                "IEND" => AtomType::Container,
                _ => AtomType::Raw,
            };
            
            // Create atom with full chunk (length + type + data + crc)
            let chunk_end = cursor.position() as usize;
            let full_chunk = &data[chunk_start..chunk_end];
            
            let mut atom = Atom::new(full_chunk, atom_type);
            atom.metadata.insert("chunk_type".to_string(), chunk_type_str.clone());
            atom.metadata.insert("chunk_length".to_string(), length.to_string());
            atom.metadata.insert("crc".to_string(), format!("{:08x}", crc));
            atom.source_offset = offset;
            
            atoms.push(atom);
            offset = cursor.position();
            
            // Break on IEND chunk
            if chunk_type_str == "IEND" {
                break;
            }
        }
        
        Ok(atoms)
    }

    /// Decompose JPEG into atoms (placeholder)
    fn decompose_jpeg(&self, data: &[u8]) -> Result<Vec<Atom>> {
        // Simplified: treat as single atom for now
        // TODO: Parse JPEG segments (SOI, APP0, DQT, DHT, SOS, etc.)
        let mut atoms = Vec::new();
        
        // SOI marker (FF D8)
        if data.len() >= 2 {
            let soi = Atom::new(&data[0..2], AtomType::Container)
                .with_metadata("marker", "SOI");
            atoms.push(soi);
        }
        
        // Rest of JPEG (simplified)
        if data.len() > 2 {
            let body = Atom::new(&data[2..], AtomType::ImageData)
                .with_metadata("format", "jpeg_scan_data");
            atoms.push(body);
        }
        
        Ok(atoms)
    }

    /// Decompose MP4 into atoms (placeholder)
    fn decompose_mp4(&self, data: &[u8]) -> Result<Vec<Atom>> {
        // Simplified: treat as single atom for now
        // TODO: Parse MP4 atoms (ftyp, moov, mdat, etc.)
        let atom = Atom::new(data, AtomType::Container)
            .with_metadata("format", "mp4");
        Ok(vec![atom])
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_format_detection_png() {
        let png_sig = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A];
        assert_eq!(FileFormat::detect(&png_sig), FileFormat::PNG);
    }

    #[test]
    fn test_format_detection_jpeg() {
        let jpeg_sig = [0xFF, 0xD8, 0xFF, 0xE0];
        assert_eq!(FileFormat::detect(&jpeg_sig), FileFormat::JPEG);
    }

    #[test]
    fn test_decompose_unknown_format() {
        let data = b"unknown data";
        let decomposer = Decomposer::auto_detect(data);
        let atoms = decomposer.decompose(data).unwrap();
        
        assert_eq!(atoms.len(), 1);
        assert_eq!(atoms[0].atom_type, AtomType::Raw);
    }

    #[test]
    fn test_decompose_minimal_png() {
        // Minimal PNG: signature + IHDR + IEND
        let mut png_data = Vec::new();
        
        // PNG signature
        png_data.extend_from_slice(&[0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]);
        
        // IHDR chunk (length=13, type=IHDR, data=13 bytes, CRC=4 bytes)
        png_data.extend_from_slice(&[0x00, 0x00, 0x00, 0x0D]); // length
        png_data.extend_from_slice(b"IHDR"); // type
        png_data.extend_from_slice(&[0; 13]); // dummy data
        png_data.extend_from_slice(&[0x00, 0x00, 0x00, 0x00]); // dummy CRC
        
        // IEND chunk
        png_data.extend_from_slice(&[0x00, 0x00, 0x00, 0x00]); // length
        png_data.extend_from_slice(b"IEND"); // type
        png_data.extend_from_slice(&[0xAE, 0x42, 0x60, 0x82]); // CRC
        
        let decomposer = Decomposer::auto_detect(&png_data);
        let atoms = decomposer.decompose(&png_data).unwrap();
        
        // Should have: signature + IHDR + IEND
        assert!(atoms.len() >= 3);
        assert_eq!(atoms[0].atom_type, AtomType::Container);
        assert_eq!(atoms[0].metadata.get("chunk_type"), Some(&"signature".to_string()));
    }
}
