#!/usr/bin/env python3
"""
Collecteur Théories Information - Shannon et successeurs
🧮 Exploration théories information, compression, fractales pour PaniniFS
"""

import json
import datetime
from typing import List, Dict, Any
import re
import os

class InformationTheoryCollector:
    def __init__(self):
        self.store = {
            "metadata": {
                "version": "1.0",
                "description": "Collecte théories information, compression, fractales",
                "creation_date": datetime.datetime.now().isoformat(),
                "source_type": "information_theory",
                "focus_areas": ["shannon_theory", "compression_algorithms", "fractal_geometry", "emergence_theory"]
            },
            "semantic_atoms": []
        }
    
    def collect_shannon_fundamentals(self) -> List[Dict]:
        """Concepts fondamentaux de Shannon et théorie information"""
        concepts = [
            {
                "concept": "Entropie Informationnelle",
                "definition": "Mesure quantitative de l'incertitude contenue dans un message, H(X) = -Σ p(x) log₂ p(x), fondement de la théorie de l'information",
                "category": "shannon_theory",
                "mathematical_form": "H(X) = -Σ p(x) log₂ p(x)",
                "breakthrough_year": 1948,
                "relevance_score": 0.98
            },
            {
                "concept": "Capacité de Canal",
                "definition": "Maximum d'information transmissible par unité de temps sur un canal bruité, C = B log₂(1 + S/N) selon théorème Shannon-Hartley",
                "category": "shannon_theory", 
                "mathematical_form": "C = B log₂(1 + S/N)",
                "breakthrough_year": 1948,
                "relevance_score": 0.95
            },
            {
                "concept": "Information Mutuelle",
                "definition": "Quantité d'information commune entre deux variables aléatoires, I(X;Y) = H(X) + H(Y) - H(X,Y), mesure dépendance informationnelle",
                "category": "shannon_theory",
                "mathematical_form": "I(X;Y) = H(X) + H(Y) - H(X,Y)",
                "breakthrough_year": 1948,
                "relevance_score": 0.93
            },
            {
                "concept": "Complexité de Kolmogorov",
                "definition": "Longueur minimale d'un programme informatique capable de produire une chaîne donnée, mesure absolue de complexité informationnelle",
                "category": "algorithmic_information",
                "mathematical_form": "K(x) = min{|p| : U(p) = x}",
                "breakthrough_year": 1965,
                "relevance_score": 0.96
            },
            {
                "concept": "Entropie Différentielle",
                "definition": "Extension de l'entropie de Shannon aux variables continues, h(X) = -∫ f(x) log f(x) dx, fondement pour signaux analogiques",
                "category": "continuous_information",
                "mathematical_form": "h(X) = -∫ f(x) log f(x) dx",
                "breakthrough_year": 1948,
                "relevance_score": 0.91
            }
        ]
        
        return self._convert_to_atoms(concepts, "shannon_fundamentals")
    
    def collect_compression_algorithms(self) -> List[Dict]:
        """Algorithmes compression - extracteurs essence information"""
        concepts = [
            {
                "concept": "Compression LZ77",
                "definition": "Algorithme compression sans perte utilisant fenêtre glissante pour trouver répétitions, base de formats ZIP et GZIP",
                "category": "lossless_compression",
                "algorithm_family": "dictionary_based",
                "compression_ratio": "2:1 à 8:1",
                "relevance_score": 0.89
            },
            {
                "concept": "Transformée Cosinus Discrète",
                "definition": "Transformation mathématique DCT = Σ f(x) cos(πn(x+0.5)/N) concentrant énergie signal sur basses fréquences, cœur JPEG/MP3",
                "category": "lossy_compression",
                "mathematical_form": "DCT(k) = Σ f(x) cos(πk(x+0.5)/N)",
                "applications": ["JPEG", "MP3", "MPEG"],
                "relevance_score": 0.94
            },
            {
                "concept": "Codage Huffman",
                "definition": "Algorithme codage entropique optimal assignant codes courts aux symboles fréquents, atteignant limite théorique Shannon",
                "category": "entropy_coding",
                "optimality": "optimal_for_symbol_probabilities",
                "theoretical_limit": "shannon_entropy",
                "relevance_score": 0.92
            },
            {
                "concept": "Ondelettes Daubechies",
                "definition": "Famille ondelettes orthogonales à support compact, permettant analyse multi-résolution avec localisation temps-fréquence",
                "category": "wavelet_compression",
                "mathematical_property": "orthogonal_compact_support",
                "applications": ["JPEG2000", "audio_compression"],
                "relevance_score": 0.88
            },
            {
                "concept": "Quantification Vectorielle",
                "definition": "Technique compression groupant vecteurs similaires en codes représentatifs, exploitant corrélations multi-dimensionnelles",
                "category": "vector_quantization",
                "dimension_reduction": "high_dimensional_clustering",
                "applications": ["speech_coding", "image_compression"],
                "relevance_score": 0.85
            },
            {
                "concept": "Prédiction Linéaire",
                "definition": "Modélisation signal comme combinaison linéaire échantillons précédents, base compression audio sans perte FLAC",
                "category": "predictive_coding",
                "mathematical_form": "x̂(n) = Σ aᵢ x(n-i)",
                "applications": ["FLAC", "speech_coding"],
                "relevance_score": 0.87
            }
        ]
        
        return self._convert_to_atoms(concepts, "compression_algorithms")
    
    def collect_fractal_geometry(self) -> List[Dict]:
        """Géométrie fractale - structures émergentes auto-similaires"""
        concepts = [
            {
                "concept": "Dimension Fractale",
                "definition": "Mesure non-entière de complexité géométrique, D = log(N)/log(r) où N objets à échelle r, révèle structure auto-similaire",
                "category": "fractal_geometry",
                "mathematical_form": "D = log(N)/log(r)",
                "breakthrough_year": 1967,
                "relevance_score": 0.94
            },
            {
                "concept": "Ensemble de Mandelbrot",
                "definition": "Ensemble fractal défini par itération z_{n+1} = z_n² + c, frontière révélant complexité infinie à toutes échelles",
                "category": "complex_dynamics",
                "mathematical_form": "z_{n+1} = z_n² + c",
                "dimensional_properties": "fractal_boundary",
                "relevance_score": 0.91
            },
            {
                "concept": "Attracteur Étrange",
                "definition": "Structure fractale vers laquelle évolue système dynamique chaotique, combine attraction et sensibilité conditions initiales",
                "category": "chaos_theory",
                "properties": ["attraction", "fractal_structure", "sensitive_dependence"],
                "examples": ["lorenz_attractor", "henon_map"],
                "relevance_score": 0.93
            },
            {
                "concept": "Compression Fractale",
                "definition": "Technique compression exploitant auto-similarité images via transformations affines contractantes, théorème point fixe Banach",
                "category": "fractal_compression",
                "mathematical_basis": "banach_fixed_point_theorem",
                "compression_approach": "self_similarity_encoding",
                "relevance_score": 0.86
            },
            {
                "concept": "Mouvement Brownien Fractionnaire",
                "definition": "Processus stochastique auto-similaire avec paramètre Hurst H, généralise mouvement brownien avec mémoire longue",
                "category": "stochastic_fractals",
                "mathematical_form": "fBm(H), 0 < H < 1",
                "memory_property": "long_range_dependence",
                "relevance_score": 0.89
            },
            {
                "concept": "Mesure Hausdorff",
                "definition": "Généralisation notion mesure pour ensembles fractals, μ_H(E) = lim inf Σ (diam Uᵢ)^s où E ⊂ ∪Uᵢ",
                "category": "measure_theory",
                "mathematical_form": "μ_H(E) = lim inf Σ (diam Uᵢ)^s",
                "applications": ["fractal_dimension", "geometric_measure"],
                "relevance_score": 0.88
            }
        ]
        
        return self._convert_to_atoms(concepts, "fractal_geometry")
    
    def collect_emergence_theories(self) -> List[Dict]:
        """Théories émergence - complexité issue de simplicité"""
        concepts = [
            {
                "concept": "Émergence Forte",
                "definition": "Propriétés système non réductibles aux propriétés composants, créant nouveaux niveaux causalité descendante",
                "category": "emergence_theory",
                "causality_type": "downward_causation",
                "irreducibility": "non_reductive",
                "relevance_score": 0.92
            },
            {
                "concept": "Transition de Phase",
                "definition": "Changement qualitatif comportement système à paramètre critique, émergence ordre macroscopique depuis désordre microscopique",
                "category": "phase_transitions",
                "emergence_type": "macroscopic_order",
                "critical_phenomena": "universality_classes",
                "relevance_score": 0.90
            },
            {
                "concept": "Auto-Organisation Critique",
                "definition": "Tendance systèmes complexes évoluer vers état critique sans réglage externe, émergence lois puissance universelles",
                "category": "self_organization",
                "mathematical_signature": "power_laws",
                "examples": ["sandpile_model", "forest_fires"],
                "relevance_score": 0.91
            },
            {
                "concept": "Percolation",
                "definition": "Transition phase géométrique où connectivité globale émerge à seuil critique pc, métaphore émergence propriétés collectives",
                "category": "percolation_theory",
                "critical_parameter": "percolation_threshold",
                "emergence_property": "infinite_cluster",
                "relevance_score": 0.87
            },
            {
                "concept": "Réseaux Complexes",
                "definition": "Structures topologiques exhibant propriétés émergentes: petit monde, invariance échelle, communautés auto-organisées",
                "category": "network_science",
                "emergent_properties": ["small_world", "scale_free", "clustering"],
                "applications": ["social_networks", "brain_networks"],
                "relevance_score": 0.89
            }
        ]
        
        return self._convert_to_atoms(concepts, "emergence_theories")
    
    def _convert_to_atoms(self, concepts: List[Dict], collection_type: str) -> List[Dict]:
        """Conversion concepts en atomes sémantiques standardisés"""
        atoms = []
        
        for i, concept_data in enumerate(concepts):
            atom = {
                "concept": concept_data["concept"],
                "definition": concept_data["definition"],
                "category": concept_data["category"],
                "metadata": {
                    key: value for key, value in concept_data.items() 
                    if key not in ["concept", "definition", "category"]
                },
                "provenance": {
                    "source_agent": "information_theory_collector",
                    "timestamp": datetime.datetime.now().isoformat(),
                    "extraction_confidence": concept_data.get("relevance_score", 0.85),
                    "collection_method": f"structured_{collection_type}",
                    "atom_id": f"info_theory_{datetime.datetime.now().strftime('%Y%m%d')}_{collection_type}_{i:03d}"
                }
            }
            atoms.append(atom)
        
        return atoms
    
    def collect_all_domains(self) -> List[Dict]:
        """Collection complète tous domaines théories information"""
        all_atoms = []
        
        print("🧮 Collecte théories Shannon...")
        all_atoms.extend(self.collect_shannon_fundamentals())
        
        print("🗜️  Collecte algorithmes compression...")
        all_atoms.extend(self.collect_compression_algorithms())
        
        print("🌀 Collecte géométrie fractale...")
        all_atoms.extend(self.collect_fractal_geometry())
        
        print("⭐ Collecte théories émergence...")
        all_atoms.extend(self.collect_emergence_theories())
        
        return all_atoms
    
    def save_collection(self, filename: str = "information_theory_semantic_store.json"):
        """Sauvegarde collection théories information"""
        atoms = self.collect_all_domains()
        self.store["semantic_atoms"] = atoms
        self.store["metadata"]["total_atoms"] = len(atoms)
        
        # Statistiques par domaine
        domain_stats = {}
        for atom in atoms:
            category = atom["category"]
            domain_stats[category] = domain_stats.get(category, 0) + 1
        
        self.store["metadata"]["domain_distribution"] = domain_stats
        self.store["metadata"]["mathematical_concepts"] = len([
            atom for atom in atoms 
            if "mathematical_form" in atom.get("metadata", {})
        ])
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.store, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Collection théories information sauvée: {filename}")
        print(f"📊 {len(atoms)} concepts collectés")
        print(f"🧮 Domaines couverts: {list(domain_stats.keys())}")
        print(f"🔢 Concepts mathématiques: {self.store['metadata']['mathematical_concepts']}")
        
        return len(atoms)

def main():
    print("🧮 COLLECTEUR THÉORIES INFORMATION")
    print("==================================")
    print("🎯 Shannon, compression, fractales, émergence")
    print("💡 Exploration mathématiques pour PaniniFS")
    print("")
    
    collector = InformationTheoryCollector()
    total_collected = collector.save_collection()
    
    print(f"\n🏆 COLLECTION TERMINÉE")
    print(f"📈 {total_collected} concepts mathématiques intégrés")
    print(f"🌟 Élargissement horizon PaniniFS vers domaines fondamentaux!")

if __name__ == "__main__":
    main()
