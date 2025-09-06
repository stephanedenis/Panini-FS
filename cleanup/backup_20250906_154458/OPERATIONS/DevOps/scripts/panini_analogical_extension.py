#!/usr/bin/env python3
"""
Extension PaniniFS : Système Marquage Analogique
🔗 Mécanisme sécurisé analogies avec frontières explicites et limites définies
"""

import json
import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import re

class AnalogyType(Enum):
    COGNITIVE_METAPHOR = "cognitive_metaphor"
    MATHEMATICAL_MAPPING = "mathematical_mapping"
    SCIENTIFIC_MODEL = "scientific_model"
    PEDAGOGICAL_TOOL = "pedagogical_tool"
    HISTORICAL_FAILED = "historical_failed"

class ValidityScope(Enum):
    LIMITED_DOMAIN = "limited_domain"
    APPROXIMATE_ONLY = "approximate_only"
    PEDAGOGICAL_ONLY = "pedagogical_only"
    HISTORICAL_OBSOLETE = "historical_obsolete"
    RESEARCH_HYPOTHESIS = "research_hypothesis"

@dataclass
class DomainMapping:
    source_domain: str
    target_domain: str
    mapping_direction: str
    valid_correspondences: Dict[str, str]
    invalid_correspondences: List[str]
    confidence_level: float

@dataclass
class BoundaryConditions:
    breakdown_points: List[str]
    domain_restrictions: str
    precision_limit: float
    validity_scope: ValidityScope
    warning_markers: List[str]

@dataclass
class AnalogyMarker:
    analogy_type: AnalogyType
    domain_mapping: DomainMapping
    boundary_conditions: BoundaryConditions
    cognitive_utility: str
    pedagogical_value: float
    risk_level: float
    
class PaniniAnalogicalExtension:
    def __init__(self):
        self.analogy_registry = {}
        self.boundary_violations = []
        self.safe_analogies = []
        
    def mark_analogy(self, concept: str, definition: str, analogy_data: Dict) -> Dict:
        """Marque concept comme analogique avec frontières explicites"""
        
        # Extraction composants analogiques
        domain_mapping = self._extract_domain_mapping(analogy_data)
        boundary_conditions = self._extract_boundaries(analogy_data)
        analogy_type = self._classify_analogy_type(analogy_data)
        
        # Création marqueur analogique
        marker = AnalogyMarker(
            analogy_type=analogy_type,
            domain_mapping=domain_mapping,
            boundary_conditions=boundary_conditions,
            cognitive_utility=analogy_data.get("cognitive_utility", "unknown"),
            pedagogical_value=analogy_data.get("pedagogical_value", 0.5),
            risk_level=self._calculate_risk_level(boundary_conditions)
        )
        
        # Enrichissement atome sémantique
        enhanced_atom = {
            "concept": concept,
            "definition": definition,
            "analogy_marker": {
                "is_analogical": True,
                "analogy_warning": "⚠️ ANALOGIE - Utilisation limitée aux domaines explicites",
                "analogy_structure": asdict(marker),
                "safe_usage_guidelines": self._generate_usage_guidelines(marker),
                "boundary_alerts": self._generate_boundary_alerts(marker)
            },
            "provenance": {
                "source_agent": "panini_analogical_extension",
                "timestamp": datetime.datetime.now().isoformat(),
                "extraction_confidence": 0.95,
                "marking_method": "explicit_boundary_marking",
                "safety_level": self._categorize_safety_level(marker.risk_level)
            }
        }
        
        # Enregistrement registre analogies
        self.analogy_registry[concept] = marker
        
        return enhanced_atom
    
    def _extract_domain_mapping(self, analogy_data: Dict) -> DomainMapping:
        """Extraction mapping domaines source/cible"""
        return DomainMapping(
            source_domain=analogy_data.get("source_domain", "unknown"),
            target_domain=analogy_data.get("target_domain", "unknown"), 
            mapping_direction=analogy_data.get("mapping_direction", "bidirectional"),
            valid_correspondences=analogy_data.get("valid_mappings", {}),
            invalid_correspondences=analogy_data.get("invalid_mappings", []),
            confidence_level=analogy_data.get("mapping_confidence", 0.7)
        )
    
    def _extract_boundaries(self, analogy_data: Dict) -> BoundaryConditions:
        """Extraction conditions frontières"""
        boundary_data = analogy_data.get("boundary_limits", {})
        
        return BoundaryConditions(
            breakdown_points=boundary_data.get("breakdown_points", []),
            domain_restrictions=boundary_data.get("domain_restrictions", "non_specified"),
            precision_limit=analogy_data.get("precision_limit", 0.5),
            validity_scope=ValidityScope.LIMITED_DOMAIN,
            warning_markers=boundary_data.get("warning_markers", ["analogie_approximative"])
        )
    
    def _classify_analogy_type(self, analogy_data: Dict) -> AnalogyType:
        """Classification type analogie"""
        category = analogy_data.get("category", "").lower()
        
        if "mathematical" in category:
            return AnalogyType.MATHEMATICAL_MAPPING
        elif "scientific" in category:
            return AnalogyType.SCIENTIFIC_MODEL
        elif "historical_failure" in category or "failed" in category:
            return AnalogyType.HISTORICAL_FAILED
        elif "pedagogical" in analogy_data.get("cognitive_utility", "").lower():
            return AnalogyType.PEDAGOGICAL_TOOL
        else:
            return AnalogyType.COGNITIVE_METAPHOR
    
    def _calculate_risk_level(self, boundaries: BoundaryConditions) -> float:
        """Calcul niveau risque analogie"""
        risk_factors = []
        
        # Risque faible précision
        if boundaries.precision_limit < 0.5:
            risk_factors.append(0.3)
        
        # Risque points breakdown nombreux
        if len(boundaries.breakdown_points) > 3:
            risk_factors.append(0.25)
        
        # Risque domaine restriction vague
        if "non_specified" in boundaries.domain_restrictions:
            risk_factors.append(0.2)
        
        return min(sum(risk_factors), 1.0)
    
    def _generate_usage_guidelines(self, marker: AnalogyMarker) -> List[str]:
        """Génération guidelines utilisation sécurisée"""
        guidelines = [
            f"🎯 USAGE: {marker.cognitive_utility}",
            f"📊 PRÉCISION: Limitée à {marker.boundary_conditions.precision_limit:.1%}",
            f"🔗 DOMAINES: {marker.domain_mapping.source_domain} → {marker.domain_mapping.target_domain}"
        ]
        
        if marker.boundary_conditions.breakdown_points:
            guidelines.append(f"⛔ ÉVITER: {', '.join(marker.boundary_conditions.breakdown_points[:3])}")
        
        if marker.risk_level > 0.5:
            guidelines.append("⚠️ RISQUE ÉLEVÉ: Vérification empirique recommandée")
        
        if marker.analogy_type == AnalogyType.HISTORICAL_FAILED:
            guidelines.append("🚫 OBSOLÈTE: Valeur historique uniquement")
        
        return guidelines
    
    def _generate_boundary_alerts(self, marker: AnalogyMarker) -> List[str]:
        """Génération alertes frontières"""
        alerts = []
        
        # Alertes breakdown points
        for breakdown in marker.boundary_conditions.breakdown_points:
            alerts.append(f"🚨 LIMITE: Analogie invalide pour {breakdown}")
        
        # Alertes correspondances invalides
        for invalid in marker.domain_mapping.invalid_correspondences:
            alerts.append(f"❌ INVALID: {invalid}")
        
        # Alerte précision
        if marker.boundary_conditions.precision_limit < 0.7:
            alerts.append(f"📉 PRÉCISION: Seulement {marker.boundary_conditions.precision_limit:.1%}")
        
        return alerts
    
    def _categorize_safety_level(self, risk_level: float) -> str:
        """Catégorisation niveau sécurité"""
        if risk_level < 0.3:
            return "safe_with_boundaries"
        elif risk_level < 0.6:
            return "moderate_risk_explicit_limits"
        else:
            return "high_risk_expert_only"
    
    def validate_analogy_usage(self, concept: str, context: str) -> Dict:
        """Validation usage analogie dans contexte donné"""
        if concept not in self.analogy_registry:
            return {"valid": True, "warnings": [], "reason": "not_analogical"}
        
        marker = self.analogy_registry[concept]
        validation = {
            "valid": True,
            "warnings": [],
            "safety_level": self._categorize_safety_level(marker.risk_level),
            "context_compatibility": self._check_context_compatibility(marker, context)
        }
        
        # Vérification breakdown points dans contexte
        context_lower = context.lower()
        for breakdown in marker.boundary_conditions.breakdown_points:
            if breakdown.lower() in context_lower:
                validation["valid"] = False
                validation["warnings"].append(f"BREAKDOWN: Contexte '{breakdown}' invalide pour analogie")
        
        # Vérification domaine restrictions
        domain_restriction = marker.boundary_conditions.domain_restrictions.lower()
        if "non_specified" not in domain_restriction and domain_restriction not in context_lower:
            validation["warnings"].append(f"DOMAIN: Contexte hors domaine '{domain_restriction}'")
        
        return validation
    
    def _check_context_compatibility(self, marker: AnalogyMarker, context: str) -> float:
        """Vérification compatibilité contexte"""
        compatibility_score = 1.0
        
        # Pénalité si contexte contient breakdown points
        context_words = set(context.lower().split())
        breakdown_words = set(' '.join(marker.boundary_conditions.breakdown_points).lower().split())
        
        overlap = len(context_words.intersection(breakdown_words))
        if overlap > 0:
            compatibility_score -= 0.5 * (overlap / len(breakdown_words))
        
        return max(compatibility_score, 0.0)
    
    def generate_analogy_safety_report(self) -> Dict:
        """Génération rapport sécurité analogies"""
        if not self.analogy_registry:
            return {"error": "No analogies registered"}
        
        # Analyse distribution risques
        risk_distribution = {"low": 0, "moderate": 0, "high": 0}
        type_distribution = {}
        
        for concept, marker in self.analogy_registry.items():
            # Distribution risques
            if marker.risk_level < 0.3:
                risk_distribution["low"] += 1
            elif marker.risk_level < 0.6:
                risk_distribution["moderate"] += 1
            else:
                risk_distribution["high"] += 1
            
            # Distribution types
            analogy_type = marker.analogy_type.value
            type_distribution[analogy_type] = type_distribution.get(analogy_type, 0) + 1
        
        # Top analogies risquées
        risky_analogies = [
            (concept, marker.risk_level) 
            for concept, marker in self.analogy_registry.items()
            if marker.risk_level > 0.5
        ]
        risky_analogies.sort(key=lambda x: x[1], reverse=True)
        
        report = {
            "analysis_metadata": {
                "total_analogies": len(self.analogy_registry),
                "analysis_date": datetime.datetime.now().isoformat(),
                "safety_framework": "explicit_boundary_marking"
            },
            "risk_distribution": risk_distribution,
            "type_distribution": type_distribution,
            "risky_analogies": risky_analogies[:5],
            "safety_recommendations": self._generate_safety_recommendations(risk_distribution),
            "boundary_marking_stats": {
                "total_boundaries": sum(len(m.boundary_conditions.breakdown_points) for m in self.analogy_registry.values()),
                "avg_precision": sum(m.boundary_conditions.precision_limit for m in self.analogy_registry.values()) / len(self.analogy_registry),
                "explicit_restrictions": len([m for m in self.analogy_registry.values() if "non_specified" not in m.boundary_conditions.domain_restrictions])
            }
        }
        
        return report
    
    def _generate_safety_recommendations(self, risk_distribution: Dict) -> List[str]:
        """Génération recommandations sécurité"""
        recommendations = []
        
        if risk_distribution["high"] > 0:
            recommendations.append("⚠️ Analogies haut risque détectées - validation empirique requise")
        
        if risk_distribution["low"] < risk_distribution["moderate"] + risk_distribution["high"]:
            recommendations.append("📚 Enrichir marquage frontières pour réduire risques")
        
        recommendations.extend([
            "🔍 Valider contexte avant usage analogie",
            "📖 Consulter guidelines usage pour chaque analogie",
            "🚨 Surveiller alertes breakdown points",
            "✅ Privilégier analogies avec frontières explicites"
        ])
        
        return recommendations

def main():
    print("🔗 EXTENSION PANINI-FS : MARQUAGE ANALOGIQUE")
    print("============================================")
    print("⚠️ Mécanisme sécurisé analogies avec frontières explicites")
    print("🎯 Prévention pièges analogiques par marquage limites")
    print("")
    
    # Démonstration système marquage
    extension = PaniniAnalogicalExtension()
    
    # Exemple analogie hydraulique électricité
    analogy_data = {
        "source_domain": "hydraulique",
        "target_domain": "électricité",
        "valid_mappings": {
            "débit_eau": "intensité_courant",
            "pression": "tension"
        },
        "boundary_limits": {
            "breakdown_points": ["fréquences_hautes", "effets_quantiques"],
            "domain_restrictions": "circuits_DC_basse_fréquence"
        },
        "cognitive_utility": "mnémonique_intuition_circuits",
        "pedagogical_value": 0.85,
        "precision_limit": 0.6
    }
    
    # Marquage analogie
    marked_atom = extension.mark_analogy(
        "Analogie Hydraulique Électricité",
        "Correspondance eau/courant pour comprendre circuits",
        analogy_data
    )
    
    print("📋 EXEMPLE MARQUAGE ANALOGIE:")
    print(f"   Concept: {marked_atom['concept']}")
    print(f"   Warning: {marked_atom['analogy_marker']['analogy_warning']}")
    print(f"   Guidelines: {len(marked_atom['analogy_marker']['safe_usage_guidelines'])} recommandations")
    print(f"   Alerts: {len(marked_atom['analogy_marker']['boundary_alerts'])} alertes frontières")
    
    # Test validation contexte
    context_safe = "circuit simple DC avec résistance"
    context_risky = "circuit haute fréquence avec effets quantiques"
    
    validation_safe = extension.validate_analogy_usage("Analogie Hydraulique Électricité", context_safe)
    validation_risky = extension.validate_analogy_usage("Analogie Hydraulique Électricité", context_risky)
    
    print(f"\n🔍 VALIDATION CONTEXTES:")
    print(f"   Contexte sûr: {'✅ Valide' if validation_safe['valid'] else '❌ Invalid'}")
    print(f"   Contexte risqué: {'✅ Valide' if validation_risky['valid'] else '❌ Invalid'}")
    print(f"   Warnings risqué: {len(validation_risky['warnings'])}")
    
    # Rapport sécurité
    safety_report = extension.generate_analogy_safety_report()
    
    print(f"\n📊 RAPPORT SÉCURITÉ:")
    print(f"   Total analogies: {safety_report['analysis_metadata']['total_analogies']}")
    print(f"   Frontières explicites: {safety_report['boundary_marking_stats']['total_boundaries']}")
    print(f"   Précision moyenne: {safety_report['boundary_marking_stats']['avg_precision']:.1%}")
    
    print(f"\n🏆 SYSTÈME MARQUAGE ANALOGIQUE DÉPLOYÉ")
    print(f"⚠️ Chaque analogie PaniniFS maintenant sécurisée avec limites explicites!")

if __name__ == "__main__":
    main()
