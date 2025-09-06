#!/usr/bin/env python3
"""
Advanced Consensus Engine : Algorithmes consensus sophistiqués
Features: Temporal weighting, Authority scoring, Conflict resolution, Cross-validation
"""

import json
import datetime
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set, Optional
import sys
import os
import math
from dataclasses import dataclass, asdict

# Import structures communes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

@dataclass
class AuthorityProfile:
    agent_id: str
    expertise_domains: List[str]
    historical_accuracy: float
    source_reliability: float
    temporal_consistency: float
    peer_validation_score: float

@dataclass
class ConflictResolution:
    concept: str
    conflicting_definitions: List[Tuple[str, str, float]]  # (definition, source, confidence)
    resolution_method: str
    resolved_definition: str
    resolution_confidence: float
    dissent_sources: List[str]

@dataclass
class AdvancedConsensus:
    concept: str
    weighted_confidence: float
    temporal_stability: float
    authority_backing: float
    cross_validation_score: float
    conflict_resolution: Optional[ConflictResolution]
    consensus_evolution: List[Tuple[str, float]]  # (timestamp, confidence)

class AdvancedConsensusEngine:
    def __init__(self):
        self.stores = {}
        self.all_atoms = []
        self.concept_index = defaultdict(list)
        self.authority_profiles = {}
        
    def load_all_sources(self) -> int:
        """Charge toutes les sources disponibles"""
        sources_config = [
            ("demo_semantic_store.json", "wikipedia"),
            ("arxiv_semantic_store.json", "arxiv"),
            ("historical_books_semantic_store.json", "historical_books"),
            ("temporal_emergence_analysis.json", "temporal_analysis")
        ]
        
        total_loaded = 0
        
        for filename, source_type in sources_config:
            if os.path.exists(filename):
                loaded = self._load_source(filename, source_type)
                total_loaded += loaded
                print(f"📊 {source_type}: {loaded} atomes chargés")
            else:
                print(f"⚠️  {filename} non trouvé")
                
        return total_loaded
    
    def _load_source(self, filename: str, source_type: str) -> int:
        """Charge source avec enrichissement métadonnées"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                store = json.load(f)
                
            self.stores[source_type] = store
            atoms = store.get('semantic_atoms', [])
            
            for atom in atoms:
                atom['source_type'] = source_type
                atom['authority_weight'] = self._calculate_source_authority(source_type)
                self.all_atoms.append(atom)
                
                concept = atom['concept'].lower().strip()
                self.concept_index[concept].append(atom)
                
            return len(atoms)
            
        except Exception as e:
            print(f"❌ Erreur chargement {filename}: {e}")
            return 0
    
    def _calculate_source_authority(self, source_type: str) -> float:
        """Calcule poids autorité par type source"""
        authority_weights = {
            "arxiv": 0.9,              # Haute autorité académique
            "historical_books": 0.85,   # Autorité historique validée
            "wikipedia": 0.7,           # Autorité populaire modérée
            "temporal_analysis": 0.6    # Autorité analytique
        }
        return authority_weights.get(source_type, 0.5)
    
    def build_authority_profiles(self):
        """Construction profils autorité agents"""
        print("👑 Construction profils autorité agents...")
        
        agent_stats = defaultdict(lambda: {
            'concepts': set(),
            'sources': set(),
            'confidences': [],
            'domains': Counter(),
            'timestamps': []
        })
        
        # Collecte statistiques par agent
        for atom in self.all_atoms:
            agent_id = atom['provenance']['source_agent']
            stats = agent_stats[agent_id]
            
            stats['concepts'].add(atom['concept'])
            stats['sources'].add(atom['source_type'])
            stats['confidences'].append(atom['provenance']['extraction_confidence'])
            stats['timestamps'].append(atom['provenance']['timestamp'])
            
            # Domaine détection (heuristique)
            concept = atom['concept'].lower()
            if any(word in concept for word in ['learning', 'neural', 'algorithm']):
                stats['domains']['ai_ml'] += 1
            elif any(word in concept for word in ['philosophy', 'reason', 'knowledge']):
                stats['domains']['philosophy'] += 1
            elif any(word in concept for word in ['economics', 'wealth', 'market']):
                stats['domains']['economics'] += 1
            else:
                stats['domains']['general'] += 1
        
        # Génération profils autorité
        for agent_id, stats in agent_stats.items():
            if len(stats['concepts']) >= 5:  # Seuil minimum
                profile = self._calculate_authority_profile(agent_id, stats)
                self.authority_profiles[agent_id] = profile
        
        print(f"  ✅ {len(self.authority_profiles)} profils autorité générés")
    
    def _calculate_authority_profile(self, agent_id: str, stats: Dict) -> AuthorityProfile:
        """Calcule profil autorité détaillé"""
        # Expertise domains (top domains)
        top_domains = [domain for domain, count in stats['domains'].most_common(3)]
        
        # Historical accuracy (confidence moyenne)
        historical_accuracy = sum(stats['confidences']) / len(stats['confidences'])
        
        # Source reliability (diversité sources)
        source_reliability = min(len(stats['sources']) / 3, 1.0)  # Max 3 sources
        
        # Temporal consistency (régularité extractions)
        temporal_consistency = min(len(stats['timestamps']) / 100, 1.0)  # Normalisation
        
        # Peer validation (sera calculé cross-références)
        peer_validation_score = 0.7  # Default, à améliorer
        
        return AuthorityProfile(
            agent_id=agent_id,
            expertise_domains=top_domains,
            historical_accuracy=historical_accuracy,
            source_reliability=source_reliability,
            temporal_consistency=temporal_consistency,
            peer_validation_score=peer_validation_score
        )
    
    def detect_conflicts(self, concept: str) -> Optional[ConflictResolution]:
        """Détecte et résout conflits pour un concept"""
        atoms = self.concept_index.get(concept.lower(), [])
        
        if len(atoms) < 2:
            return None
        
        # Extraction définitions + métadonnées
        definitions = []
        for atom in atoms:
            definition = atom['definition']
            source = atom['source_type']
            confidence = atom['provenance']['extraction_confidence']
            definitions.append((definition, source, confidence))
        
        # Détection conflits (définitions très différentes)
        if self._are_definitions_conflicting(definitions):
            return self._resolve_conflict(concept, definitions)
        
        return None
    
    def _are_definitions_conflicting(self, definitions: List[Tuple[str, str, float]]) -> bool:
        """Détecte si définitions sont en conflit"""
        if len(definitions) < 2:
            return False
        
        # Heuristique simple: longueur très différente ou mots-clés opposés
        lengths = [len(def_text) for def_text, _, _ in definitions]
        max_length, min_length = max(lengths), min(lengths)
        
        # Conflit si ratio longueur > 3 ou keywords très différents
        if max_length > 3 * min_length:
            return True
        
        # TODO: Analyse sémantique plus sophistiquée
        return False
    
    def _resolve_conflict(self, concept: str, definitions: List[Tuple[str, str, float]]) -> ConflictResolution:
        """Résout conflit par pondération autorité"""
        # Tri par autorité + confidence
        weighted_definitions = []
        for definition, source, confidence in definitions:
            authority_weight = self._calculate_source_authority(source)
            weighted_score = confidence * authority_weight
            weighted_definitions.append((definition, source, confidence, weighted_score))
        
        # Résolution: définition avec score pondéré max
        best_definition = max(weighted_definitions, key=lambda x: x[3])
        resolved_def = best_definition[0]
        resolution_confidence = best_definition[3]
        
        # Sources en désaccord
        dissent_sources = [source for _, source, _, score in weighted_definitions 
                          if score < resolution_confidence * 0.8]
        
        return ConflictResolution(
            concept=concept,
            conflicting_definitions=[(d, s, c) for d, s, c, _ in weighted_definitions],
            resolution_method="authority_weighted_voting",
            resolved_definition=resolved_def,
            resolution_confidence=resolution_confidence,
            dissent_sources=dissent_sources
        )
    
    def calculate_advanced_consensus(self, concept: str) -> AdvancedConsensus:
        """Calcule consensus avancé pour concept"""
        atoms = self.concept_index.get(concept.lower(), [])
        
        if not atoms:
            return None
        
        # Metrics composites
        weighted_confidence = self._calculate_weighted_confidence(atoms)
        temporal_stability = self._calculate_temporal_stability(atoms)
        authority_backing = self._calculate_authority_backing(atoms)
        cross_validation_score = self._calculate_cross_validation_score(atoms)
        
        # Détection conflits
        conflict_resolution = self.detect_conflicts(concept)
        
        # Évolution consensus (simulation timeline)
        consensus_evolution = self._calculate_consensus_evolution(atoms)
        
        return AdvancedConsensus(
            concept=concept,
            weighted_confidence=weighted_confidence,
            temporal_stability=temporal_stability,
            authority_backing=authority_backing,
            cross_validation_score=cross_validation_score,
            conflict_resolution=conflict_resolution,
            consensus_evolution=consensus_evolution
        )
    
    def _calculate_weighted_confidence(self, atoms: List[Dict]) -> float:
        """Confidence pondérée par autorité sources"""
        total_weight = 0
        weighted_sum = 0
        
        for atom in atoms:
            confidence = atom['provenance']['extraction_confidence']
            authority = atom['authority_weight']
            weight = authority
            
            weighted_sum += confidence * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0
    
    def _calculate_temporal_stability(self, atoms: List[Dict]) -> float:
        """Stabilité temporelle concept"""
        if len(atoms) <= 1:
            return 1.0
        
        # Variance confidence dans le temps
        confidences = [atom['provenance']['extraction_confidence'] for atom in atoms]
        mean_conf = sum(confidences) / len(confidences)
        variance = sum((c - mean_conf)**2 for c in confidences) / len(confidences)
        
        stability = max(0, 1.0 - variance * 2)  # Conversion variance -> stabilité
        return stability
    
    def _calculate_authority_backing(self, atoms: List[Dict]) -> float:
        """Score soutien autorités"""
        authority_scores = [atom['authority_weight'] for atom in atoms]
        return sum(authority_scores) / len(authority_scores) if authority_scores else 0
    
    def _calculate_cross_validation_score(self, atoms: List[Dict]) -> float:
        """Score validation croisée sources multiples"""
        sources = set(atom['source_type'] for atom in atoms)
        agents = set(atom['provenance']['source_agent'] for atom in atoms)
        
        # Score basé sur diversité
        source_diversity = min(len(sources) / 3, 1.0)  # Max 3 types sources
        agent_diversity = min(len(agents) / 5, 1.0)    # Max 5 agents
        
        return (source_diversity + agent_diversity) / 2
    
    def _calculate_consensus_evolution(self, atoms: List[Dict]) -> List[Tuple[str, float]]:
        """Timeline évolution consensus"""
        # Tri temporel
        sorted_atoms = sorted(atoms, key=lambda x: x['provenance']['timestamp'])
        
        evolution = []
        cumulative_confidence = 0
        
        for i, atom in enumerate(sorted_atoms, 1):
            cumulative_confidence += atom['provenance']['extraction_confidence']
            avg_confidence = cumulative_confidence / i
            
            timestamp = atom['provenance']['timestamp'][:10]  # Date seulement
            evolution.append((timestamp, round(avg_confidence, 3)))
        
        return evolution
    
    def generate_comprehensive_consensus_report(self) -> Dict:
        """Rapport consensus avancé complet"""
        print("\n🧠 GÉNÉRATION RAPPORT CONSENSUS AVANCÉ")
        print("=" * 40)
        
        # Construction profils autorité
        self.build_authority_profiles()
        
        # Analyse concepts prioritaires
        concept_priorities = Counter()
        for concept, atoms in self.concept_index.items():
            concept_priorities[concept] = len(atoms)
        
        top_concepts = [concept for concept, count in concept_priorities.most_common(20)]
        
        # Calcul consensus avancé
        advanced_consensuses = []
        conflicts_detected = []
        
        for concept in top_concepts:
            consensus = self.calculate_advanced_consensus(concept)
            if consensus:
                advanced_consensuses.append(asdict(consensus))
                
                if consensus.conflict_resolution:
                    conflicts_detected.append(asdict(consensus.conflict_resolution))
        
        # Métriques globales
        total_concepts = len(self.concept_index)
        consensus_scores = [c['weighted_confidence'] for c in advanced_consensuses]
        
        report = {
            "analysis_metadata": {
                "total_concepts": total_concepts,
                "analyzed_concepts": len(advanced_consensuses),
                "authority_profiles": len(self.authority_profiles),
                "conflicts_detected": len(conflicts_detected),
                "total_atoms": len(self.all_atoms),
                "analysis_date": datetime.datetime.now().isoformat(),
                "engine_version": "advanced_consensus_v2.0"
            },
            "authority_profiles": [asdict(profile) for profile in self.authority_profiles.values()],
            "advanced_consensuses": advanced_consensuses,
            "conflict_resolutions": conflicts_detected,
            "consensus_metrics": {
                "avg_weighted_confidence": sum(consensus_scores) / len(consensus_scores) if consensus_scores else 0,
                "consensus_distribution": Counter([round(score, 1) for score in consensus_scores]),
                "conflict_rate": len(conflicts_detected) / len(advanced_consensuses) if advanced_consensuses else 0
            },
            "recommendations": {
                "high_confidence_concepts": [c['concept'] for c in advanced_consensuses if c['weighted_confidence'] > 0.8],
                "needs_validation": [c['concept'] for c in advanced_consensuses if c['cross_validation_score'] < 0.5],
                "temporal_unstable": [c['concept'] for c in advanced_consensuses if c['temporal_stability'] < 0.6]
            }
        }
        
        return report
    
    def save_advanced_consensus_analysis(self, filename: str):
        """Sauvegarde analyse consensus avancée"""
        report = self.generate_comprehensive_consensus_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Analyse consensus avancée sauvée: {filename}")
        
        # Affichage résumé
        metadata = report['analysis_metadata']
        print(f"\n🧠 RÉSUMÉ CONSENSUS AVANCÉ:")
        print(f"   • {metadata['total_concepts']} concepts analysés")
        print(f"   • {metadata['authority_profiles']} profils autorité")
        print(f"   • {metadata['conflicts_detected']} conflits détectés")
        
        metrics = report['consensus_metrics']
        print(f"\n📊 MÉTRIQUES CONSENSUS:")
        print(f"   • Confidence pondérée moyenne: {metrics['avg_weighted_confidence']:.3f}")
        print(f"   • Taux conflits: {metrics['conflict_rate']:.3f}")
        
        recommendations = report['recommendations']
        print(f"\n💡 RECOMMANDATIONS:")
        print(f"   • {len(recommendations['high_confidence_concepts'])} concepts haute confiance")
        print(f"   • {len(recommendations['needs_validation'])} concepts nécessitent validation")
        print(f"   • {len(recommendations['temporal_unstable'])} concepts temporellement instables")
        
        return report

def main():
    print("🧠 MOTEUR CONSENSUS AVANCÉ")
    print("==========================")
    
    engine = AdvancedConsensusEngine()
    
    # Chargement toutes sources
    total_loaded = engine.load_all_sources()
    
    if total_loaded == 0:
        print("❌ Aucune source trouvée")
        return
    
    print(f"\n🔍 Analyse consensus avancée sur {total_loaded} atomes...")
    
    # Génération rapport consensus sophistiqué
    analysis_file = "advanced_consensus_analysis.json"
    report = engine.save_advanced_consensus_analysis(analysis_file)
    
    print(f"\n🎯 ANALYSE CONSENSUS AVANCÉE TERMINÉE")
    print(f"📄 Rapport détaillé: {analysis_file}")
    print(f"🏆 Algorithmes next-gen: Temporal weighting + Authority scoring + Conflict resolution")

if __name__ == "__main__":
    main()
