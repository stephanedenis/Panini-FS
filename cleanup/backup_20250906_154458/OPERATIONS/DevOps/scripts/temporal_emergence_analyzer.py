#!/usr/bin/env python3
"""
Analyseur Émergence Temporelle : Détection patterns évolution concepts
Focus: Timeline concepts, détection innovations, consensus historique vs moderne
"""

import json
import datetime
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set
import sys
import os
from dataclasses import dataclass

# Import structures communes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

@dataclass
class ConceptEvolution:
    concept: str
    timeline: List[Tuple[str, str]]  # (year/period, source)
    definitions_evolution: List[Tuple[str, str, str]]  # (year, definition, source)
    emergence_confidence: float
    stability_score: float
    innovation_markers: List[str]

class TemporalEmergenceAnalyzer:
    def __init__(self):
        self.stores = {}
        self.temporal_atoms = []
        self.concept_timeline = defaultdict(list)
        
    def load_temporal_stores(self) -> int:
        """Charge tous les stores avec données temporelles"""
        stores_config = [
            ("demo_semantic_store.json", "wikipedia", "2024"),
            ("arxiv_semantic_store.json", "arxiv", "2024"),
            ("historical_books_semantic_store.json", "historical_books", "1700-1900"),
            ("multi_source_consensus_analysis.json", "analysis", "2024")
        ]
        
        total_loaded = 0
        
        for filename, source_type, period in stores_config:
            if os.path.exists(filename):
                loaded = self._load_temporal_store(filename, source_type, period)
                total_loaded += loaded
                print(f"📊 {source_type} ({period}): {loaded} atomes temporels")
            else:
                print(f"⚠️  {filename} non trouvé")
                
        return total_loaded
    
    def _load_temporal_store(self, filename: str, source_type: str, period: str) -> int:
        """Charge store avec enrichissement temporel"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                store = json.load(f)
                
            atoms = store.get('semantic_atoms', [])
            
            for atom in atoms:
                # Enrichissement temporel
                temporal_atom = atom.copy()
                temporal_atom['source_type'] = source_type
                temporal_atom['period'] = period
                temporal_atom['temporal_weight'] = self._calculate_temporal_weight(atom, period)
                
                self.temporal_atoms.append(temporal_atom)
                
                # Index timeline par concept
                concept = atom['concept'].lower().strip()
                self.concept_timeline[concept].append({
                    'atom': temporal_atom,
                    'period': period,
                    'source': source_type,
                    'timestamp': atom['provenance']['timestamp'],
                    'confidence': atom['provenance']['extraction_confidence']
                })
                
            return len(atoms)
            
        except Exception as e:
            print(f"❌ Erreur chargement {filename}: {e}")
            return 0
    
    def _calculate_temporal_weight(self, atom: Dict, period: str) -> float:
        """Calcule poids temporel selon époque"""
        if period == "2024":
            return 1.0  # Moderne = poids max
        elif "1700-1900" in period:
            return 0.8  # Historique = poids réduit mais important
        else:
            return 0.9  # Default
    
    def detect_concept_emergence_patterns(self) -> List[ConceptEvolution]:
        """Détecte patterns émergence concepts cross-temporel"""
        print("🌱 Détection patterns émergence temporelle...")
        
        evolutions = []
        
        for concept, timeline_data in self.concept_timeline.items():
            if len(timeline_data) > 1:  # Multi-période seulement
                evolution = self._analyze_concept_evolution(concept, timeline_data)
                if evolution:
                    evolutions.append(evolution)
        
        # Tri par score émergence
        evolutions.sort(key=lambda x: x.emergence_confidence, reverse=True)
        
        print(f"  ✅ {len(evolutions)} patterns évolution détectés")
        return evolutions
    
    def _analyze_concept_evolution(self, concept: str, timeline_data: List[Dict]) -> ConceptEvolution:
        """Analyse évolution détaillée d'un concept"""
        # Construction timeline chronologique
        timeline = []
        definitions_evolution = []
        
        # Tri par période (historique → moderne)
        sorted_timeline = sorted(timeline_data, key=lambda x: self._period_to_numeric(x['period']))
        
        for entry in sorted_timeline:
            period = entry['period']
            source = entry['source']
            timeline.append((period, source))
            
            definition = entry['atom']['definition'][:100] + "..."
            definitions_evolution.append((period, definition, source))
        
        # Calcul scores
        emergence_confidence = self._calculate_emergence_confidence(sorted_timeline)
        stability_score = self._calculate_stability_score(sorted_timeline)
        innovation_markers = self._detect_innovation_markers(sorted_timeline)
        
        return ConceptEvolution(
            concept=concept,
            timeline=timeline,
            definitions_evolution=definitions_evolution,
            emergence_confidence=emergence_confidence,
            stability_score=stability_score,
            innovation_markers=innovation_markers
        )
    
    def _period_to_numeric(self, period: str) -> int:
        """Conversion période en numérique pour tri"""
        if "1700-1900" in period:
            return 1800  # Milieu période historique
        elif "2024" in period:
            return 2024
        else:
            return 2000  # Default moderne
    
    def _calculate_emergence_confidence(self, timeline_data: List[Dict]) -> float:
        """Score émergence basé sur progression temporelle"""
        if len(timeline_data) <= 1:
            return 0.0
            
        # Facteurs émergence
        confidence = 0.5  # Base
        
        # Bonus progression historique → moderne
        periods = [self._period_to_numeric(entry['period']) for entry in timeline_data]
        if max(periods) - min(periods) > 100:  # Span temporel significatif
            confidence += 0.3
            
        # Bonus confidence moyenne haute
        avg_confidence = sum(entry['confidence'] for entry in timeline_data) / len(timeline_data)
        confidence += (avg_confidence - 0.5) * 0.4
        
        # Bonus diversité sources
        sources = set(entry['source'] for entry in timeline_data)
        if len(sources) > 1:
            confidence += 0.2
            
        return min(confidence, 1.0)
    
    def _calculate_stability_score(self, timeline_data: List[Dict]) -> float:
        """Score stabilité concept à travers le temps"""
        if len(timeline_data) <= 1:
            return 1.0
            
        # Stabilité = faible variance confidence + présence continue
        confidences = [entry['confidence'] for entry in timeline_data]
        variance = sum((c - sum(confidences)/len(confidences))**2 for c in confidences) / len(confidences)
        
        stability = 1.0 - min(variance * 2, 0.5)  # Variance faible = stabilité haute
        
        return stability
    
    def _detect_innovation_markers(self, timeline_data: List[Dict]) -> List[str]:
        """Détecte marqueurs innovation dans évolution concept"""
        markers = []
        
        # Progression confidence
        confidences = [entry['confidence'] for entry in timeline_data]
        if len(confidences) > 1 and confidences[-1] > confidences[0]:
            markers.append("confidence_increase")
            
        # Diversification sources
        sources = [entry['source'] for entry in timeline_data]
        if len(set(sources)) > 1:
            markers.append("multi_source_validation")
            
        # Span temporel large
        periods = [self._period_to_numeric(entry['period']) for entry in timeline_data]
        if max(periods) - min(periods) > 200:
            markers.append("long_term_persistence")
            
        # Présence historique + moderne
        if any("1700-1900" in entry['period'] for entry in timeline_data) and \
           any("2024" in entry['period'] for entry in timeline_data):
            markers.append("historical_modern_bridge")
            
        return markers
    
    def find_innovation_hotspots(self) -> Dict[str, List[str]]:
        """Trouve hotspots innovation par période/source"""
        hotspots = defaultdict(list)
        
        # Groupement par période
        period_concepts = defaultdict(set)
        for concept, timeline_data in self.concept_timeline.items():
            for entry in timeline_data:
                period_concepts[entry['period']].add(concept)
        
        # Détection hotspots
        for period, concepts in period_concepts.items():
            if len(concepts) > 5:  # Seuil hotspot
                hotspots[f"period_{period}"] = list(concepts)[:10]  # Top 10
        
        # Groupement par source
        source_concepts = defaultdict(set)
        for concept, timeline_data in self.concept_timeline.items():
            for entry in timeline_data:
                source_concepts[entry['source']].add(concept)
                
        for source, concepts in source_concepts.items():
            if len(concepts) > 10:  # Seuil hotspot
                hotspots[f"source_{source}"] = list(concepts)[:15]  # Top 15
        
        return dict(hotspots)
    
    def generate_temporal_analysis_report(self) -> Dict:
        """Génère rapport complet analyse temporelle"""
        print("\n⏰ GÉNÉRATION RAPPORT ANALYSE TEMPORELLE")
        print("=" * 45)
        
        # Patterns émergence
        concept_evolutions = self.detect_concept_emergence_patterns()
        
        # Hotspots innovation  
        innovation_hotspots = self.find_innovation_hotspots()
        
        # Métriques temporelles globales
        total_concepts = len(self.concept_timeline)
        multi_period_concepts = len([c for c, t in self.concept_timeline.items() if len(t) > 1])
        
        # Distribution temporelle
        period_distribution = Counter()
        source_distribution = Counter()
        
        for atom in self.temporal_atoms:
            period_distribution[atom['period']] += 1
            source_distribution[atom['source_type']] += 1
        
        report = {
            "analysis_metadata": {
                "total_concepts": total_concepts,
                "multi_period_concepts": multi_period_concepts,
                "total_temporal_atoms": len(self.temporal_atoms),
                "temporal_span": "1700-2024",
                "analysis_date": datetime.datetime.now().isoformat(),
                "analyzer_version": "temporal_emergence_v1.0"
            },
            "concept_evolutions": [
                {
                    "concept": evo.concept,
                    "timeline": evo.timeline,
                    "emergence_confidence": evo.emergence_confidence,
                    "stability_score": evo.stability_score,
                    "innovation_markers": evo.innovation_markers
                }
                for evo in concept_evolutions[:20]  # Top 20
            ],
            "innovation_hotspots": innovation_hotspots,
            "temporal_metrics": {
                "multi_period_rate": multi_period_concepts / total_concepts if total_concepts else 0,
                "avg_emergence_confidence": sum(evo.emergence_confidence for evo in concept_evolutions) / len(concept_evolutions) if concept_evolutions else 0,
                "temporal_diversity": len(set(atom['period'] for atom in self.temporal_atoms))
            },
            "distribution_analysis": {
                "period_distribution": dict(period_distribution),
                "source_distribution": dict(source_distribution)
            }
        }
        
        return report
    
    def save_temporal_analysis(self, filename: str):
        """Sauvegarde analyse temporelle"""
        report = self.generate_temporal_analysis_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Analyse temporelle sauvée: {filename}")
        
        # Affichage résumé
        metadata = report['analysis_metadata']
        print(f"\n⏰ RÉSUMÉ ANALYSE TEMPORELLE:")
        print(f"   • {metadata['total_concepts']} concepts analysés")
        print(f"   • {metadata['multi_period_concepts']} concepts multi-périodes")
        print(f"   • Span temporel: {metadata['temporal_span']}")
        
        metrics = report['temporal_metrics']
        print(f"\n📈 MÉTRIQUES TEMPORELLES:")
        print(f"   • Taux multi-période: {metrics['multi_period_rate']:.3f}")
        print(f"   • Confidence émergence moyenne: {metrics['avg_emergence_confidence']:.3f}")
        print(f"   • Diversité temporelle: {metrics['temporal_diversity']} périodes")
        
        # Top évolutions
        evolutions = report['concept_evolutions']
        if evolutions:
            print(f"\n🌱 TOP ÉVOLUTIONS CONCEPTUELLES:")
            for evo in evolutions[:5]:
                print(f"   • {evo['concept']}: confidence {evo['emergence_confidence']:.3f}, markers {evo['innovation_markers']}")
        
        return report

def main():
    print("⏰ ANALYSEUR ÉMERGENCE TEMPORELLE")
    print("=================================")
    
    analyzer = TemporalEmergenceAnalyzer()
    
    # Chargement stores temporels
    total_loaded = analyzer.load_temporal_stores()
    
    if total_loaded == 0:
        print("❌ Aucune donnée temporelle trouvée")
        return
    
    print(f"\n🔍 Analyse émergence sur {total_loaded} atomes temporels...")
    
    # Génération rapport temporal complet
    analysis_file = "temporal_emergence_analysis.json"
    report = analyzer.save_temporal_analysis(analysis_file)
    
    print(f"\n🎯 ANALYSE TEMPORELLE TERMINÉE")
    print(f"📄 Rapport détaillé: {analysis_file}")
    print(f"🌊 Timeline complète: 1700-2024 (324 ans span)")

if __name__ == "__main__":
    main()
