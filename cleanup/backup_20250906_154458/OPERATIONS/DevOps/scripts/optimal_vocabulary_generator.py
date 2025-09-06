#!/usr/bin/env python3
"""
Générateur Vocabulaire Prototype Langage Optimal
👶 Création vocabulaire développemental avec progression analogique optimisée
"""

import json
import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import re

@dataclass
class OptimalWord:
    phonetic_form: str
    gestural_form: str
    visual_symbol: str
    semantic_core: str
    analogical_base: str
    age_introduction: str
    cognitive_prerequisites: List[str]
    mnemonic_aids: List[str]
    complexity_level: int

@dataclass
class ConceptualProgression:
    base_concept: str
    analogical_extensions: List[str]
    age_milestones: Dict[str, str]
    cognitive_scaffolding: List[str]

class OptimalVocabularyGenerator:
    def __init__(self):
        self.vocabulary_database = {}
        self.analogical_networks = {}
        self.developmental_progression = {}
        
    def generate_baby_core_vocabulary(self) -> Dict[str, OptimalWord]:
        """Génération vocabulaire core pour bébés 0-12 mois"""
        print("👶 GÉNÉRATION VOCABULAIRE CORE BÉBÉ...")
        
        baby_core = {
            # Besoins primaires
            "ma": OptimalWord(
                phonetic_form="ma",
                gestural_form="hand_to_mouth",
                visual_symbol="○",
                semantic_core="primary_caregiver",
                analogical_base="comfort_source",
                age_introduction="2-4_months",
                cognitive_prerequisites=["attachment_formation"],
                mnemonic_aids=["labial_comfort", "maternal_frequency"],
                complexity_level=1
            ),
            "pa": OptimalWord(
                phonetic_form="pa",
                gestural_form="reach_up",
                visual_symbol="↑",
                semantic_core="want_attention",
                analogical_base="elevation_request",
                age_introduction="4-6_months",
                cognitive_prerequisites=["intentional_communication"],
                mnemonic_aids=["bilabial_emphasis", "upward_motion"],
                complexity_level=1
            ),
            "ba": OptimalWord(
                phonetic_form="ba",
                gestural_form="push_away",
                visual_symbol="—",
                semantic_core="enough_stop",
                analogical_base="boundary_creation",
                age_introduction="6-8_months",
                cognitive_prerequisites=["self_agency"],
                mnemonic_aids=["bilabial_closure", "rejection_motion"],
                complexity_level=1
            ),
            "da": OptimalWord(
                phonetic_form="da",
                gestural_form="point_indicate",
                visual_symbol="→",
                semantic_core="this_that",
                analogical_base="directional_reference",
                age_introduction="8-10_months",
                cognitive_prerequisites=["joint_attention"],
                mnemonic_aids=["dental_precision", "pointing_gesture"],
                complexity_level=2
            ),
            "na": OptimalWord(
                phonetic_form="na",
                gestural_form="head_shake",
                visual_symbol="×",
                semantic_core="no_negation",
                analogical_base="opposition_concept",
                age_introduction="10-12_months",
                cognitive_prerequisites=["intentional_rejection"],
                mnemonic_aids=["nasal_resonance", "negative_motion"],
                complexity_level=2
            )
        }
        
        return baby_core
    
    def generate_toddler_expansion(self) -> Dict[str, OptimalWord]:
        """Génération expansion vocabulaire toddlers 12-24 mois"""
        print("🚶 GÉNÉRATION EXPANSION TODDLER...")
        
        toddler_expansion = {
            # Concepts spatiaux
            "up": OptimalWord(
                phonetic_form="ʌp",
                gestural_form="arms_raised",
                visual_symbol="↑",
                semantic_core="vertical_positive",
                analogical_base="elevation_improvement",
                age_introduction="12-15_months",
                cognitive_prerequisites=["spatial_awareness"],
                mnemonic_aids=["vowel_raising", "upward_gesture"],
                complexity_level=2
            ),
            "dow": OptimalWord(
                phonetic_form="daʊ",
                gestural_form="point_down",
                visual_symbol="↓",
                semantic_core="vertical_negative",
                analogical_base="descent_decrease",
                age_introduction="12-15_months",
                cognitive_prerequisites=["spatial_awareness"],
                mnemonic_aids=["vowel_lowering", "downward_gesture"],
                complexity_level=2
            ),
            "go": OptimalWord(
                phonetic_form="goʊ",
                gestural_form="forward_motion",
                visual_symbol="→",
                semantic_core="movement_initiation",
                analogical_base="progress_advance",
                age_introduction="15-18_months",
                cognitive_prerequisites=["intentional_movement"],
                mnemonic_aids=["vowel_advancement", "forward_gesture"],
                complexity_level=2
            ),
            "kom": OptimalWord(
                phonetic_form="kʌm",
                gestural_form="beckoning",
                visual_symbol="←",
                semantic_core="approach_invitation",
                analogical_base="attraction_gathering",
                age_introduction="15-18_months",
                cognitive_prerequisites=["social_invitation"],
                mnemonic_aids=["velar_closure", "gathering_gesture"],
                complexity_level=3
            ),
            
            # Concepts temporels
            "naw": OptimalWord(
                phonetic_form="naʊ",
                gestural_form="immediate_point",
                visual_symbol="●",
                semantic_core="present_immediate",
                analogical_base="current_moment",
                age_introduction="18-21_months",
                cognitive_prerequisites=["temporal_awareness"],
                mnemonic_aids=["diphthong_urgency", "immediate_gesture"],
                complexity_level=3
            ),
            "den": OptimalWord(
                phonetic_form="ðɛn",
                gestural_form="sequential_point",
                visual_symbol="●→●",
                semantic_core="temporal_sequence",
                analogical_base="causal_succession",
                age_introduction="21-24_months",
                cognitive_prerequisites=["sequence_understanding"],
                mnemonic_aids=["dental_friction", "sequential_gesture"],
                complexity_level=4
            )
        }
        
        return toddler_expansion
    
    def generate_preschool_systematization(self) -> Dict[str, OptimalWord]:
        """Génération systematisation preschool 2-4 ans"""
        print("🎒 GÉNÉRATION SYSTEMATISATION PRESCHOOL...")
        
        preschool_system = {
            # Système analogique taille
            "big": OptimalWord(
                phonetic_form="bɪg",
                gestural_form="arms_wide",
                visual_symbol="●●●",
                semantic_core="size_large",
                analogical_base="importance_magnitude",
                age_introduction="24-30_months",
                cognitive_prerequisites=["comparative_thinking"],
                mnemonic_aids=["bilabial_expansion", "spreading_gesture"],
                complexity_level=3
            ),
            "smal": OptimalWord(
                phonetic_form="smɔl",
                gestural_form="pinch_fingers",
                visual_symbol="·",
                semantic_core="size_small",
                analogical_base="insignificance_delicacy",
                age_introduction="24-30_months",
                cognitive_prerequisites=["comparative_thinking"],
                mnemonic_aids=["fricative_constriction", "pinching_gesture"],
                complexity_level=3
            ),
            
            # Système analogique couleur-émotion
            "brat": OptimalWord(
                phonetic_form="braɪt",
                gestural_form="hands_open_up",
                visual_symbol="☀",
                semantic_core="luminous_positive",
                analogical_base="happiness_energy",
                age_introduction="30-36_months",
                cognitive_prerequisites=["emotional_categorization"],
                mnemonic_aids=["bright_vowel", "opening_gesture"],
                complexity_level=4
            ),
            "dark": OptimalWord(
                phonetic_form="dɑrk",
                gestural_form="hands_close_down",
                visual_symbol="●",
                semantic_core="shadow_negative",
                analogical_base="sadness_mystery",
                age_introduction="30-36_months",
                cognitive_prerequisites=["emotional_categorization"],
                mnemonic_aids=["dark_vowel", "closing_gesture"],
                complexity_level=4
            ),
            
            # Système analogique quantité
            "mor": OptimalWord(
                phonetic_form="mɔr",
                gestural_form="gathering_motion",
                visual_symbol="++",
                semantic_core="quantity_increase",
                analogical_base="abundance_growth",
                age_introduction="36-42_months",
                cognitive_prerequisites=["quantitative_concepts"],
                mnemonic_aids=["open_vowel", "accumulating_gesture"],
                complexity_level=4
            ),
            "les": OptimalWord(
                phonetic_form="lɛs",
                gestural_form="diminishing_motion",
                visual_symbol="--",
                semantic_core="quantity_decrease",
                analogical_base="scarcity_reduction",
                age_introduction="36-42_months",
                cognitive_prerequisites=["quantitative_concepts"],
                mnemonic_aids=["mid_vowel", "reducing_gesture"],
                complexity_level=4
            )
        }
        
        return preschool_system
    
    def generate_analogical_networks(self) -> Dict[str, ConceptualProgression]:
        """Génération réseaux analogiques développementaux"""
        print("🔗 GÉNÉRATION RÉSEAUX ANALOGIQUES...")
        
        networks = {
            "spatial_vertical": ConceptualProgression(
                base_concept="up_down",
                analogical_extensions=[
                    "good_bad",
                    "happy_sad", 
                    "important_unimportant",
                    "success_failure",
                    "divine_mundane"
                ],
                age_milestones={
                    "12-18_months": "physical_spatial",
                    "18-24_months": "emotional_valence",
                    "2-3_years": "social_hierarchy",
                    "3-4_years": "abstract_values",
                    "4-5_years": "metaphysical_concepts"
                },
                cognitive_scaffolding=[
                    "embodied_experience",
                    "emotional_association",
                    "social_observation",
                    "abstract_reasoning"
                ]
            ),
            "container_metaphor": ConceptualProgression(
                base_concept="in_out",
                analogical_extensions=[
                    "included_excluded",
                    "member_stranger",
                    "safe_dangerous",
                    "familiar_foreign",
                    "understood_mysterious"
                ],
                age_milestones={
                    "15-21_months": "physical_containment",
                    "21-30_months": "social_inclusion",
                    "30-42_months": "emotional_safety",
                    "3-4_years": "conceptual_categories",
                    "4-5_years": "abstract_membership"
                },
                cognitive_scaffolding=[
                    "object_permanence",
                    "social_belonging",
                    "emotional_security",
                    "categorical_thinking"
                ]
            ),
            "journey_metaphor": ConceptualProgression(
                base_concept="go_come",
                analogical_extensions=[
                    "start_finish",
                    "attempt_achievement",
                    "learning_mastery",
                    "problem_solution",
                    "life_death"
                ],
                age_milestones={
                    "18-24_months": "physical_movement",
                    "2-3_years": "goal_directed_action",
                    "3-4_years": "learning_process",
                    "4-5_years": "abstract_progress",
                    "5-6_years": "existential_concepts"
                },
                cognitive_scaffolding=[
                    "motor_planning",
                    "intentional_action",
                    "causal_understanding",
                    "abstract_thinking"
                ]
            )
        }
        
        return networks
    
    def generate_phonetic_optimization_rules(self) -> Dict[str, Any]:
        """Génération règles optimisation phonétique"""
        print("🎵 GÉNÉRATION RÈGLES OPTIMISATION PHONÉTIQUE...")
        
        optimization_rules = {
            "developmental_constraints": {
                "early_phonemes": {
                    "vowels": ["a", "ə", "o", "i", "u"],
                    "consonants": ["m", "b", "p", "d", "t", "n"],
                    "rationale": "Earliest motor coordination capabilities"
                },
                "intermediate_phonemes": {
                    "vowels": ["e", "ɛ", "ɔ", "ʌ"],
                    "consonants": ["k", "g", "f", "s", "l", "r"],
                    "rationale": "Developing fine motor control"
                },
                "advanced_phonemes": {
                    "vowels": ["ɪ", "ʊ", "aɪ", "aʊ", "oɪ"],
                    "consonants": ["ʃ", "ʒ", "tʃ", "dʒ", "θ", "ð"],
                    "rationale": "Mature articulation precision"
                }
            },
            "mnemonic_principles": {
                "sound_symbolism": {
                    "high_frequency": "small, bright, fast concepts",
                    "low_frequency": "large, dark, slow concepts",
                    "front_vowels": "close, immediate concepts", 
                    "back_vowels": "distant, abstract concepts",
                    "plosives": "sudden, forceful actions",
                    "fricatives": "continuous, gradual processes"
                },
                "articulatory_iconicity": {
                    "labial_sounds": "oral, feeding, comfort concepts",
                    "dental_sounds": "precise, pointing, specific concepts",
                    "velar_sounds": "back, hidden, internal concepts",
                    "nasal_sounds": "negative, rejection, boundary concepts"
                }
            },
            "cognitive_load_optimization": {
                "syllable_structure": {
                    "stage_1": "CV, V patterns only",
                    "stage_2": "CV, VC, CVC patterns",
                    "stage_3": "CVCV, complex onsets",
                    "stage_4": "unrestricted complexity"
                },
                "phonotactic_constraints": {
                    "avoid_similar_consecutives": "reduce confusion",
                    "maximize_contrast": "enhance distinctivity",
                    "respect_sonority": "natural syllable structure"
                }
            }
        }
        
        return optimization_rules
    
    def generate_gestural_system(self) -> Dict[str, Any]:
        """Génération système gestuel coordonné"""
        print("👋 GÉNÉRATION SYSTÈME GESTUEL...")
        
        gestural_system = {
            "baby_signs_foundation": {
                "basic_needs": {
                    "milk": "squeezing_motion",
                    "eat": "hand_to_mouth",
                    "more": "fingertips_together",
                    "finished": "hands_shake_down",
                    "sleep": "hands_to_cheek"
                },
                "social_interaction": {
                    "hello": "wave_open_close",
                    "goodbye": "wave_side_to_side",
                    "please": "circular_chest_motion",
                    "thank_you": "fingers_to_lips_forward",
                    "sorry": "circular_chest_motion_opposite"
                }
            },
            "spatial_grammar": {
                "location_markers": {
                    "here": "point_down_near",
                    "there": "point_away",
                    "up": "point_up",
                    "down": "point_down"
                },
                "directional_system": {
                    "come": "beckoning_toward_body",
                    "go": "pushing_away_from_body",
                    "forward": "hand_motion_forward",
                    "backward": "hand_motion_backward"
                }
            },
            "temporal_markers": {
                "now": "tap_present_space",
                "then": "point_to_future_space",
                "before": "point_to_past_space",
                "after": "sequential_hand_movements"
            },
            "quantity_qualifiers": {
                "big": "hands_spread_wide",
                "small": "pinch_gesture",
                "many": "repeated_indicating",
                "few": "single_indicating"
            }
        }
        
        return gestural_system
    
    def generate_visual_symbol_system(self) -> Dict[str, Any]:
        """Génération système symboles visuels"""
        print("👁️ GÉNÉRATION SYSTÈME SYMBOLES VISUELS...")
        
        visual_system = {
            "pictographic_stage": {
                "concrete_objects": {
                    "sun": "○",
                    "water": "~~~",
                    "house": "△",
                    "tree": "🌳",
                    "person": "人"
                },
                "basic_actions": {
                    "go": "→",
                    "come": "←",
                    "up": "↑",
                    "down": "↓",
                    "stop": "■"
                }
            },
            "ideographic_stage": {
                "abstract_concepts": {
                    "good": "☀",
                    "bad": "●",
                    "love": "♡",
                    "think": "💭",
                    "speak": "💬"
                },
                "compound_concepts": {
                    "teach": "person + knowledge_transfer",
                    "learn": "person + knowledge_reception",
                    "play": "person + joy_action"
                }
            },
            "systematic_stage": {
                "morphological_markers": {
                    "plural": "concept + (×n)",
                    "past": "concept + (←)",
                    "future": "concept + (→)",
                    "question": "concept + (?)",
                    "negation": "concept + (×)"
                },
                "semantic_categories": {
                    "living_things": "organic_marker",
                    "tools": "functional_marker", 
                    "places": "location_marker",
                    "actions": "dynamic_marker",
                    "qualities": "descriptive_marker"
                }
            }
        }
        
        return visual_system
    
    def synthesize_prototype_vocabulary(self) -> Dict[str, Any]:
        """Synthèse vocabulaire prototype complet"""
        print("🎯 SYNTHÈSE VOCABULAIRE PROTOTYPE...")
        
        # Collection tous composants
        baby_core = self.generate_baby_core_vocabulary()
        toddler_expansion = self.generate_toddler_expansion()
        preschool_system = self.generate_preschool_systematization()
        analogical_networks = self.generate_analogical_networks()
        phonetic_rules = self.generate_phonetic_optimization_rules()
        gestural_system = self.generate_gestural_system()
        visual_system = self.generate_visual_symbol_system()
        
        # Compilation vocabulaire par stades
        vocabulary_by_stage = {
            "stage_1_baby": {
                "age_range": "0-12_months",
                "vocabulary": baby_core,
                "total_words": len(baby_core),
                "complexity_range": "1-2",
                "primary_modality": "gestural + vocal"
            },
            "stage_2_toddler": {
                "age_range": "12-24_months",
                "vocabulary": {**baby_core, **toddler_expansion},
                "total_words": len(baby_core) + len(toddler_expansion),
                "complexity_range": "1-4",
                "primary_modality": "vocal + gestural"
            },
            "stage_3_preschool": {
                "age_range": "24-48_months",
                "vocabulary": {**baby_core, **toddler_expansion, **preschool_system},
                "total_words": len(baby_core) + len(toddler_expansion) + len(preschool_system),
                "complexity_range": "1-5",
                "primary_modality": "vocal + visual_symbols"
            }
        }
        
        prototype = {
            "design_principles": {
                "neurobiological_respect": "Follow brain development constraints",
                "analogical_foundation": "Build conceptual networks systematically",
                "multimodal_integration": "Coordinate speech, gesture, and writing",
                "cognitive_enhancement": "Optimize language for cognitive development"
            },
            "vocabulary_progression": vocabulary_by_stage,
            "analogical_networks": analogical_networks,
            "phonetic_optimization": phonetic_rules,
            "gestural_coordination": gestural_system,
            "visual_symbol_system": visual_system,
            "implementation_guidelines": {
                "introduction_sequence": "Respect developmental readiness",
                "practice_methods": "Multi-sensory reinforcement",
                "assessment_criteria": "Spontaneous usage in context",
                "adaptation_flexibility": "Individual developmental variation"
            }
        }
        
        return prototype
    
    def save_prototype_vocabulary(self, output_path: str = None) -> str:
        """Sauvegarde vocabulaire prototype"""
        if not output_path:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"/home/stephane/GitHub/PaniniFS-1/scripts/scripts/optimal_language_prototype_{timestamp}.json"
        
        prototype = self.synthesize_prototype_vocabulary()
        
        # Conversion dataclass vers dict pour JSON
        def convert_for_json(obj):
            if hasattr(obj, '__dict__'):
                return asdict(obj)
            elif isinstance(obj, dict):
                return {k: convert_for_json(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_for_json(item) for item in obj]
            else:
                return obj
        
        prototype_json = convert_for_json(prototype)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(prototype_json, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Prototype vocabulaire sauvegardé: {output_path}")
        return output_path

def main():
    print("👶 GÉNÉRATEUR VOCABULAIRE PROTOTYPE LANGAGE OPTIMAL")
    print("=" * 60)
    print("🎯 Création vocabulaire développemental avec progression analogique")
    print("📚 Multimodal: Phonétique + Gestuel + Visuel")
    print("")
    
    generator = OptimalVocabularyGenerator()
    
    # Génération prototype
    prototype = generator.synthesize_prototype_vocabulary()
    
    # Affichage résultats
    print(f"📊 STATISTIQUES PROTOTYPE:")
    for stage_name, stage_data in prototype["vocabulary_progression"].items():
        stage_display = stage_name.replace("_", " ").title()
        print(f"   🎯 {stage_display}")
        print(f"      Âge: {stage_data['age_range']}")
        print(f"      Mots: {stage_data['total_words']}")
        print(f"      Complexité: {stage_data['complexity_range']}")
        print(f"      Modalité: {stage_data['primary_modality']}")
    
    print(f"\n🔗 RÉSEAUX ANALOGIQUES:")
    for network_name, network_data in prototype["analogical_networks"].items():
        network_display = network_name.replace("_", " ").title()
        print(f"   📈 {network_display}")
        print(f"      Base: {network_data.base_concept}")
        print(f"      Extensions: {len(network_data.analogical_extensions)}")
    
    print(f"\n🎵 OPTIMISATION PHONÉTIQUE:")
    phonetic = prototype["phonetic_optimization"]["developmental_constraints"]
    print(f"   Phonèmes précoces: {len(phonetic['early_phonemes']['vowels'])} voyelles, {len(phonetic['early_phonemes']['consonants'])} consonnes")
    print(f"   Progression: Précoce → Intermédiaire → Avancé")
    
    print(f"\n👋 SYSTÈME GESTUEL:")
    gestural = prototype["gestural_coordination"]
    print(f"   Baby signs: {len(gestural['baby_signs_foundation']['basic_needs'])} besoins + {len(gestural['baby_signs_foundation']['social_interaction'])} social")
    print(f"   Grammaire spatiale: 3D + temporelle + quantitative")
    
    print(f"\n👁️ SYSTÈME VISUEL:")
    visual = prototype["visual_symbol_system"]
    print(f"   Progression: Pictographique → Idéographique → Systématique")
    print(f"   Objets concrets: {len(visual['pictographic_stage']['concrete_objects'])}")
    print(f"   Concepts abstraits: {len(visual['ideographic_stage']['abstract_concepts'])}")
    
    # Sauvegarde
    prototype_path = generator.save_prototype_vocabulary()
    
    print(f"\n🏆 PROTOTYPE VOCABULAIRE OPTIMAL GÉNÉRÉ")
    print(f"👶 Progression 0-4 ans avec fondations analogiques")
    print(f"🧠 Optimisé contraintes neurocognitives + développement")
    print(f"🎯 Multimodal: Parole + Geste + Écriture coordonnés")
    print(f"📁 Sauvegardé: {prototype_path.split('/')[-1]}")

if __name__ == "__main__":
    main()
