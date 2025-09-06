#!/usr/bin/env python3
"""
Analyseur Neurocognitif pour Langage Optimal
🧠 Étude contraintes cerveau humain + développement cognitif pour langue construite
"""

import json
import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

class DevelopmentalStage(Enum):
    INFANT_0_6M = "infant_0_6_months"
    INFANT_6_12M = "infant_6_12_months"
    TODDLER_1_2Y = "toddler_1_2_years"
    PRESCHOOL_2_4Y = "preschool_2_4_years"
    CHILD_4_7Y = "child_4_7_years"
    SCHOOL_7_12Y = "school_7_12_years"
    ADOLESCENT_12_18Y = "adolescent_12_18_years"
    ADULT_18PLUS = "adult_18_plus"

class CognitiveCapacity(Enum):
    AUDITORY_PROCESSING = "auditory_processing"
    PHONATORY_MOTOR = "phonatory_motor"
    ECHOIC_MEMORY = "echoic_memory"
    WORKING_MEMORY = "working_memory"
    SEMANTIC_MEMORY = "semantic_memory"
    VISUAL_PROCESSING = "visual_processing"
    MOTOR_COORDINATION = "motor_coordination"
    ABSTRACT_REASONING = "abstract_reasoning"

@dataclass
class NeurocognitiveConstraint:
    capacity_type: CognitiveCapacity
    developmental_stage: DevelopmentalStage
    limit_value: float
    limit_unit: str
    description: str
    implications_for_language: List[str]

@dataclass
class PhonatoryCapability:
    age_range: str
    vowel_capacity: List[str]
    consonant_capacity: List[str]
    syllable_complexity: int
    vocal_range_hz: Tuple[float, float]
    articulation_precision: float

@dataclass
class CognitiveLanguageFeature:
    feature_name: str
    minimum_age: str
    cognitive_prerequisites: List[str]
    complexity_level: int
    analogical_foundation: str
    mnemonic_aids: List[str]

class NeurocognitiveLinguisticAnalyzer:
    def __init__(self):
        self.constraints_database = {}
        self.developmental_capabilities = {}
        self.phonatory_evolution = {}
        self.piaget_stages = {}
        
    def analyze_auditory_constraints(self) -> Dict[str, Any]:
        """Analyse contraintes système auditif humain"""
        print("👂 ANALYSE CONTRAINTES AUDITIVES...")
        
        auditory_constraints = {
            "frequency_range": {
                "human_hearing": "20 Hz - 20,000 Hz",
                "speech_critical": "200 Hz - 8,000 Hz",
                "optimal_recognition": "500 Hz - 4,000 Hz",
                "baby_preference": "100 Hz - 500 Hz (maternal voice)",
                "implications": [
                    "Fréquences fondamentales optimales: 100-500 Hz",
                    "Harmoniques critiques: jusqu'à 4 kHz",
                    "Éviter fréquences > 8 kHz pour phonèmes essentiels"
                ]
            },
            "temporal_processing": {
                "phoneme_discrimination": "40-50 ms minimum",
                "syllable_boundary": "100-200 ms",
                "echoic_memory_duration": "2-4 seconds",
                "working_memory_span": "7±2 items",
                "implications": [
                    "Durée minimale phonèmes: 50 ms",
                    "Pause syllabique: 100-200 ms",
                    "Séquences maximales: 7 éléments",
                    "Répétition nécessaire si > 4 secondes"
                ]
            },
            "masking_effects": {
                "forward_masking": "50-200 ms",
                "backward_masking": "20-50 ms",
                "simultaneous_masking": "frequency dependent",
                "implications": [
                    "Éviter phonèmes similaires consécutifs",
                    "Espacement temporel minimum: 200 ms",
                    "Contraste fréquentiel pour distinctivité"
                ]
            }
        }
        
        return auditory_constraints
    
    def analyze_phonatory_constraints(self) -> Dict[str, Any]:
        """Analyse contraintes appareil phonatoire"""
        print("🗣️ ANALYSE CONTRAINTES PHONATOIRES...")
        
        phonatory_constraints = {
            "articulatory_development": {
                "0-6_months": {
                    "vowels": ["a", "e", "o"],
                    "consonants": ["m", "b", "p"],
                    "syllable_types": ["CV", "V"],
                    "max_syllables": 1,
                    "vocal_range": (100, 400)
                },
                "6-12_months": {
                    "vowels": ["a", "e", "i", "o", "u"],
                    "consonants": ["m", "b", "p", "d", "t", "n"],
                    "syllable_types": ["CV", "VC", "CVC"],
                    "max_syllables": 2,
                    "vocal_range": (100, 500)
                },
                "12-24_months": {
                    "vowels": ["a", "e", "i", "o", "u", "ə"],
                    "consonants": ["m", "b", "p", "d", "t", "n", "k", "g", "f", "s"],
                    "syllable_types": ["CV", "VC", "CVC", "CVCV"],
                    "max_syllables": 3,
                    "vocal_range": (80, 600)
                },
                "2-4_years": {
                    "vowels": "full vowel system",
                    "consonants": "most consonants except complex clusters",
                    "syllable_types": ["complex syllables possible"],
                    "max_syllables": 4,
                    "vocal_range": (80, 800)
                }
            },
            "motor_coordination": {
                "fine_motor_development": {
                    "0-2_years": "gross articulatory movements",
                    "2-4_years": "refined coordination emerging",
                    "4-7_years": "precise articulation developing",
                    "7+_years": "adult-like precision"
                },
                "coarticulation_ability": {
                    "simple": "2-3 years",
                    "complex": "5-7 years",
                    "fluent": "7+ years"
                }
            }
        }
        
        return phonatory_constraints
    
    def analyze_memory_constraints(self) -> Dict[str, Any]:
        """Analyse contraintes mémoire et traitement"""
        print("🧠 ANALYSE CONTRAINTES MÉMOIRE...")
        
        memory_constraints = {
            "echoic_memory": {
                "duration": "2-4 seconds",
                "capacity": "unlimited within duration",
                "decay_rate": "exponential",
                "implications": [
                    "Unités linguistiques < 4 secondes",
                    "Répétition nécessaire pour consolidation",
                    "Structure rythmique aide rétention"
                ]
            },
            "working_memory": {
                "phonological_loop": {
                    "capacity": "2 seconds of speech",
                    "rehearsal_rate": "1.5-2 words/second",
                    "developmental": {
                        "3-4_years": "2-3 items",
                        "5-6_years": "3-4 items", 
                        "7-8_years": "4-5 items",
                        "adult": "7±2 items"
                    }
                },
                "visuospatial_sketchpad": {
                    "capacity": "3-4 visual objects",
                    "duration": "15-30 seconds",
                    "implications": [
                        "Signes visuels: max 4 éléments simultanés",
                        "Séquences gestuelles: durée limitée",
                        "Répétition spatiale nécessaire"
                    ]
                }
            },
            "long_term_memory": {
                "semantic_network": {
                    "formation": "progressive par associations",
                    "retrieval_cues": "multiple pathways optimal",
                    "consolidation_time": "hours to years"
                },
                "procedural_memory": {
                    "motor_patterns": "automatization through repetition",
                    "linguistic_patterns": "grammar internalization"
                }
            }
        }
        
        return memory_constraints
    
    def analyze_piaget_stages(self) -> Dict[str, Any]:
        """Analyse stades développement cognitif Piaget + successeurs"""
        print("👶 ANALYSE STADES DÉVELOPPEMENT PIAGET...")
        
        piaget_stages = {
            "sensorimotor_stage": {
                "age_range": "0-2 years",
                "key_capabilities": [
                    "Coordination sensorielle-motrice",
                    "Permanence objet émergente",
                    "Imitation différée tardive",
                    "Premiers symboles mentaux"
                ],
                "language_implications": [
                    "Mots liés actions immédiates",
                    "Vocabulaire concret sensoriel",
                    "Gestes précèdent parole",
                    "Associations directes besoins-symboles"
                ],
                "optimal_vocabulary": [
                    "mama", "papa", "milk", "up", "more",
                    "bye-bye", "no", "yes", "hot", "ouch"
                ]
            },
            "preoperational_stage": {
                "age_range": "2-7 years",
                "key_capabilities": [
                    "Pensée symbolique développée",
                    "Langage représentationnel",
                    "Pensée intuitive non-logique",
                    "Centration cognitive",
                    "Animisme et artificialisme"
                ],
                "language_implications": [
                    "Métaphores simples possibles",
                    "Analogies concrètes efficaces",
                    "Personnification naturelle",
                    "Catégorisation perceptuelle"
                ],
                "optimal_structures": [
                    "Comparaisons sensorielles",
                    "Métaphores animales",
                    "Associations visuelles",
                    "Rythmes et répétitions"
                ]
            },
            "concrete_operational": {
                "age_range": "7-11 years",
                "key_capabilities": [
                    "Opérations logiques concrètes",
                    "Conservation et réversibilité",
                    "Classification hiérarchique",
                    "Sériation et correspondance"
                ],
                "language_implications": [
                    "Grammaire logique accessible",
                    "Système classificatoire complexe",
                    "Analogies structurelles possibles",
                    "Règles explicites compréhensibles"
                ]
            },
            "formal_operational": {
                "age_range": "11+ years",
                "key_capabilities": [
                    "Pensée abstraite hypothétique",
                    "Logique formelle",
                    "Combinatoire systématique",
                    "Métacognition développée"
                ],
                "language_implications": [
                    "Concepts abstraits maîtrisables",
                    "Métaphores complexes possibles",
                    "Métalangage accessible",
                    "Optimisation consciente"
                ]
            }
        }
        
        # Ajout contributions post-piagetiennes
        modern_insights = {
            "theory_of_mind": {
                "emergence": "4-5 years",
                "implications": [
                    "Compréhension intentions communicatives",
                    "Pragmatique conversationnelle",
                    "Métaphores mentales accessibles"
                ]
            },
            "executive_functions": {
                "inhibitory_control": "3-7 years development",
                "working_memory": "3-15 years development", 
                "cognitive_flexibility": "3-7 years key period",
                "implications": [
                    "Contrôle attention linguistique",
                    "Commutation codes possible",
                    "Adaptation contextuelle"
                ]
            },
            "statistical_learning": {
                "infant_capabilities": "present from birth",
                "pattern_detection": "probabilistic learning",
                "implications": [
                    "Régularités phonotactiques détectées",
                    "Structures grammaticales inductives",
                    "Fréquence optimise acquisition"
                ]
            }
        }
        
        piaget_stages["modern_additions"] = modern_insights
        return piaget_stages
    
    def design_developmental_vocabulary(self) -> Dict[str, Any]:
        """Design vocabulaire développemental optimal"""
        print("📚 DESIGN VOCABULAIRE DÉVELOPPEMENTAL...")
        
        developmental_vocab = {
            "stage_0_6_months": {
                "phonetic_inventory": {
                    "vowels": ["a", "ə", "o"],
                    "consonants": ["m", "b", "p"],
                    "syllable_patterns": ["ma", "ba", "pa", "a", "o"]
                },
                "semantic_categories": [
                    "caregiver_identification",
                    "basic_needs",
                    "comfort_states"
                ],
                "core_words": {
                    "ma": "primary caregiver",
                    "ba": "secondary caregiver", 
                    "pa": "food/milk",
                    "a": "attention request",
                    "o": "discomfort"
                },
                "gestural_complements": {
                    "reaching": "want/need",
                    "pushing_away": "reject/enough",
                    "clapping": "pleasure/approval"
                }
            },
            "stage_6_12_months": {
                "phonetic_expansion": {
                    "new_vowels": ["i", "u", "e"],
                    "new_consonants": ["d", "t", "n"],
                    "syllable_patterns": ["CVCV", "CV", "VC"]
                },
                "semantic_expansion": [
                    "object_permanence",
                    "spatial_relations",
                    "social_interaction"
                ],
                "core_additions": {
                    "di": "disappearance/gone",
                    "tu": "you/other",
                    "ne": "negation/no",
                    "up": "vertical movement",
                    "bi": "bye/departure"
                }
            },
            "stage_12_24_months": {
                "combinatorial_emergence": {
                    "two_word_combinations": True,
                    "semantic_relations": [
                        "agent-action",
                        "action-object", 
                        "attribute-entity",
                        "location-entity"
                    ]
                },
                "analogical_foundations": {
                    "size_analogies": "big=important, small=less",
                    "spatial_analogies": "up=good, down=bad",
                    "temporal_analogies": "fast=urgent, slow=calm"
                }
            }
        }
        
        return developmental_vocab
    
    def analyze_optimal_writing_system(self) -> Dict[str, Any]:
        """Analyse système écriture optimal pour développement"""
        print("✍️ ANALYSE SYSTÈME ÉCRITURE OPTIMAL...")
        
        writing_system = {
            "developmental_sequence": {
                "stage_1_pictographic": {
                    "age": "2-4 years",
                    "characteristics": [
                        "Direct visual representation",
                        "Iconic relationship to meaning",
                        "Single concept per symbol"
                    ],
                    "examples": {
                        "○": "sun/day/warm",
                        "~~~": "water/liquid",
                        "△": "house/shelter",
                        "—": "ground/flat/stable"
                    }
                },
                "stage_2_logographic": {
                    "age": "4-6 years",
                    "characteristics": [
                        "Abstract symbol-meaning link",
                        "Compound concepts possible",
                        "Cultural conventions"
                    ],
                    "combination_rules": [
                        "Semantic composition",
                        "Visual harmony",
                        "Mnemonic structure"
                    ]
                },
                "stage_3_syllabic": {
                    "age": "6-8 years",
                    "characteristics": [
                        "Phonetic awareness integration",
                        "Sound-symbol correspondence",
                        "Syllable-based decomposition"
                    ]
                },
                "stage_4_alphabetic": {
                    "age": "8+ years",
                    "characteristics": [
                        "Phonemic analysis",
                        "Compositional flexibility",
                        "Systematic correspondence"
                    ]
                }
            },
            "visual_constraints": {
                "recognition_threshold": "3-4 distinctive features",
                "complexity_limits": {
                    "3-4_years": "max 3 strokes",
                    "5-6_years": "max 5 strokes",
                    "7+_years": "complex forms possible"
                },
                "gestalt_principles": [
                    "Figure-ground separation",
                    "Closure completion",
                    "Symmetry preference",
                    "Simplicity bias"
                ]
            }
        }
        
        return writing_system
    
    def analyze_sign_language_constraints(self) -> Dict[str, Any]:
        """Analyse contraintes langage signé développemental"""
        print("👋 ANALYSE CONTRAINTES LANGAGE SIGNÉ...")
        
        sign_constraints = {
            "motor_development": {
                "gross_motor": {
                    "6-12_months": "whole arm movements",
                    "12-18_months": "deliberate pointing",
                    "18-24_months": "two-handed coordination",
                    "2-3_years": "spatial locations",
                    "3-4_years": "directional movements"
                },
                "fine_motor": {
                    "12-18_months": "hand shapes emerge",
                    "18-24_months": "finger differentiation",
                    "2-3_years": "precision grip",
                    "3-4_years": "complex handshapes",
                    "4-5_years": "simultaneous bilateral"
                }
            },
            "visual_attention": {
                "tracking_abilities": {
                    "6-12_months": "central vision focus",
                    "12-18_months": "peripheral awareness",
                    "18-24_months": "gaze following",
                    "2-3_years": "divided attention",
                    "3-4_years": "selective attention"
                },
                "processing_speed": {
                    "infant": "slow sequential",
                    "toddler": "improved speed",
                    "preschool": "parallel processing emerging",
                    "school_age": "adult-like speed"
                }
            },
            "optimal_sign_structure": {
                "early_signs": {
                    "handshape": "simple fist or open hand",
                    "movement": "gross motor, whole arm",
                    "location": "near body center",
                    "examples": ["eat", "milk", "more", "finished"]
                },
                "intermediate_signs": {
                    "handshape": "basic hand configurations",
                    "movement": "controlled directional",
                    "location": "expanded signing space",
                    "combinations": "two-handed possible"
                },
                "advanced_signs": {
                    "handshape": "complex finger configurations",
                    "movement": "precise spatial grammar",
                    "location": "full 3D signing space",
                    "morphology": "inflectional variations"
                }
            }
        }
        
        return sign_constraints
    
    def generate_sapir_whorf_optimization(self) -> Dict[str, Any]:
        """Génération optimisation Sapir-Whorf pour développement cognitif"""
        print("🔄 OPTIMISATION SAPIR-WHORF...")
        
        sapir_whorf_optimization = {
            "linguistic_relativity_principles": {
                "weak_version": "Language influences thought patterns",
                "strong_version": "Language determines cognitive categories",
                "optimization_target": "Enhanced cognitive development through language"
            },
            "developmental_linguistic_scaffolding": {
                "cognitive_bootstrapping": {
                    "spatial_language": "enhances spatial reasoning",
                    "temporal_language": "develops time concepts",
                    "causal_language": "improves causal reasoning",
                    "abstract_language": "enables abstract thought"
                },
                "age_appropriate_concepts": {
                    "0-2_years": [
                        "spatial_relations",
                        "temporal_sequence",
                        "causal_basics"
                    ],
                    "2-4_years": [
                        "categorization_systems",
                        "analogical_thinking",
                        "perspective_taking"
                    ],
                    "4-7_years": [
                        "logical_operations",
                        "systematic_classification",
                        "hypothetical_reasoning"
                    ],
                    "7+_years": [
                        "abstract_mathematics",
                        "philosophical_concepts",
                        "meta_cognitive_awareness"
                    ]
                }
            },
            "optimal_concept_introduction": {
                "analogical_progression": {
                    "concrete_to_abstract": "physical → mental",
                    "simple_to_complex": "basic → composite",
                    "familiar_to_novel": "known → unknown"
                },
                "mnemonic_integration": {
                    "phonetic_mnemonics": "sound-meaning links",
                    "visual_mnemonics": "shape-concept associations",
                    "kinesthetic_mnemonics": "movement-meaning bonds",
                    "semantic_mnemonics": "conceptual networks"
                }
            }
        }
        
        return sapir_whorf_optimization
    
    def synthesize_optimal_language_design(self) -> Dict[str, Any]:
        """Synthèse design langage optimal"""
        print("🎯 SYNTHÈSE DESIGN LANGAGE OPTIMAL...")
        
        # Collecte toutes analyses
        auditory = self.analyze_auditory_constraints()
        phonatory = self.analyze_phonatory_constraints()
        memory = self.analyze_memory_constraints()
        piaget = self.analyze_piaget_stages()
        vocabulary = self.design_developmental_vocabulary()
        writing = self.analyze_optimal_writing_system()
        sign = self.analyze_sign_language_constraints()
        sapir_whorf = self.generate_sapir_whorf_optimization()
        
        synthesis = {
            "language_design_principles": {
                "neurobiological_foundation": "Respect brain constraints and capabilities",
                "developmental_optimization": "Age-appropriate complexity progression",
                "multimodal_integration": "Speech + gesture + writing synergy",
                "cognitive_enhancement": "Language as cognitive development tool"
            },
            "core_design_features": {
                "phonetic_system": {
                    "baby_friendly_core": phonatory["articulatory_development"]["0-6_months"],
                    "expansion_sequence": "Follow motor development timeline",
                    "frequency_optimization": auditory["frequency_range"]["optimal_recognition"],
                    "temporal_constraints": auditory["temporal_processing"]
                },
                "semantic_system": {
                    "conceptual_progression": "Piaget stages + modern insights",
                    "analogical_foundations": "Concrete to abstract mapping",
                    "mnemonic_integration": "Multi-sensory associations",
                    "cultural_scaffolding": "Social context integration"
                },
                "writing_system": {
                    "developmental_sequence": writing["developmental_sequence"],
                    "visual_optimization": writing["visual_constraints"],
                    "motor_compatibility": "Match fine motor development"
                },
                "sign_system": {
                    "gestural_progression": sign["motor_development"],
                    "visual_attention_respect": sign["visual_attention"],
                    "spatial_grammar": "3D linguistic space utilization"
                }
            },
            "implementation_roadmap": {
                "phase_1_foundation": {
                    "target_age": "0-2 years",
                    "focus": "Basic communication needs",
                    "modalities": ["baby_signs", "simple_vocalizations"],
                    "vocabulary_size": "10-50 core concepts"
                },
                "phase_2_expansion": {
                    "target_age": "2-4 years", 
                    "focus": "Symbolic representation",
                    "modalities": ["expanded_speech", "pictographic_writing"],
                    "vocabulary_size": "200-500 concepts"
                },
                "phase_3_systematization": {
                    "target_age": "4-7 years",
                    "focus": "Logical structure",
                    "modalities": ["grammatical_speech", "logographic_writing"],
                    "vocabulary_size": "1000-2000 concepts"
                },
                "phase_4_optimization": {
                    "target_age": "7+ years",
                    "focus": "Cognitive enhancement",
                    "modalities": ["full_linguistic_system"],
                    "vocabulary_size": "unlimited systematic expansion"
                }
            }
        }
        
        return synthesis
    
    def save_analysis_report(self, output_path: str = None) -> str:
        """Sauvegarde rapport complet analyse neurocognitive"""
        if not output_path:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"/home/stephane/GitHub/PaniniFS-1/scripts/scripts/neurocognitive_language_analysis_{timestamp}.json"
        
        # Exécution toutes analyses
        complete_analysis = {
            "analysis_metadata": {
                "generation_date": datetime.datetime.now().isoformat(),
                "analysis_scope": "Neurocognitive constraints for optimal language design",
                "theoretical_frameworks": [
                    "Neuroscience constraints",
                    "Piaget developmental stages",
                    "Baby sign language",
                    "Sapir-Whorf optimization"
                ]
            },
            "auditory_constraints": self.analyze_auditory_constraints(),
            "phonatory_constraints": self.analyze_phonatory_constraints(),
            "memory_constraints": self.analyze_memory_constraints(),
            "piaget_developmental_stages": self.analyze_piaget_stages(),
            "developmental_vocabulary": self.design_developmental_vocabulary(),
            "optimal_writing_system": self.analyze_optimal_writing_system(),
            "sign_language_constraints": self.analyze_sign_language_constraints(),
            "sapir_whorf_optimization": self.generate_sapir_whorf_optimization(),
            "optimal_language_synthesis": self.synthesize_optimal_language_design()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(complete_analysis, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Analyse neurocognitive sauvegardée: {output_path}")
        return output_path

def main():
    print("🧠 ANALYSEUR NEUROCOGNITIF LANGAGE OPTIMAL")
    print("=" * 50)
    print("🎯 Design langue basée contraintes cerveau + développement")
    print("📚 Fondations: Neuroscience + Piaget + Baby Signs + Sapir-Whorf")
    print("")
    
    analyzer = NeurocognitiveLinguisticAnalyzer()
    
    # Analyses complètes
    print("🔬 ANALYSES NEUROCOGNITIVES...")
    synthesis = analyzer.synthesize_optimal_language_design()
    
    # Affichage résultats clés
    print(f"\n🎯 PRINCIPES DESIGN:")
    for principle, description in synthesis["language_design_principles"].items():
        print(f"   📌 {principle.replace('_', ' ').title()}: {description}")
    
    print(f"\n📈 ROADMAP IMPLÉMENTATION:")
    for phase, details in synthesis["implementation_roadmap"].items():
        phase_name = phase.replace("_", " ").title()
        print(f"   🚀 {phase_name}")
        print(f"      Âge: {details['target_age']}")
        print(f"      Focus: {details['focus']}")
        print(f"      Vocabulaire: {details['vocabulary_size']}")
    
    # Sauvegarde
    report_path = analyzer.save_analysis_report()
    
    print(f"\n🏆 ANALYSE NEUROCOGNITIVE COMPLÈTE")
    print(f"📊 Contraintes cerveau + développement analysées")
    print(f"🧠 Design optimal multimodal (parole + geste + écriture)")
    print(f"👶 Progression développementale 0-18+ ans")
    print(f"🔄 Optimisation Sapir-Whorf pour enhancement cognitif")
    print(f"📁 Rapport: {report_path.split('/')[-1]}")

if __name__ == "__main__":
    main()
