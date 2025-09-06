#!/usr/bin/env python3
"""
Prototype Rust Bridge : Export vers format Rust pour tests performance
Préparation migration Python → Rust avec benchmarking
"""

import json
import time
import cbor2
import pickle
import gzip
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import sys
import os

# Import structures communes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

@dataclass
class RustSemanticAtom:
    """Structure optimisée pour Rust"""
    id: str
    concept: str
    definition: str
    source_agent: str
    source_type: str  # wikipedia, arxiv, etc.
    timestamp: str
    confidence: float
    parent_sources: List[str]

@dataclass
class RustConceptIndex:
    """Index optimisé pour recherche Rust"""
    concept_to_atoms: Dict[str, List[str]]  # concept -> atom_ids
    agent_to_atoms: Dict[str, List[str]]    # agent -> atom_ids
    source_to_atoms: Dict[str, List[str]]   # source_type -> atom_ids
    temporal_index: List[tuple]             # (timestamp, atom_id) sorted

class RustBridge:
    def __init__(self):
        self.atoms = []
        self.index = None
        
    def load_python_stores(self) -> int:
        """Charge tous les stores Python disponibles"""
        store_files = [
            ("demo_semantic_store.json", "wikipedia"),
            ("arxiv_semantic_store.json", "arxiv"),
            ("multi_source_consensus_analysis.json", "analysis")
        ]
        
        total_loaded = 0
        
        for filename, source_type in store_files:
            if os.path.exists(filename):
                loaded = self._load_store(filename, source_type)
                total_loaded += loaded
                print(f"📊 {source_type}: {loaded} atomes chargés")
            else:
                print(f"⚠️  {filename} non trouvé")
                
        return total_loaded
    
    def _load_store(self, filename: str, source_type: str) -> int:
        """Charge un store spécifique"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                store = json.load(f)
                
            atoms_data = store.get('semantic_atoms', [])
            
            for atom_data in atoms_data:
                # Conversion vers structure Rust
                rust_atom = RustSemanticAtom(
                    id=atom_data['id'],
                    concept=atom_data['concept'],
                    definition=atom_data['definition'][:500],  # Limite pour perf
                    source_agent=atom_data['provenance']['source_agent'],
                    source_type=source_type,
                    timestamp=atom_data['provenance']['timestamp'],
                    confidence=atom_data['provenance']['extraction_confidence'],
                    parent_sources=atom_data['provenance']['parent_sources']
                )
                
                self.atoms.append(rust_atom)
                
            return len(atoms_data)
            
        except Exception as e:
            print(f"❌ Erreur chargement {filename}: {e}")
            return 0
    
    def build_optimized_index(self):
        """Construit index optimisé pour Rust"""
        print("🔧 Construction index optimisé...")
        
        concept_to_atoms = {}
        agent_to_atoms = {}
        source_to_atoms = {}
        temporal_index = []
        
        for atom in self.atoms:
            atom_id = atom.id
            
            # Index par concept
            concept = atom.concept.lower().strip()
            if concept not in concept_to_atoms:
                concept_to_atoms[concept] = []
            concept_to_atoms[concept].append(atom_id)
            
            # Index par agent
            agent = atom.source_agent
            if agent not in agent_to_atoms:
                agent_to_atoms[agent] = []
            agent_to_atoms[agent].append(atom_id)
            
            # Index par source
            source = atom.source_type
            if source not in source_to_atoms:
                source_to_atoms[source] = []
            source_to_atoms[source].append(atom_id)
            
            # Index temporel
            temporal_index.append((atom.timestamp, atom_id))
        
        # Tri index temporel
        temporal_index.sort(key=lambda x: x[0])
        
        self.index = RustConceptIndex(
            concept_to_atoms=concept_to_atoms,
            agent_to_atoms=agent_to_atoms,
            source_to_atoms=source_to_atoms,
            temporal_index=temporal_index
        )
        
        print(f"✅ Index construit: {len(concept_to_atoms)} concepts indexés")
    
    def export_to_rust_formats(self):
        """Export vers multiple formats pour test Rust"""
        print("🦀 Export vers formats Rust...")
        
        # Données pour export
        export_data = {
            'atoms': [asdict(atom) for atom in self.atoms],
            'index': asdict(self.index) if self.index else None,
            'metadata': {
                'total_atoms': len(self.atoms),
                'export_timestamp': time.time(),
                'version': '0.1.0'
            }
        }
        
        # Format 1: JSON (compatible mais verbose)
        self._export_json(export_data)
        
        # Format 2: CBOR (compact binary)
        self._export_cbor(export_data)
        
        # Format 3: Pickle + gzip (Python-specific mais très compact)
        self._export_pickle_gzip(export_data)
        
        # Format 4: Custom binary pour Rust
        self._export_custom_binary(export_data)
    
    def _export_json(self, data: Dict):
        """Export JSON standard"""
        filename = "rust_bridge_data.json"
        start_time = time.time()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        size = Path(filename).stat().st_size
        duration = time.time() - start_time
        
        print(f"  📄 JSON: {filename} ({size:,} bytes, {duration:.3f}s)")
    
    def _export_cbor(self, data: Dict):
        """Export CBOR (Concise Binary Object Representation)"""
        filename = "rust_bridge_data.cbor"
        start_time = time.time()
        
        try:
            with open(filename, 'wb') as f:
                cbor2.dump(data, f)
                
            size = Path(filename).stat().st_size
            duration = time.time() - start_time
            
            print(f"  🗜️  CBOR: {filename} ({size:,} bytes, {duration:.3f}s)")
            
        except ImportError:
            print("  ⚠️  cbor2 non installé - skip CBOR export")
        except Exception as e:
            print(f"  ❌ Erreur CBOR: {e}")
    
    def _export_pickle_gzip(self, data: Dict):
        """Export Pickle compressé"""
        filename = "rust_bridge_data.pkl.gz"
        start_time = time.time()
        
        with gzip.open(filename, 'wb') as f:
            pickle.dump(data, f)
            
        size = Path(filename).stat().st_size
        duration = time.time() - start_time
        
        print(f"  🗜️  Pickle+gzip: {filename} ({size:,} bytes, {duration:.3f}s)")
    
    def _export_custom_binary(self, data: Dict):
        """Export format binaire custom pour Rust"""
        filename = "rust_bridge_data.bin"
        start_time = time.time()
        
        # Format simple: [count][atom1][atom2]...[index]
        with open(filename, 'wb') as f:
            # Header: nombre d'atomes (4 bytes)
            f.write(len(self.atoms).to_bytes(4, 'little'))
            
            # Atomes: format fixe pour performance Rust
            for atom in self.atoms:
                # ID (16 bytes, padded)
                id_bytes = atom.id.encode('utf-8')[:16].ljust(16, b'\0')
                f.write(id_bytes)
                
                # Concept (64 bytes, padded)
                concept_bytes = atom.concept.encode('utf-8')[:64].ljust(64, b'\0')
                f.write(concept_bytes)
                
                # Confidence (8 bytes, double)
                import struct
                f.write(struct.pack('<d', atom.confidence))
                
                # Timestamp (32 bytes, padded)
                timestamp_bytes = atom.timestamp.encode('utf-8')[:32].ljust(32, b'\0')
                f.write(timestamp_bytes)
                
        size = Path(filename).stat().st_size
        duration = time.time() - start_time
        
        print(f"  ⚡ Custom binary: {filename} ({size:,} bytes, {duration:.3f}s)")
    
    def benchmark_formats(self):
        """Benchmark lecture des différents formats"""
        print("\n⚡ BENCHMARK FORMATS:")
        print("=" * 30)
        
        formats = [
            ("rust_bridge_data.json", self._benchmark_json),
            ("rust_bridge_data.cbor", self._benchmark_cbor),
            ("rust_bridge_data.pkl.gz", self._benchmark_pickle),
            ("rust_bridge_data.bin", self._benchmark_binary)
        ]
        
        for filename, benchmark_func in formats:
            if os.path.exists(filename):
                size = Path(filename).stat().st_size
                duration = benchmark_func(filename)
                if duration:
                    throughput = size / duration / 1024 / 1024  # MB/s
                    print(f"  {filename}: {duration:.3f}s ({throughput:.1f} MB/s)")
            else:
                print(f"  {filename}: non trouvé")
    
    def _benchmark_json(self, filename: str) -> float:
        """Benchmark lecture JSON"""
        start_time = time.time()
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return time.time() - start_time
        except Exception:
            return None
    
    def _benchmark_cbor(self, filename: str) -> float:
        """Benchmark lecture CBOR"""
        start_time = time.time()
        try:
            with open(filename, 'rb') as f:
                data = cbor2.load(f)
            return time.time() - start_time
        except Exception:
            return None
    
    def _benchmark_pickle(self, filename: str) -> float:
        """Benchmark lecture Pickle"""
        start_time = time.time()
        try:
            with gzip.open(filename, 'rb') as f:
                data = pickle.load(f)
            return time.time() - start_time
        except Exception:
            return None
    
    def _benchmark_binary(self, filename: str) -> float:
        """Benchmark lecture format custom"""
        start_time = time.time()
        try:
            with open(filename, 'rb') as f:
                # Lecture header
                count = int.from_bytes(f.read(4), 'little')
                
                # Lecture atomes (simulation)
                for _ in range(min(count, 100)):  # Test sur 100 premiers
                    f.read(16 + 64 + 8 + 32)  # Taille fixe par atome
                    
            return time.time() - start_time
        except Exception:
            return None
    
    def generate_rust_prototype(self):
        """Génère code Rust prototype pour tests"""
        rust_code = '''
// Prototype Rust pour PaniniFS
// cargo.toml: serde = { version = "1.0", features = ["derive"] }

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::File;
use std::io::BufReader;
use std::time::Instant;

#[derive(Debug, Serialize, Deserialize, Clone)]
struct SemanticAtom {
    id: String,
    concept: String,
    definition: String,
    source_agent: String,
    source_type: String,
    timestamp: String,
    confidence: f64,
    parent_sources: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize)]
struct ConceptIndex {
    concept_to_atoms: HashMap<String, Vec<String>>,
    agent_to_atoms: HashMap<String, Vec<String>>,
    source_to_atoms: HashMap<String, Vec<String>>,
    temporal_index: Vec<(String, String)>,
}

#[derive(Debug, Serialize, Deserialize)]
struct RustBridgeData {
    atoms: Vec<SemanticAtom>,
    index: Option<ConceptIndex>,
    metadata: HashMap<String, serde_json::Value>,
}

impl RustBridgeData {
    fn load_from_json(filename: &str) -> Result<Self, Box<dyn std::error::Error>> {
        let start = Instant::now();
        
        let file = File::open(filename)?;
        let reader = BufReader::new(file);
        let data: RustBridgeData = serde_json::from_reader(reader)?;
        
        let duration = start.elapsed();
        println!("🦀 Rust JSON load: {:?} ({} atoms)", duration, data.atoms.len());
        
        Ok(data)
    }
    
    fn search_concept(&self, query: &str) -> Vec<&SemanticAtom> {
        let start = Instant::now();
        
        let results: Vec<&SemanticAtom> = self.atoms
            .iter()
            .filter(|atom| atom.concept.to_lowercase().contains(&query.to_lowercase()))
            .collect();
            
        let duration = start.elapsed();
        println!("🔍 Search '{}': {:?} ({} results)", query, duration, results.len());
        
        results
    }
    
    fn analyze_performance(&self) {
        println!("⚡ Performance Analysis:");
        println!("  Total atoms: {}", self.atoms.len());
        
        if let Some(ref index) = self.index {
            println!("  Indexed concepts: {}", index.concept_to_atoms.len());
            println!("  Indexed agents: {}", index.agent_to_atoms.len());
            println!("  Indexed sources: {}", index.source_to_atoms.len());
        }
        
        // Benchmark recherches
        let queries = ["learning", "neural", "algorithm", "intelligence"];
        for query in &queries {
            self.search_concept(query);
        }
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🚀 PaniniFS Rust Prototype");
    
    // Chargement données
    let data = RustBridgeData::load_from_json("rust_bridge_data.json")?;
    
    // Analyse performance
    data.analyze_performance();
    
    Ok(())
}
'''
        
        with open("rust_prototype.rs", 'w') as f:
            f.write(rust_code)
            
        print(f"🦀 Prototype Rust généré: rust_prototype.rs")
        print(f"💡 Pour tester: cargo init && cp rust_prototype.rs src/main.rs && cargo run")

def main():
    print("🦀 PONT PYTHON → RUST POUR PANINI FS")
    print("=====================================")
    
    bridge = RustBridge()
    
    # Chargement données Python
    total_atoms = bridge.load_python_stores()
    
    if total_atoms == 0:
        print("❌ Aucune donnée à exporter")
        return
    
    print(f"\n🔧 Traitement {total_atoms} atomes...")
    
    # Construction index optimisé
    bridge.build_optimized_index()
    
    # Export vers formats Rust
    bridge.export_to_rust_formats()
    
    # Benchmark formats
    bridge.benchmark_formats()
    
    # Génération code prototype
    bridge.generate_rust_prototype()
    
    print(f"\n🎯 PONT RUST PRÊT")
    print(f"✨ Données exportées dans multiple formats")
    print(f"🦀 Prototype Rust généré pour tests performance")
    print(f"⚡ Prochaine étape: Implémentation Rust native")

if __name__ == "__main__":
    main()
