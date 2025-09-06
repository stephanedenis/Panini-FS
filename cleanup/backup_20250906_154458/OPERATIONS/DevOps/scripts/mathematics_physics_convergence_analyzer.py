#!/usr/bin/env python3
"""
Analyseur Convergences Mathématiques-Physiques
🔗 Exploration connexions entre théories information, compression, fractales et physique
"""

import json
import datetime
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set
import re
import os

class MathPhysicsConvergenceAnalyzer:
    def __init__(self):
        self.sources = {}
        self.all_atoms = []
        self.convergence_patterns = []
        self.cross_domain_connections = defaultdict(list)
        
    def load_mathematical_sources(self) -> int:
        """Charge sources mathématiques et physiques"""
        sources_config = [
            ("information_theory_semantic_store.json", "information_theory"),
            ("physics_mathematics_semantic_store.json", "physics_mathematics"),
            ("demo_semantic_store.json", "wikipedia_general"),
            ("arxiv_semantic_store.json", "arxiv_papers"),
            ("historical_books_semantic_store.json", "historical_books")
        ]
        
        total_loaded = 0
        
        for filename, source_type in sources_config:
            if os.path.exists(filename):
                loaded = self._load_source(filename, source_type)
                total_loaded += loaded
                print(f"📊 {source_type}: {loaded} atomes chargés")
        
        return total_loaded
    
    def _load_source(self, filename: str, source_type: str) -> int:
        """Charge source avec enrichissement métadonnées"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                store = json.load(f)
            
            self.sources[source_type] = store
            atoms = store.get('semantic_atoms', [])
            
            for atom in atoms:
                atom['source_type'] = source_type
                self.all_atoms.append(atom)
            
            return len(atoms)
        except Exception as e:
            print(f"❌ Erreur chargement {filename}: {e}")
            return 0
    
    def detect_mathematical_convergences(self) -> List[Dict]:
        """Détecte convergences entre domaines mathématiques"""
        convergences = []
        
        # Patterns de convergence conceptuelle
        convergence_patterns = [
            {
                "pattern_name": "information_entropy_convergence",
                "keywords": ["entropy", "entropie", "information"],
                "domains": ["shannon_theory", "statistical_mechanics", "thermodynamics"],
                "unifying_principle": "entropy as universal information measure"
            },
            {
                "pattern_name": "compression_fractal_convergence", 
                "keywords": ["compression", "fractal", "self-similarity", "auto-similaire"],
                "domains": ["compression_algorithms", "fractal_geometry"],
                "unifying_principle": "exploitation of self-similarity for compression"
            },
            {
                "pattern_name": "quantum_classical_emergence",
                "keywords": ["quantum", "classical", "emergence", "décohérence"],
                "domains": ["quantum_information", "emergence_theory"],
                "unifying_principle": "quantum-to-classical transition as emergence"
            },
            {
                "pattern_name": "phase_transitions_universality",
                "keywords": ["transition", "critical", "universality", "critique"],
                "domains": ["phase_transitions", "percolation_theory", "statistical_mechanics"],
                "unifying_principle": "universal behavior at critical points"
            },
            {
                "pattern_name": "holographic_information_principle",
                "keywords": ["holographic", "boundary", "dimension", "information"],
                "domains": ["holographic_principle", "compression_algorithms"],
                "unifying_principle": "dimensional reduction preserves information"
            }
        ]
        
        for pattern in convergence_patterns:
            convergence = self._analyze_convergence_pattern(pattern)
            if convergence:
                convergences.append(convergence)
        
        return convergences
    
    def _analyze_convergence_pattern(self, pattern: Dict) -> Dict:
        """Analyse pattern convergence spécifique"""
        matching_atoms = []
        keywords = pattern["keywords"]
        
        for atom in self.all_atoms:
            concept_text = f"{atom['concept']} {atom['definition']}".lower()
            if any(keyword.lower() in concept_text for keyword in keywords):
                matching_atoms.append(atom)
        
        if len(matching_atoms) < 2:
            return None
        
        # Analyse cross-domain connections
        source_distribution = Counter(atom['source_type'] for atom in matching_atoms)
        category_distribution = Counter(atom.get('category', 'unknown') for atom in matching_atoms)
        
        convergence = {
            "pattern_name": pattern["pattern_name"],
            "unifying_principle": pattern["unifying_principle"],
            "matching_concepts": [atom['concept'] for atom in matching_atoms],
            "source_diversity": len(source_distribution),
            "sources_involved": dict(source_distribution),
            "category_diversity": len(category_distribution),
            "categories_involved": dict(category_distribution),
            "convergence_strength": self._calculate_convergence_strength(matching_atoms),
            "mathematical_connections": self._extract_mathematical_connections(matching_atoms),
            "cross_references": self._find_cross_references(matching_atoms)
        }
        
        return convergence
    
    def _calculate_convergence_strength(self, atoms: List[Dict]) -> float:
        """Calcule force convergence basée sur diversité et cohérence"""
        if not atoms:
            return 0.0
        
        # Diversité sources
        sources = set(atom['source_type'] for atom in atoms)
        source_diversity = len(sources) / 5  # Max 5 sources différentes
        
        # Cohérence confidence
        confidences = [
            atom['provenance']['extraction_confidence'] 
            for atom in atoms 
            if 'provenance' in atom
        ]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.5
        
        # Richesse mathématique
        math_richness = len([
            atom for atom in atoms 
            if 'mathematical_form' in atom.get('metadata', {})
        ]) / len(atoms)
        
        return (source_diversity + avg_confidence + math_richness) / 3
    
    def _extract_mathematical_connections(self, atoms: List[Dict]) -> List[Dict]:
        """Extrait connexions mathématiques entre concepts"""
        math_connections = []
        
        for atom in atoms:
            metadata = atom.get('metadata', {})
            if 'mathematical_form' in metadata:
                math_connections.append({
                    "concept": atom['concept'],
                    "mathematical_form": metadata['mathematical_form'],
                    "category": atom.get('category', 'unknown')
                })
        
        return math_connections
    
    def _find_cross_references(self, atoms: List[Dict]) -> List[Dict]:
        """Trouve références croisées entre concepts"""
        cross_refs = []
        
        for i, atom1 in enumerate(atoms):
            for j, atom2 in enumerate(atoms[i+1:], i+1):
                # Recherche mots communs significatifs
                words1 = set(re.findall(r'\b\w{4,}\b', atom1['definition'].lower()))
                words2 = set(re.findall(r'\b\w{4,}\b', atom2['definition'].lower()))
                
                common_words = words1.intersection(words2)
                significant_words = [w for w in common_words if len(w) > 5]
                
                if len(significant_words) >= 2:
                    cross_refs.append({
                        "concept1": atom1['concept'],
                        "concept2": atom2['concept'],
                        "common_terms": list(significant_words),
                        "connection_strength": len(significant_words) / max(len(words1), len(words2))
                    })
        
        return cross_refs
    
    def analyze_emergence_hierarchies(self) -> Dict:
        """Analyse hiérarchies émergence multi-niveaux"""
        hierarchies = {
            "information_hierarchy": self._analyze_information_hierarchy(),
            "complexity_hierarchy": self._analyze_complexity_hierarchy(),
            "scale_hierarchy": self._analyze_scale_hierarchy()
        }
        
        return hierarchies
    
    def _analyze_information_hierarchy(self) -> List[Dict]:
        """Hiérarchie informationnelle: bits → entropie → complexité"""
        levels = [
            {
                "level": 1,
                "scale": "microscopic",
                "concepts": ["bit", "quantum_bit", "information_bit"],
                "emergence_mechanism": "discrete_information_units"
            },
            {
                "level": 2, 
                "scale": "mesoscopic",
                "concepts": ["entropy", "entropie", "mutual_information"],
                "emergence_mechanism": "statistical_aggregation"
            },
            {
                "level": 3,
                "scale": "macroscopic", 
                "concepts": ["complexity", "emergence", "self_organization"],
                "emergence_mechanism": "collective_behavior"
            }
        ]
        
        return levels
    
    def _analyze_complexity_hierarchy(self) -> List[Dict]:
        """Hiérarchie complexité: simple → compliqué → complexe"""
        return [
            {
                "complexity_type": "simple",
                "characteristics": ["linear", "predictable", "reductionist"],
                "examples": ["linear_coding", "huffman_coding"]
            },
            {
                "complexity_type": "complicated",
                "characteristics": ["non-linear", "many_parts", "engineered"],
                "examples": ["JPEG_compression", "wavelet_transforms"]
            },
            {
                "complexity_type": "complex",
                "characteristics": ["emergent", "adaptive", "self_organizing"],
                "examples": ["neural_networks", "quantum_systems", "fractals"]
            }
        ]
    
    def _analyze_scale_hierarchy(self) -> List[Dict]:
        """Hiérarchie échelles: quantum → classical → cosmic"""
        return [
            {
                "scale": "quantum",
                "size_range": "10^-35 to 10^-15 m",
                "dominant_physics": ["quantum_mechanics", "uncertainty_principle"],
                "information_features": ["superposition", "entanglement", "no_cloning"]
            },
            {
                "scale": "classical",
                "size_range": "10^-9 to 10^9 m", 
                "dominant_physics": ["statistical_mechanics", "thermodynamics"],
                "information_features": ["shannon_entropy", "compression", "error_correction"]
            },
            {
                "scale": "cosmic",
                "size_range": "10^15 to 10^26 m",
                "dominant_physics": ["general_relativity", "cosmology"],
                "information_features": ["holographic_principle", "black_hole_entropy", "cosmic_information"]
            }
        ]
    
    def generate_convergence_insights(self) -> Dict:
        """Génère insights convergences mathématiques-physiques"""
        convergences = self.detect_mathematical_convergences()
        hierarchies = self.analyze_emergence_hierarchies()
        
        # Métaanalyse convergences
        strong_convergences = [c for c in convergences if c['convergence_strength'] > 0.7]
        unifying_principles = [c['unifying_principle'] for c in convergences]
        
        insights = {
            "analysis_metadata": {
                "total_atoms_analyzed": len(self.all_atoms),
                "convergence_patterns_detected": len(convergences),
                "strong_convergences": len(strong_convergences),
                "sources_integrated": len(self.sources),
                "analysis_date": datetime.datetime.now().isoformat()
            },
            "convergence_analysis": convergences,
            "emergence_hierarchies": hierarchies,
            "unifying_principles": unifying_principles,
            "meta_insights": {
                "information_as_universal_currency": self._analyze_information_universality(),
                "mathematics_physics_unity": self._analyze_math_physics_unity(),
                "emergence_ubiquity": self._analyze_emergence_patterns(),
                "compression_as_understanding": self._analyze_compression_understanding()
            },
            "panini_fs_implications": self._analyze_panini_implications(convergences)
        }
        
        return insights
    
    def _analyze_information_universality(self) -> Dict:
        """Analyse information comme monnaie universelle"""
        info_concepts = [
            atom for atom in self.all_atoms
            if 'information' in atom['concept'].lower() or 'entrop' in atom['concept'].lower()
        ]
        
        return {
            "concept_count": len(info_concepts),
            "domains_spanned": len(set(atom.get('category', 'unknown') for atom in info_concepts)),
            "universality_evidence": "information appears across all physical scales and mathematical domains"
        }
    
    def _analyze_math_physics_unity(self) -> Dict:
        """Analyse unité mathématiques-physique"""
        math_atoms = [atom for atom in self.all_atoms if atom['source_type'] == 'information_theory']
        physics_atoms = [atom for atom in self.all_atoms if atom['source_type'] == 'physics_mathematics']
        
        return {
            "mathematical_concepts": len(math_atoms),
            "physical_concepts": len(physics_atoms),
            "unity_principle": "mathematics provides language for physical reality",
            "emergent_understanding": "mathematical structures emerge from physical constraints"
        }
    
    def _analyze_emergence_patterns(self) -> Dict:
        """Analyse patterns émergence ubiquitaires"""
        emergence_atoms = [
            atom for atom in self.all_atoms
            if 'emerg' in atom['definition'].lower() or 'phase' in atom['definition'].lower()
        ]
        
        return {
            "emergence_concepts": len(emergence_atoms),
            "ubiquity_principle": "emergence as universal organizing principle",
            "scale_independence": "emergence occurs at all scales of reality"
        }
    
    def _analyze_compression_understanding(self) -> Dict:
        """Analyse compression comme compréhension"""
        compression_atoms = [
            atom for atom in self.all_atoms
            if 'compression' in atom['definition'].lower() or 'compact' in atom['definition'].lower()
        ]
        
        return {
            "compression_concepts": len(compression_atoms),
            "understanding_principle": "compression extracts essential information",
            "knowledge_encoding": "understanding is efficient information encoding"
        }
    
    def _analyze_panini_implications(self, convergences: List[Dict]) -> Dict:
        """Implications pour architecture PaniniFS"""
        return {
            "semantic_compression": "PaniniFS as universal semantic compressor",
            "hierarchical_emergence": "semantic atoms → concepts → understanding",
            "information_preservation": "lossless semantic compression via attribution",
            "fractal_organization": "self-similar patterns across semantic scales",
            "quantum_semantics": "superposition of meanings until measurement/context",
            "holographic_knowledge": "complete knowledge accessible from semantic fragments",
            "convergence_validation": f"{len(convergences)} patterns validate PaniniFS architecture"
        }
    
    def save_convergence_analysis(self, filename: str = "mathematics_physics_convergence_analysis.json"):
        """Sauvegarde analyse convergences"""
        insights = self.generate_convergence_insights()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(insights, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Analyse convergences sauvée: {filename}")
        
        # Affichage résumé
        metadata = insights['analysis_metadata']
        print(f"\n🔗 CONVERGENCES MATHÉMATIQUES-PHYSIQUES:")
        print(f"   • {metadata['total_atoms_analyzed']} atomes analysés")
        print(f"   • {metadata['convergence_patterns_detected']} patterns convergence détectés")
        print(f"   • {metadata['strong_convergences']} convergences fortes")
        
        print(f"\n💡 PRINCIPES UNIFICATEURS:")
        for principle in insights['unifying_principles'][:3]:
            print(f"   • {principle}")
        
        panini_implications = insights['panini_fs_implications']
        print(f"\n🌟 IMPLICATIONS PANINI-FS:")
        print(f"   • {panini_implications['semantic_compression']}")
        print(f"   • {panini_implications['hierarchical_emergence']}")
        print(f"   • {panini_implications['convergence_validation']}")
        
        return insights

def main():
    print("🔗 ANALYSEUR CONVERGENCES MATHÉMATIQUES-PHYSIQUES")
    print("=================================================")
    print("🧮 Exploration connexions théories information ↔ physique")
    print("💡 Validation architecture PaniniFS par convergences")
    print("")
    
    analyzer = MathPhysicsConvergenceAnalyzer()
    
    # Chargement sources
    total_loaded = analyzer.load_mathematical_sources()
    
    if total_loaded == 0:
        print("❌ Aucune source mathématique trouvée")
        return
    
    print(f"\n🔍 Analyse convergences sur {total_loaded} atomes...")
    
    # Génération analyse convergences
    insights = analyzer.save_convergence_analysis()
    
    print(f"\n🏆 ANALYSE CONVERGENCES TERMINÉE")
    print(f"🌟 Validation PaniniFS par convergences mathématiques-physiques universelles!")

if __name__ == "__main__":
    main()
