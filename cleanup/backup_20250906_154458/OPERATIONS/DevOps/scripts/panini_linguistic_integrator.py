#!/usr/bin/env python3
"""
Intégrateur PaniniFS-Langage : Connexion Encyclopédie ↔ Langue Optimale
🔗 Bridge entre FS sémantique et design langage neurocognitif optimal
"""

import json
import datetime
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict

@dataclass
class LinguisticOptimization:
    concept_id: str
    optimal_phonetic: str
    optimal_gestural: str
    optimal_visual: str
    cognitive_age: str
    analogical_foundation: str
    panini_semantic_atoms: List[str]

class PaniniLinguisticIntegrator:
    def __init__(self, base_path: str = "/home/stephane/GitHub/PaniniFS-1/scripts/scripts"):
        self.base_path = base_path
        self.panini_semantic_store = {}
        self.neurocognitive_constraints = {}
        self.optimal_vocabulary = {}
        self.linguistic_mappings = {}
        
    def load_panini_semantic_data(self) -> bool:
        """Chargement données sémantiques PaniniFS"""
        print("📚 CHARGEMENT DONNÉES SÉMANTIQUES PANINI...")
        
        # Recherche architecture unifiée la plus récente
        architecture_files = []
        for file in os.listdir(self.base_path):
            if file.startswith("panini_unified_architecture_") and file.endswith(".json"):
                full_path = os.path.join(self.base_path, file)
                mod_time = os.path.getmtime(full_path)
                architecture_files.append((file, mod_time, full_path))
        
        if architecture_files:
            latest_file = max(architecture_files, key=lambda x: x[1])
            try:
                with open(latest_file[2], 'r', encoding='utf-8') as f:
                    self.panini_semantic_store = json.load(f)
                print(f"   ✅ Architecture PaniniFS chargée: {latest_file[0]}")
                return True
            except Exception as e:
                print(f"   ❌ Erreur chargement: {e}")
        
        return False
    
    def load_neurocognitive_analysis(self) -> bool:
        """Chargement analyse neurocognitive"""
        print("🧠 CHARGEMENT ANALYSE NEUROCOGNITIVE...")
        
        # Recherche analyse neurocognitive la plus récente
        neuro_files = []
        for file in os.listdir(self.base_path):
            if file.startswith("neurocognitive_language_analysis_") and file.endswith(".json"):
                full_path = os.path.join(self.base_path, file)
                mod_time = os.path.getmtime(full_path)
                neuro_files.append((file, mod_time, full_path))
        
        if neuro_files:
            latest_file = max(neuro_files, key=lambda x: x[1])
            try:
                with open(latest_file[2], 'r', encoding='utf-8') as f:
                    self.neurocognitive_constraints = json.load(f)
                print(f"   ✅ Analyse neurocognitive chargée: {latest_file[0]}")
                return True
            except Exception as e:
                print(f"   ❌ Erreur chargement: {e}")
        
        return False
    
    def load_optimal_vocabulary(self) -> bool:
        """Chargement vocabulaire optimal"""
        print("📖 CHARGEMENT VOCABULAIRE OPTIMAL...")
        
        # Recherche prototype vocabulaire le plus récent
        vocab_files = []
        for file in os.listdir(self.base_path):
            if file.startswith("optimal_language_prototype_") and file.endswith(".json"):
                full_path = os.path.join(self.base_path, file)
                mod_time = os.path.getmtime(full_path)
                vocab_files.append((file, mod_time, full_path))
        
        if vocab_files:
            latest_file = max(vocab_files, key=lambda x: x[1])
            try:
                with open(latest_file[2], 'r', encoding='utf-8') as f:
                    self.optimal_vocabulary = json.load(f)
                print(f"   ✅ Vocabulaire optimal chargé: {latest_file[0]}")
                return True
            except Exception as e:
                print(f"   ❌ Erreur chargement: {e}")
        
        return False
    
    def analyze_semantic_concept_complexity(self) -> Dict[str, Any]:
        """Analyse complexité concepts sémantiques PaniniFS"""
        print("🔍 ANALYSE COMPLEXITÉ CONCEPTS SÉMANTIQUES...")
        
        if not self.panini_semantic_store:
            return {}
        
        atoms = self.panini_semantic_store.get("unified_semantic_atoms", {})
        
        complexity_analysis = {
            "concept_complexity_distribution": {},
            "component_complexity": {},
            "cognitive_age_mapping": {},
            "linguistic_readiness": {}
        }
        
        # Analyse par atome sémantique
        for atom_id, atom_data in atoms.items():
            concept = atom_data.get("concept", "unknown")
            definition = atom_data.get("definition", "")
            component = atom_data.get("component_source", "unknown")
            
            # Calcul complexité conceptuelle
            concept_complexity = self._calculate_concept_complexity(concept, definition, atom_data)
            
            # Mapping âge cognitif optimal
            cognitive_age = self._map_to_cognitive_age(concept_complexity, concept, definition)
            
            # Évaluation ready linguistique
            linguistic_readiness = self._assess_linguistic_readiness(concept, definition, concept_complexity)
            
            complexity_analysis["concept_complexity_distribution"][atom_id] = {
                "concept": concept,
                "complexity_score": concept_complexity,
                "cognitive_age": cognitive_age,
                "linguistic_readiness": linguistic_readiness,
                "component_source": component
            }
            
            # Agrégation par composant
            if component not in complexity_analysis["component_complexity"]:
                complexity_analysis["component_complexity"][component] = {
                    "total_concepts": 0,
                    "avg_complexity": 0,
                    "complexity_range": [10, 0]
                }
            
            comp_data = complexity_analysis["component_complexity"][component]
            comp_data["total_concepts"] += 1
            comp_data["avg_complexity"] = (comp_data["avg_complexity"] + concept_complexity) / 2
            comp_data["complexity_range"][0] = min(comp_data["complexity_range"][0], concept_complexity)
            comp_data["complexity_range"][1] = max(comp_data["complexity_range"][1], concept_complexity)
        
        return complexity_analysis
    
    def _calculate_concept_complexity(self, concept: str, definition: str, atom_data: Dict) -> float:
        """Calcul complexité conceptuelle"""
        complexity_score = 0.0
        
        # Complexité lexicale
        concept_words = len(concept.split())
        complexity_score += concept_words * 0.5
        
        # Complexité définition
        definition_words = len(definition.split())
        complexity_score += min(definition_words / 10, 2.0)
        
        # Complexité abstraite vs concrète
        abstract_keywords = ["théorie", "concept", "abstrait", "principe", "métaphore", "analogie"]
        concrete_keywords = ["objet", "action", "physique", "tangible", "observable"]
        
        abstract_count = sum(1 for keyword in abstract_keywords if keyword.lower() in definition.lower())
        concrete_count = sum(1 for keyword in concrete_keywords if keyword.lower() in definition.lower())
        
        if abstract_count > concrete_count:
            complexity_score += 2.0
        elif concrete_count > abstract_count:
            complexity_score += 0.5
        else:
            complexity_score += 1.0
        
        # Complexité domaine source
        component = atom_data.get("component_source", "")
        component_complexity = {
            "information_theory": 3.0,
            "physics_mathematics": 4.0,
            "convergence_analysis": 4.5,
            "autonomous_engine": 2.0,
            "analogy_safety": 3.5,
            "pattern_discovery": 3.0
        }
        complexity_score += component_complexity.get(component, 2.0)
        
        return min(complexity_score, 10.0)
    
    def _map_to_cognitive_age(self, complexity: float, concept: str, definition: str) -> str:
        """Mapping complexité vers âge cognitif optimal"""
        if complexity <= 2.0:
            return "2-4_years"
        elif complexity <= 4.0:
            return "4-7_years"
        elif complexity <= 6.0:
            return "7-12_years"
        elif complexity <= 8.0:
            return "12-16_years"
        else:
            return "16+_years"
    
    def _assess_linguistic_readiness(self, concept: str, definition: str, complexity: float) -> str:
        """Évaluation readiness linguistique"""
        if complexity <= 3.0 and len(concept.split()) <= 2:
            return "ready_for_optimization"
        elif complexity <= 5.0:
            return "needs_simplification"
        else:
            return "requires_scaffolding"
    
    def generate_concept_linguistic_mappings(self) -> Dict[str, Any]:
        """Génération mappings linguistiques pour concepts PaniniFS"""
        print("🔗 GÉNÉRATION MAPPINGS LINGUISTIQUES...")
        
        complexity_analysis = self.analyze_semantic_concept_complexity()
        
        if not complexity_analysis:
            return {}
        
        linguistic_mappings = {
            "optimized_concepts": {},
            "age_stratified_vocabulary": {},
            "multimodal_representations": {},
            "analogical_progressions": {}
        }
        
        # Traitement chaque concept
        for atom_id, concept_data in complexity_analysis["concept_complexity_distribution"].items():
            concept = concept_data["concept"]
            cognitive_age = concept_data["cognitive_age"]
            readiness = concept_data["linguistic_readiness"]
            
            if readiness == "ready_for_optimization":
                # Génération représentation linguistique optimale
                optimal_rep = self._generate_optimal_representation(concept, cognitive_age)
                linguistic_mappings["optimized_concepts"][atom_id] = optimal_rep
            
            # Stratification par âge
            if cognitive_age not in linguistic_mappings["age_stratified_vocabulary"]:
                linguistic_mappings["age_stratified_vocabulary"][cognitive_age] = []
            
            linguistic_mappings["age_stratified_vocabulary"][cognitive_age].append({
                "atom_id": atom_id,
                "concept": concept,
                "complexity": concept_data["complexity_score"],
                "readiness": readiness
            })
        
        # Génération progressions analogiques
        linguistic_mappings["analogical_progressions"] = self._generate_analogical_progressions(
            complexity_analysis["concept_complexity_distribution"]
        )
        
        return linguistic_mappings
    
    def _generate_optimal_representation(self, concept: str, cognitive_age: str) -> Dict[str, str]:
        """Génération représentation linguistique optimale"""
        
        # Simplification phonétique basée âge
        phonetic_simplifications = {
            "2-4_years": {
                "entropy": "entro",
                "information": "info", 
                "quantum": "kwant",
                "fractal": "fraktal"
            },
            "4-7_years": {
                "convergence": "konverj",
                "emergence": "emerj",
                "complexity": "komplex"
            },
            "7-12_years": {
                "thermodynamic": "termo",
                "holographic": "holo",
                "statistical": "stat"
            }
        }
        
        concept_lower = concept.lower()
        phonetic_form = concept_lower
        
        for age, simplifications in phonetic_simplifications.items():
            if age == cognitive_age:
                for full_word, simplified in simplifications.items():
                    if full_word in concept_lower:
                        phonetic_form = concept_lower.replace(full_word, simplified)
                        break
        
        # Génération forme gestuelle
        gestural_mapping = {
            "information": "hand_to_head",
            "entropy": "spreading_fingers",
            "quantum": "quantum_hand_position",
            "fractal": "recursive_gesture",
            "emergence": "opening_hands",
            "convergence": "hands_coming_together"
        }
        
        gestural_form = "generic_concept_gesture"
        for keyword, gesture in gestural_mapping.items():
            if keyword in concept_lower:
                gestural_form = gesture
                break
        
        # Génération symbole visuel
        visual_mapping = {
            "information": "ℹ️",
            "entropy": "📊",
            "quantum": "⚛️",
            "fractal": "🌀",
            "emergence": "✨",
            "convergence": "🔗"
        }
        
        visual_symbol = "🔺"  # symbole générique
        for keyword, symbol in visual_mapping.items():
            if keyword in concept_lower:
                visual_symbol = symbol
                break
        
        return {
            "original_concept": concept,
            "phonetic_form": phonetic_form,
            "gestural_form": gestural_form,
            "visual_symbol": visual_symbol,
            "cognitive_age": cognitive_age
        }
    
    def _generate_analogical_progressions(self, concepts: Dict) -> Dict[str, Any]:
        """Génération progressions analogiques entre concepts"""
        
        progressions = {
            "concrete_to_abstract": [],
            "simple_to_complex": [],
            "domain_bridges": []
        }
        
        # Identification concepts concrets vs abstraits
        concrete_concepts = []
        abstract_concepts = []
        
        for atom_id, data in concepts.items():
            if data["complexity_score"] <= 3.0:
                concrete_concepts.append((atom_id, data))
            else:
                abstract_concepts.append((atom_id, data))
        
        # Création bridges concret→abstrait
        for concrete_id, concrete_data in concrete_concepts:
            for abstract_id, abstract_data in abstract_concepts:
                similarity = self._calculate_conceptual_similarity(
                    concrete_data["concept"], 
                    abstract_data["concept"]
                )
                
                if similarity > 0.3:
                    progressions["concrete_to_abstract"].append({
                        "concrete_concept": concrete_data["concept"],
                        "abstract_concept": abstract_data["concept"],
                        "similarity_score": similarity,
                        "suggested_bridge": f"Like {concrete_data['concept']} but more complex"
                    })
        
        return progressions
    
    def _calculate_conceptual_similarity(self, concept1: str, concept2: str) -> float:
        """Calcul similarité conceptuelle simple"""
        words1 = set(concept1.lower().split())
        words2 = set(concept2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def integrate_with_developmental_vocabulary(self) -> Dict[str, Any]:
        """Intégration avec vocabulaire développemental optimal"""
        print("🎯 INTÉGRATION VOCABULAIRE DÉVELOPPEMENTAL...")
        
        if not self.optimal_vocabulary:
            return {}
        
        linguistic_mappings = self.generate_concept_linguistic_mappings()
        
        integration = {
            "enhanced_developmental_stages": {},
            "panini_concept_insertions": {},
            "cross_modal_synergies": {},
            "cognitive_scaffolding_paths": {}
        }
        
        # Enrichissement stades développementaux avec concepts PaniniFS
        vocab_progression = self.optimal_vocabulary.get("vocabulary_progression", {})
        
        for stage_name, stage_data in vocab_progression.items():
            age_range = stage_data.get("age_range", "")
            
            # Mapping âge développemental vers concepts PaniniFS appropriés
            appropriate_concepts = []
            
            for age_category, concepts_list in linguistic_mappings.get("age_stratified_vocabulary", {}).items():
                if self._age_ranges_overlap(age_range, age_category):
                    for concept_data in concepts_list:
                        if concept_data["readiness"] == "ready_for_optimization":
                            appropriate_concepts.append(concept_data)
            
            integration["enhanced_developmental_stages"][stage_name] = {
                "original_vocabulary_size": stage_data.get("total_words", 0),
                "panini_concepts_added": len(appropriate_concepts),
                "enhanced_total": stage_data.get("total_words", 0) + len(appropriate_concepts),
                "added_concepts": appropriate_concepts[:5]  # Limite pour lisibilité
            }
        
        # Identification synergies cross-modales
        integration["cross_modal_synergies"] = self._identify_cross_modal_synergies()
        
        return integration
    
    def _age_ranges_overlap(self, range1: str, range2: str) -> bool:
        """Vérification chevauchement tranches d'âge"""
        # Extraction numérique simple des ranges (approximation)
        def extract_age_number(age_range):
            import re
            numbers = re.findall(r'\d+', age_range)
            return int(numbers[0]) if numbers else 0
        
        age1 = extract_age_number(range1)
        age2 = extract_age_number(range2)
        
        return abs(age1 - age2) <= 2  # Tolérance 2 ans
    
    def _identify_cross_modal_synergies(self) -> List[Dict]:
        """Identification synergies cross-modales"""
        return [
            {
                "synergy_type": "gesture_phonetic",
                "description": "Gestes renforcent apprentissage phonétique",
                "example": "Gesture 'spreading' + phonetic 'entropy' = enhanced retention"
            },
            {
                "synergy_type": "visual_semantic",
                "description": "Symboles visuels clarifient concepts abstraits",
                "example": "Symbol ⚛️ + concept 'quantum' = concrete anchor"
            },
            {
                "synergy_type": "analogical_scaffolding",
                "description": "Progressions analogiques facilitent complexification",
                "example": "Concrete 'spreading water' → abstract 'entropy increase'"
            }
        ]
    
    def generate_panini_linguistic_enhancement_report(self) -> Dict[str, Any]:
        """Génération rapport enhancement linguistique PaniniFS"""
        print("📊 GÉNÉRATION RAPPORT ENHANCEMENT LINGUISTIQUE...")
        
        # Collecte toutes analyses
        complexity_analysis = self.analyze_semantic_concept_complexity()
        linguistic_mappings = self.generate_concept_linguistic_mappings()
        developmental_integration = self.integrate_with_developmental_vocabulary()
        
        report = {
            "enhancement_metadata": {
                "generation_date": datetime.datetime.now().isoformat(),
                "panini_concepts_analyzed": len(complexity_analysis.get("concept_complexity_distribution", {})),
                "optimization_scope": "Neurocognitive language optimization for PaniniFS concepts",
                "integration_framework": "Developmental vocabulary + semantic encyclopedia"
            },
            "concept_complexity_analysis": complexity_analysis,
            "linguistic_optimizations": linguistic_mappings,
            "developmental_integration": developmental_integration,
            "enhancement_opportunities": {
                "immediate_optimizations": self._identify_immediate_optimizations(complexity_analysis),
                "long_term_enhancements": self._identify_long_term_enhancements(),
                "multimodal_expansions": self._identify_multimodal_expansions()
            },
            "implementation_roadmap": {
                "phase_1_concept_simplification": "Optimize high-readiness concepts",
                "phase_2_analogical_bridges": "Create concrete→abstract progressions", 
                "phase_3_multimodal_integration": "Deploy gesture+visual+phonetic systems",
                "phase_4_developmental_testing": "Validate with target age groups"
            }
        }
        
        return report
    
    def _identify_immediate_optimizations(self, complexity_analysis: Dict) -> List[Dict]:
        """Identification optimisations immédiates"""
        optimizations = []
        
        for atom_id, data in complexity_analysis.get("concept_complexity_distribution", {}).items():
            if data.get("linguistic_readiness") == "ready_for_optimization":
                optimizations.append({
                    "concept": data["concept"],
                    "current_complexity": data["complexity_score"],
                    "target_age": data["cognitive_age"],
                    "optimization_type": "phonetic_gestural_visual"
                })
        
        return optimizations[:10]  # Top 10
    
    def _identify_long_term_enhancements(self) -> List[str]:
        """Identification enhancements long terme"""
        return [
            "Développement système écriture évolutive (pictographique→idéographique→alphabétique)",
            "Création grammaire spatiale 3D pour concepts physiques complexes",
            "Intégration réalité augmentée pour visualisation concepts abstraits",
            "Développement assistant IA adaptatif progression cognitive individuelle",
            "Recherche empirique validation efficacité apprentissage"
        ]
    
    def _identify_multimodal_expansions(self) -> List[str]:
        """Identification expansions multimodales"""
        return [
            "Système gestuel scientifique pour équations mathématiques",
            "Notation visuelle universelle pour concepts physiques",
            "Interface haptique pour concepts kinesthésiques",
            "Système sonification pour structures de données complexes",
            "Réalité virtuelle pour exploration concepts 4D+"
        ]
    
    def save_integration_report(self, output_path: str = None) -> str:
        """Sauvegarde rapport intégration"""
        if not output_path:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"/home/stephane/GitHub/PaniniFS-1/scripts/scripts/panini_linguistic_integration_{timestamp}.json"
        
        report = self.generate_panini_linguistic_enhancement_report()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Rapport intégration sauvegardé: {output_path}")
        return output_path

def main():
    print("🔗 INTÉGRATEUR PANINI-FS ↔ LANGAGE OPTIMAL")
    print("=" * 50)
    print("🎯 Bridge encyclopédie sémantique ↔ design linguistique neurocognitif")
    print("📚 PaniniFS concepts → optimisation développementale")
    print("")
    
    integrator = PaniniLinguisticIntegrator()
    
    # Chargement données
    print("📊 CHARGEMENT DONNÉES...")
    panini_loaded = integrator.load_panini_semantic_data()
    neuro_loaded = integrator.load_neurocognitive_analysis()
    vocab_loaded = integrator.load_optimal_vocabulary()
    
    if not all([panini_loaded, neuro_loaded, vocab_loaded]):
        print("❌ Impossible de charger toutes les données nécessaires")
        return
    
    # Génération rapport intégration
    report = integrator.generate_panini_linguistic_enhancement_report()
    
    # Affichage résultats clés
    metadata = report["enhancement_metadata"]
    print(f"\n📊 ANALYSE CONCEPTS PANINI:")
    print(f"   Concepts analysés: {metadata['panini_concepts_analyzed']}")
    
    complexity = report["concept_complexity_analysis"]
    if complexity:
        total_concepts = len(complexity.get("concept_complexity_distribution", {}))
        ready_concepts = sum(1 for data in complexity.get("concept_complexity_distribution", {}).values() 
                           if data.get("linguistic_readiness") == "ready_for_optimization")
        print(f"   Prêts optimisation: {ready_concepts}/{total_concepts}")
    
    # Affichage composants par complexité
    if "component_complexity" in complexity:
        print(f"\n🧠 COMPLEXITÉ PAR COMPOSANT:")
        for component, data in complexity["component_complexity"].items():
            print(f"   {component}: {data['avg_complexity']:.1f}/10 (range {data['complexity_range'][0]:.1f}-{data['complexity_range'][1]:.1f})")
    
    # Affichage intégration développementale
    developmental = report["developmental_integration"]
    if "enhanced_developmental_stages" in developmental:
        print(f"\n👶 INTÉGRATION DÉVELOPPEMENTALE:")
        for stage, data in developmental["enhanced_developmental_stages"].items():
            stage_display = stage.replace("_", " ").title()
            print(f"   {stage_display}: +{data['panini_concepts_added']} concepts PaniniFS")
    
    # Affichage opportunités
    opportunities = report["enhancement_opportunities"]
    print(f"\n🚀 OPPORTUNITÉS ENHANCEMENT:")
    immediate = opportunities.get("immediate_optimizations", [])
    print(f"   Optimisations immédiates: {len(immediate)} concepts")
    
    if immediate:
        print(f"   Top concepts prêts:")
        for opt in immediate[:3]:
            print(f"     • {opt['concept']} (âge: {opt['target_age']})")
    
    # Sauvegarde
    report_path = integrator.save_integration_report()
    
    print(f"\n🏆 INTÉGRATION PANINI-LANGAGE COMPLÈTE")
    print(f"📚 Encyclopédie sémantique analysée pour optimisation linguistique")
    print(f"🧠 Concepts mappés vers contraintes neurocognitives développementales")
    print(f"🎯 Bridge fonctionnel entre FS et langage optimal créé")
    print(f"📁 Rapport: {report_path.split('/')[-1]}")

if __name__ == "__main__":
    main()
