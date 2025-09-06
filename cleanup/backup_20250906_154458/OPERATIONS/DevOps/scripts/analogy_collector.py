#!/usr/bin/env python3
"""
Collecteur Analogies et Métaphores - Mécanismes cognitifs et limites
🔗 Exploration analogies, métaphores, correspondances avec marquage limites explicites
"""

import json
import datetime
from typing import List, Dict, Any, Optional
import re
import os

class AnalogyCollector:
    def __init__(self):
        self.store = {
            "metadata": {
                "version": "1.0",
                "description": "Collection analogies avec marquage limites explicites",
                "creation_date": datetime.datetime.now().isoformat(),
                "source_type": "analogy_mapping",
                "focus_areas": ["cognitive_analogies", "scientific_metaphors", "limit_boundaries", "mapping_failures"]
            },
            "semantic_atoms": []
        }
    
    def collect_cognitive_analogies(self) -> List[Dict]:
        """Analogies cognitives fondamentales avec limites explicites"""
        concepts = [
            {
                "concept": "Analogie Hydraulique Électricité",
                "definition": "Correspondance eau/courant, pression/tension, résistance/étroitesse pour comprendre circuits électriques",
                "category": "scientific_analogy",
                "source_domain": "hydraulique",
                "target_domain": "électricité",
                "valid_mappings": {
                    "débit_eau": "intensité_courant",
                    "pression": "tension",
                    "tuyau_étroit": "résistance",
                    "réservoir": "condensateur"
                },
                "boundary_limits": {
                    "breakdown_points": ["fréquences_hautes", "effets_quantiques", "champs_electromagnétiques"],
                    "invalid_mappings": ["température_eau ≠ température_électrique", "viscosité ≠ impédance_complexe"],
                    "domain_restrictions": "circuits_DC_basse_fréquence_uniquement"
                },
                "cognitive_utility": "mnémonique_intuition_initiale",
                "pedagogical_value": 0.85,
                "precision_limit": 0.6,
                "relevance_score": 0.92
            },
            {
                "concept": "Métaphore Système Solaire Atome",
                "definition": "Modèle planétaire atome avec électrons orbitant noyau, analogie gravitationnelle pour structure atomique",
                "category": "historical_analogy",
                "source_domain": "système_solaire",
                "target_domain": "structure_atomique",
                "valid_mappings": {
                    "soleil": "noyau",
                    "planètes": "électrons",
                    "orbites": "niveaux_énergie",
                    "attraction_gravitationnelle": "attraction_coulombienne"
                },
                "boundary_limits": {
                    "breakdown_points": ["mécanique_quantique", "principe_incertitude", "dualité_onde_particule"],
                    "invalid_mappings": ["orbites_définies ≠ nuages_probabilité", "rayonnement_énergie_impossible"],
                    "domain_restrictions": "pré_quantique_intuition_grossière",
                    "historical_obsolescence": "remplacé_modèle_quantique_1925"
                },
                "cognitive_utility": "introduction_structure_atomique",
                "pedagogical_value": 0.7,
                "precision_limit": 0.3,
                "relevance_score": 0.88
            },
            {
                "concept": "Analogie Cerveau Ordinateur",
                "definition": "Correspondance traitement information cerveau/ordinateur, mémoire/stockage, processus/algorithmes",
                "category": "computational_analogy",
                "source_domain": "informatique",
                "target_domain": "neurosciences",
                "valid_mappings": {
                    "processeur": "neurones",
                    "mémoire_ram": "mémoire_travail",
                    "stockage": "mémoire_long_terme",
                    "algorithmes": "processus_cognitifs"
                },
                "boundary_limits": {
                    "breakdown_points": ["plasticité_neuronale", "émotions", "conscience", "apprentissage_continu"],
                    "invalid_mappings": ["binaire ≠ graduel", "séquentiel ≠ parallèle_massif", "logique ≠ émotionnel"],
                    "domain_restrictions": "aspects_computationnels_restreints",
                    "oversimplification_risk": "réduction_conscience_calcul"
                },
                "cognitive_utility": "modélisation_aspects_informationnels",
                "pedagogical_value": 0.75,
                "precision_limit": 0.5,
                "relevance_score": 0.83
            },
            {
                "concept": "Métaphore ADN Code Informatique",
                "definition": "Correspondance séquences ADN/code programme, gènes/fonctions, expression/exécution",
                "category": "biological_analogy",
                "source_domain": "programmation",
                "target_domain": "génétique",
                "valid_mappings": {
                    "code_source": "séquence_ADN",
                    "fonctions": "gènes",
                    "variables": "protéines",
                    "compilation": "transcription_traduction",
                    "exécution": "expression_génique"
                },
                "boundary_limits": {
                    "breakdown_points": ["épigénétique", "régulation_complexe", "environnement_cellulaire", "évolution"],
                    "invalid_mappings": ["déterminisme_strict ≠ régulation_dynamique", "bugs ≠ mutations_bénéfiques"],
                    "domain_restrictions": "aspects_informationnels_basiques",
                    "complexity_underestimation": "interactions_multi_niveaux_ignorées"
                },
                "cognitive_utility": "compréhension_hérédité_information",
                "pedagogical_value": 0.8,
                "precision_limit": 0.55,
                "relevance_score": 0.87
            },
            {
                "concept": "Analogie Réseau Social Neurones",
                "definition": "Correspondance connexions sociales/synapses, influence/poids synaptiques, propagation/activation",
                "category": "network_analogy",
                "source_domain": "réseaux_sociaux",
                "target_domain": "réseaux_neuronaux",
                "valid_mappings": {
                    "individus": "neurones",
                    "connexions_amis": "synapses",
                    "influence": "poids_synaptiques",
                    "rumeur_propagation": "propagation_signal",
                    "leaders_opinion": "neurones_hub"
                },
                "boundary_limits": {
                    "breakdown_points": ["vitesse_propagation", "nature_signal", "plasticité_temporelle"],
                    "invalid_mappings": ["contenu_sémantique ≠ électrochimique", "volonté ≠ automatisme"],
                    "domain_restrictions": "structure_topologique_uniquement",
                    "abstraction_level": "dynamiques_émergentes_similaires"
                },
                "cognitive_utility": "compréhension_réseaux_complexes",
                "pedagogical_value": 0.78,
                "precision_limit": 0.6,
                "relevance_score": 0.81
            }
        ]
        
        return self._convert_to_atoms(concepts, "cognitive_analogies")
    
    def collect_mathematical_analogies(self) -> List[Dict]:
        """Analogies mathématiques avec domaines validité"""
        concepts = [
            {
                "concept": "Analogie Dérivée Pente",
                "definition": "Correspondance dérivée fonction/pente tangente, changement instantané/inclinaison géométrique",
                "category": "mathematical_analogy",
                "source_domain": "géométrie_euclidienne",
                "target_domain": "calcul_différentiel",
                "valid_mappings": {
                    "pente_droite": "dérivée_constante",
                    "tangente_courbe": "dérivée_point",
                    "montée_descente": "signe_dérivée",
                    "raideur": "valeur_absolue_dérivée"
                },
                "boundary_limits": {
                    "breakdown_points": ["fonctions_non_dérivables", "discontinuités", "dimensions_supérieures"],
                    "invalid_mappings": ["pente_infinie ≠ dérivée_complexe", "ligne_droite ≠ variation_locale"],
                    "domain_restrictions": "fonctions_lisses_1D",
                    "conceptual_precision": "approximation_locale_uniquement"
                },
                "cognitive_utility": "visualisation_changement_instantané",
                "pedagogical_value": 0.9,
                "precision_limit": 0.8,
                "relevance_score": 0.93
            },
            {
                "concept": "Métaphore Intégrale Aire",
                "definition": "Correspondance intégrale/aire sous courbe, accumulation/surface géométrique",
                "category": "mathematical_analogy", 
                "source_domain": "géométrie_aires",
                "target_domain": "calcul_intégral",
                "valid_mappings": {
                    "aire_rectangle": "somme_riemann",
                    "surface_courbe": "intégrale_définie",
                    "accumulation": "primitive",
                    "découpage_fin": "limite_partitions"
                },
                "boundary_limits": {
                    "breakdown_points": ["intégrales_généralisées", "mesures_complexes", "espaces_abstraits"],
                    "invalid_mappings": ["aire_négative ≠ surface_physique", "infini ≠ géométrie_euclidienne"],
                    "domain_restrictions": "fonctions_continues_positives",
                    "abstraction_leap": "de_géométrique_vers_analytique"
                },
                "cognitive_utility": "intuition_accumulation_continue",
                "pedagogical_value": 0.88,
                "precision_limit": 0.75,
                "relevance_score": 0.91
            },
            {
                "concept": "Analogie Vecteur Flèche",
                "definition": "Correspondance vecteur mathématique/flèche physique, direction/orientation, magnitude/longueur",
                "category": "mathematical_analogy",
                "source_domain": "objets_physiques",
                "target_domain": "algèbre_linéaire",
                "valid_mappings": {
                    "flèche": "vecteur_géométrique",
                    "longueur": "norme",
                    "direction": "direction_mathématique",
                    "bout_flèche": "point_arrivée",
                    "addition_forces": "addition_vectorielle"
                },
                "boundary_limits": {
                    "breakdown_points": ["espaces_abstraits", "dimensions_supérieures", "espaces_fonctionnels"],
                    "invalid_mappings": ["matière_physique ≠ entité_abstraite", "3D_visuel ≠ nD_mathématique"],
                    "domain_restrictions": "vecteurs_géométriques_2D_3D",
                    "conceptual_limitation": "visualisation_limitée_dimensions"
                },
                "cognitive_utility": "intuition_géométrique_opérations",
                "pedagogical_value": 0.85,
                "precision_limit": 0.7,
                "relevance_score": 0.89
            }
        ]
        
        return self._convert_to_atoms(concepts, "mathematical_analogies")
    
    def collect_analogy_failures(self) -> List[Dict]:
        """Échecs analogies célèbres - leçons limites"""
        concepts = [
            {
                "concept": "Échec Analogie Éther Luminifère",
                "definition": "Analogie son/air → lumière/éther échoue, révèle nature ondulatoire sans support matériel",
                "category": "historical_failure",
                "failed_mapping": {
                    "source_domain": "propagation_son_air",
                    "target_domain": "propagation_lumière",
                    "assumed_correspondence": "air/son → éther/lumière"
                },
                "failure_points": {
                    "empirical_refutation": "expérience_michelson_morley",
                    "theoretical_breakthrough": "relativité_restreinte",
                    "conceptual_revolution": "ondes_sans_support_matériel"
                },
                "lessons_learned": {
                    "analogie_limitation": "similarité_superficielle_trompeuse",
                    "empirical_necessity": "test_expérimental_crucial",
                    "paradigm_shift": "abandon_analogie_pour_nouveau_concept"
                },
                "cognitive_impact": "révision_concepts_fondamentaux",
                "historical_importance": 0.95,
                "relevance_score": 0.88
            },
            {
                "concept": "Piège Analogie Vitesse Lumière Projectile",
                "definition": "Analogie vitesse projectile/vitesse lumière échoue, révèle relativité et limite universelle",
                "category": "conceptual_trap",
                "failed_mapping": {
                    "source_domain": "mécanique_classique",
                    "target_domain": "électromagnétisme",
                    "assumed_correspondence": "addition_vitesses_galileenne"
                },
                "failure_points": {
                    "invariance_c": "vitesse_lumière_constante",
                    "relativistic_effects": "dilatation_temps_contraction_espace",
                    "energy_mass": "équivalence_masse_énergie"
                },
                "lessons_learned": {
                    "universal_constants": "certaines_quantités_absolues",
                    "scale_dependence": "physique_change_selon_échelle",
                    "counter_intuitive": "réalité_dépasse_intuition_quotidienne"
                },
                "cognitive_impact": "révision_concepts_espace_temps",
                "historical_importance": 0.92,
                "relevance_score": 0.86
            }
        ]
        
        return self._convert_to_atoms(concepts, "analogy_failures")
    
    def collect_metaanalogy_theory(self) -> List[Dict]:
        """Théorie méta-analogique - structure mappings cognitifs"""
        concepts = [
            {
                "concept": "Structure Mapping Theory",
                "definition": "Théorie Gentner: analogie = alignement structures relationnelles préservant consistance systématique",
                "category": "cognitive_theory",
                "mapping_principles": {
                    "systematicity": "préférence_systèmes_relations_cohérents",
                    "one_to_one": "correspondance_unique_éléments",
                    "parallel_connectivity": "préservation_structure_relationnelle"
                },
                "analogy_components": {
                    "surface_similarity": "similarités_superficielles_attributs",
                    "structural_alignment": "correspondance_relations_profondes",
                    "pragmatic_centrality": "importance_but_analogie"
                },
                "quality_factors": {
                    "systematicity_principle": "cohérence_système_relations",
                    "semantic_similarity": "proximité_domaines_source_cible",
                    "pragmatic_importance": "pertinence_objectif_cognitif"
                },
                "cognitive_utility": "modèle_traitement_analogique",
                "theoretical_support": 0.9,
                "relevance_score": 0.94
            },
            {
                "concept": "Analogical Reasoning Limits",
                "definition": "Limites raisonnement analogique: bootstrap problem, projection sélective, induction superficielle",
                "category": "cognitive_limits",
                "limitation_types": {
                    "bootstrap_problem": "analogie_nécessite_connaissance_préalable",
                    "selective_projection": "choix_aspects_mappés_subjectif",
                    "surface_similarity_bias": "piège_similarités_superficielles",
                    "overgeneralization": "extension_excessive_domaine_validité"
                },
                "mitigation_strategies": {
                    "explicit_boundary_marking": "délimitation_explicite_domaine",
                    "multiple_analogies": "triangulation_analogies_multiples",
                    "empirical_validation": "test_prédictions_analogiques",
                    "structural_focus": "privilégier_relations_sur_attributs"
                },
                "panini_implications": {
                    "boundary_atoms": "atomes_frontières_explicites",
                    "analogy_markers": "marquage_nature_analogique",
                    "validity_scope": "domaine_validité_encodé",
                    "confidence_gradation": "gradation_confiance_mapping"
                },
                "cognitive_utility": "prévention_erreurs_analogiques",
                "theoretical_support": 0.85,
                "relevance_score": 0.91
            }
        ]
        
        return self._convert_to_atoms(concepts, "metaanalogy_theory")
    
    def _convert_to_atoms(self, concepts: List[Dict], collection_type: str) -> List[Dict]:
        """Conversion concepts analogiques en atomes avec marquage spécialisé"""
        atoms = []
        
        for i, concept_data in enumerate(concepts):
            # Extraction marquage analogique spécialisé
            analogy_markers = self._extract_analogy_markers(concept_data)
            
            atom = {
                "concept": concept_data["concept"],
                "definition": concept_data["definition"],
                "category": concept_data["category"],
                "analogy_structure": analogy_markers,
                "metadata": {
                    key: value for key, value in concept_data.items()
                    if key not in ["concept", "definition", "category"]
                },
                "provenance": {
                    "source_agent": "analogy_collector",
                    "timestamp": datetime.datetime.now().isoformat(),
                    "extraction_confidence": concept_data.get("relevance_score", 0.85),
                    "collection_method": f"structured_{collection_type}",
                    "atom_id": f"analogy_{datetime.datetime.now().strftime('%Y%m%d')}_{collection_type}_{i:03d}"
                }
            }
            atoms.append(atom)
        
        return atoms
    
    def _extract_analogy_markers(self, concept_data: Dict) -> Dict:
        """Extraction marqueurs analogiques selon structure PaniniFS"""
        markers = {
            "analogy_type": "explicit_marked_analogy",
            "mapping_quality": "provisional_with_boundaries"
        }
        
        # Marquage domaines source/cible si présents
        if "source_domain" in concept_data and "target_domain" in concept_data:
            markers["domain_mapping"] = {
                "source": concept_data["source_domain"],
                "target": concept_data["target_domain"],
                "mapping_direction": "source_to_target"
            }
        
        # Marquage limites si présentes
        if "boundary_limits" in concept_data:
            markers["boundary_conditions"] = concept_data["boundary_limits"]
            markers["validity_scope"] = "limited_domain_with_explicit_boundaries"
        
        # Marquage correspondances valides/invalides
        if "valid_mappings" in concept_data:
            markers["valid_correspondences"] = concept_data["valid_mappings"]
        
        if "invalid_mappings" in concept_data.get("boundary_limits", {}):
            markers["invalid_correspondences"] = concept_data["boundary_limits"]["invalid_mappings"]
        
        # Utilité cognitive et limites précision
        if "cognitive_utility" in concept_data:
            markers["cognitive_function"] = concept_data["cognitive_utility"]
        
        if "precision_limit" in concept_data:
            markers["precision_boundary"] = concept_data["precision_limit"]
            markers["warning"] = "analogie_mnémonique_limites_explicites"
        
        return markers
    
    def collect_all_analogies(self) -> List[Dict]:
        """Collection complète analogies avec marquage limites"""
        all_atoms = []
        
        print("🧠 Collecte analogies cognitives...")
        all_atoms.extend(self.collect_cognitive_analogies())
        
        print("🔢 Collecte analogies mathématiques...")
        all_atoms.extend(self.collect_mathematical_analogies())
        
        print("❌ Collecte échecs analogiques...")
        all_atoms.extend(self.collect_analogy_failures())
        
        print("🎯 Collecte théorie méta-analogique...")
        all_atoms.extend(self.collect_metaanalogy_theory())
        
        return all_atoms
    
    def save_collection(self, filename: str = "analogy_semantic_store.json"):
        """Sauvegarde collection analogies avec structure marquage"""
        atoms = self.collect_all_analogies()
        self.store["semantic_atoms"] = atoms
        self.store["metadata"]["total_atoms"] = len(atoms)
        
        # Analyse marqueurs analogiques
        analogy_stats = {
            "explicit_boundaries": 0,
            "domain_mappings": 0,
            "precision_limits": 0,
            "cognitive_utilities": 0
        }
        
        for atom in atoms:
            markers = atom.get("analogy_structure", {})
            if "boundary_conditions" in markers:
                analogy_stats["explicit_boundaries"] += 1
            if "domain_mapping" in markers:
                analogy_stats["domain_mappings"] += 1
            if "precision_boundary" in markers:
                analogy_stats["precision_limits"] += 1
            if "cognitive_function" in markers:
                analogy_stats["cognitive_utilities"] += 1
        
        self.store["metadata"]["analogy_markers"] = analogy_stats
        self.store["metadata"]["boundary_marking_principle"] = "toute_analogie_avec_limites_explicites"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.store, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Collection analogies sauvée: {filename}")
        print(f"📊 {len(atoms)} analogies collectées avec marquage limites")
        print(f"🔗 Marqueurs analogiques:")
        print(f"   • {analogy_stats['explicit_boundaries']} frontières explicites")
        print(f"   • {analogy_stats['domain_mappings']} mappings domaines")
        print(f"   • {analogy_stats['precision_limits']} limites précision")
        print(f"   • {analogy_stats['cognitive_utilities']} utilités cognitives")
        
        return len(atoms)

def main():
    print("🔗 COLLECTEUR ANALOGIES AVEC MARQUAGE LIMITES")
    print("==============================================")
    print("🎯 Analogies cognitives, échecs historiques, méta-théorie")
    print("⚠️  Marquage explicite domaines validité et frontières")
    print("")
    
    collector = AnalogyCollector()
    total_collected = collector.save_collection()
    
    print(f"\n🏆 COLLECTION TERMINÉE")
    print(f"📈 {total_collected} analogies avec marquage limites intégrées")
    print(f"🌟 PaniniFS enrichi avec mécanisme analogique sécurisé!")
    print(f"⚠️  Chaque analogie marquée avec frontières explicites!")

if __name__ == "__main__":
    main()
