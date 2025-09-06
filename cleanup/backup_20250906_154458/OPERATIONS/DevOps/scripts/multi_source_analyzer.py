#!/usr/bin/env python3
"""
Analyseur multi-sources pour consensus avancé Wikipedia + arXiv
Détecte convergences, divergences et émergences conceptuelles
"""

import json
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple
import sys
import os
import datetime
from dataclasses import dataclass

# Import structures communes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

@dataclass
class ConceptConsensus:
    concept: str
    sources: List[str]  # wikipedia, arxiv
    definitions: List[str]
    agents: List[str]
    confidence_scores: List[float]
    temporal_range: Tuple[str, str]
    consensus_score: float
    divergence_factors: List[str]

class MultiSourceConsensusAnalyzer:
    def __init__(self):
        self.stores = {}
        self.all_atoms = []
        self.concept_index = defaultdict(list)
        
    def load_store(self, filename: str, source_type: str):
        """Charge un store sémantique (Wikipedia, arXiv, etc.)"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                store = json.load(f)
                
            self.stores[source_type] = store
            atoms = store.get('semantic_atoms', [])
            
            # Index par concept
            for atom in atoms:
                atom['source_type'] = source_type  # Tag source
                self.all_atoms.append(atom)
                concept = atom['concept'].lower().strip()
                self.concept_index[concept].append(atom)
                
            print(f"📊 {source_type}: {len(atoms)} atomes chargés")
            return len(atoms)
            
        except FileNotFoundError:
            print(f"⚠️  {filename} non trouvé")
            return 0
        except Exception as e:
            print(f"❌ Erreur chargement {filename}: {e}")
            return 0
    
    def find_cross_source_concepts(self, min_sources: int = 2) -> List[str]:
        """Trouve concepts présents dans multiple sources"""
        cross_source = []
        
        for concept, atoms in self.concept_index.items():
            sources = set(atom['source_type'] for atom in atoms)
            if len(sources) >= min_sources:
                cross_source.append(concept)
                
        print(f"🔗 {len(cross_source)} concepts multi-sources identifiés")
        return sorted(cross_source)
    
    def analyze_concept_consensus(self, concept: str) -> ConceptConsensus:
        """Analyse consensus détaillé pour un concept"""
        atoms = self.concept_index.get(concept.lower(), [])
        
        if not atoms:
            return None
            
        # Extraction métadonnées
        sources = list(set(atom['source_type'] for atom in atoms))
        definitions = [atom['definition'] for atom in atoms]
        agents = list(set(atom['provenance']['source_agent'] for atom in atoms))
        confidence_scores = [atom['provenance']['extraction_confidence'] for atom in atoms]
        
        # Range temporel
        timestamps = [atom['provenance']['timestamp'] for atom in atoms]
        temporal_range = (min(timestamps), max(timestamps))
        
        # Calcul score consensus
        consensus_score = self._calculate_consensus_score(atoms)
        
        # Facteurs divergence
        divergence_factors = self._identify_divergence_factors(atoms)
        
        return ConceptConsensus(
            concept=concept,
            sources=sources,
            definitions=definitions,
            agents=agents,
            confidence_scores=confidence_scores,
            temporal_range=temporal_range,
            consensus_score=consensus_score,
            divergence_factors=divergence_factors
        )
    
    def _calculate_consensus_score(self, atoms: List[Dict]) -> float:
        """Calcule score consensus basé sur multiple facteurs"""
        if len(atoms) <= 1:
            return 0.5
            
        # Facteur 1: Concordance définitions (similarité mots-clés)
        definition_similarity = self._calculate_definition_similarity(atoms)
        
        # Facteur 2: Confidence moyenne sources
        avg_confidence = sum(atom['provenance']['extraction_confidence'] for atom in atoms) / len(atoms)
        
        # Facteur 3: Diversité sources (bonus si multiple sources)
        source_diversity = len(set(atom['source_type'] for atom in atoms)) / len(self.stores)
        
        # Facteur 4: Stabilité temporelle (bonus si extractions étalées)
        temporal_stability = self._calculate_temporal_stability(atoms)
        
        # Score composite
        consensus = (
            definition_similarity * 0.4 +
            avg_confidence * 0.3 +
            source_diversity * 0.2 +
            temporal_stability * 0.1
        )
        
        return round(consensus, 3)
    
    def _calculate_definition_similarity(self, atoms: List[Dict]) -> float:
        """Calcule similarité entre définitions"""
        if len(atoms) <= 1:
            return 1.0
            
        definitions = [atom['definition'].lower() for atom in atoms]
        
        # Extraction mots-clés communs
        all_words = []
        for definition in definitions:
            words = set(word for word in definition.split() if len(word) > 3)
            all_words.append(words)
        
        if not all_words:
            return 0.0
            
        # Intersection / Union moyenne
        similarities = []
        for i in range(len(all_words)):
            for j in range(i + 1, len(all_words)):
                intersection = all_words[i] & all_words[j]
                union = all_words[i] | all_words[j]
                similarity = len(intersection) / len(union) if union else 0
                similarities.append(similarity)
        
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def _calculate_temporal_stability(self, atoms: List[Dict]) -> float:
        """Calcule stabilité temporelle (spread = bon)"""
        if len(atoms) <= 1:
            return 1.0
            
        timestamps = [atom['provenance']['timestamp'] for atom in atoms]
        # Simple heuristique: plus c'est étalé, plus c'est stable
        unique_times = len(set(ts[:10] for ts in timestamps))  # Date uniqueness
        return min(unique_times / len(atoms), 1.0)
    
    def _identify_divergence_factors(self, atoms: List[Dict]) -> List[str]:
        """Identifie facteurs de divergence"""
        factors = []
        
        # Sources différentes
        sources = set(atom['source_type'] for atom in atoms)
        if len(sources) > 1:
            factors.append(f"multi_source_{len(sources)}")
            
        # Agents différents  
        agents = set(atom['provenance']['source_agent'] for atom in atoms)
        if len(agents) > 1:
            factors.append(f"multi_agent_{len(agents)}")
            
        # Confidence variance
        confidences = [atom['provenance']['extraction_confidence'] for atom in atoms]
        if max(confidences) - min(confidences) > 0.2:
            factors.append("confidence_variance")
            
        # Longueur définitions très différente
        def_lengths = [len(atom['definition']) for atom in atoms]
        if max(def_lengths) > 2 * min(def_lengths):
            factors.append("definition_length_variance")
            
        return factors
    
    def detect_emergent_concepts(self, confidence_threshold: float = 0.8) -> List[str]:
        """Détecte concepts émergents (haute confidence, source unique)"""
        emergent = []
        
        for concept, atoms in self.concept_index.items():
            if len(atoms) == 1:  # Source unique
                atom = atoms[0]
                confidence = atom['provenance']['extraction_confidence']
                
                if confidence >= confidence_threshold:
                    emergent.append(concept)
                    
        print(f"🌱 {len(emergent)} concepts émergents détectés")
        return sorted(emergent)
    
    def find_concept_clusters(self, similarity_threshold: float = 0.3) -> List[List[str]]:
        """Trouve clusters de concepts similaires"""
        concepts = list(self.concept_index.keys())
        clusters = []
        processed = set()
        
        for concept in concepts:
            if concept in processed:
                continue
                
            cluster = [concept]
            processed.add(concept)
            
            # Cherche concepts similaires
            for other_concept in concepts:
                if other_concept != concept and other_concept not in processed:
                    similarity = self._concept_similarity(concept, other_concept)
                    if similarity >= similarity_threshold:
                        cluster.append(other_concept)
                        processed.add(other_concept)
            
            if len(cluster) > 1:
                clusters.append(cluster)
                
        print(f"🔗 {len(clusters)} clusters conceptuels identifiés")
        return clusters
    
    def _concept_similarity(self, concept1: str, concept2: str) -> float:
        """Calcule similarité entre deux concepts"""
        atoms1 = self.concept_index.get(concept1, [])
        atoms2 = self.concept_index.get(concept2, [])
        
        if not atoms1 or not atoms2:
            return 0.0
            
        # Similarité basée sur contextes/définitions
        contexts1 = " ".join(atom['definition'] + " " + atom.get('context', '') for atom in atoms1)
        contexts2 = " ".join(atom['definition'] + " " + atom.get('context', '') for atom in atoms2)
        
        words1 = set(contexts1.lower().split())
        words2 = set(contexts2.lower().split())
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union) if union else 0.0
    
    def generate_comprehensive_report(self) -> Dict:
        """Génère rapport complet multi-sources"""
        print("\n🧠 GÉNÉRATION RAPPORT CONSENSUS MULTI-SOURCES")
        print("=" * 50)
        
        # Concepts cross-source
        cross_source_concepts = self.find_cross_source_concepts()
        
        # Analyse consensus top concepts
        consensus_analyses = []
        for concept in cross_source_concepts[:20]:  # Top 20
            consensus = self.analyze_concept_consensus(concept)
            if consensus:
                consensus_analyses.append({
                    'concept': consensus.concept,
                    'sources': consensus.sources,
                    'consensus_score': consensus.consensus_score,
                    'agents_count': len(consensus.agents),
                    'definitions_count': len(consensus.definitions),
                    'divergence_factors': consensus.divergence_factors
                })
        
        # Concepts émergents
        emergent_concepts = self.detect_emergent_concepts()
        
        # Clusters conceptuels
        concept_clusters = self.find_concept_clusters()
        
        # Métriques globales
        total_concepts = len(self.concept_index)
        total_atoms = len(self.all_atoms)
        source_coverage = {source: len([a for a in self.all_atoms if a['source_type'] == source]) 
                          for source in self.stores.keys()}
        
        report = {
            "analysis_metadata": {
                "total_concepts": total_concepts,
                "total_atoms": total_atoms,
                "sources_analyzed": list(self.stores.keys()),
                "cross_source_concepts": len(cross_source_concepts),
                "emergent_concepts": len(emergent_concepts),
                "concept_clusters": len(concept_clusters),
                "analysis_date": datetime.datetime.now().isoformat(),
                "analyzer_version": "multi_source_v1.0"
            },
            "source_coverage": source_coverage,
            "cross_source_analysis": {
                "concepts": cross_source_concepts[:50],  # Top 50
                "consensus_scores": consensus_analyses
            },
            "emergent_concepts": emergent_concepts[:30],  # Top 30
            "concept_clusters": concept_clusters[:20],   # Top 20
            "consensus_metrics": {
                "avg_cross_source_consensus": sum(c['consensus_score'] for c in consensus_analyses) / len(consensus_analyses) if consensus_analyses else 0,
                "source_agreement_rate": len(cross_source_concepts) / total_concepts if total_concepts else 0,
                "emergence_rate": len(emergent_concepts) / total_concepts if total_concepts else 0
            }
        }
        
        return report
    
    def save_analysis(self, filename: str):
        """Sauvegarde analyse multi-sources"""
        report = self.generate_comprehensive_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Analyse multi-sources sauvée: {filename}")
        
        # Affichage résumé
        metadata = report['analysis_metadata']
        print(f"\n📊 RÉSUMÉ CONSENSUS MULTI-SOURCES:")
        print(f"   • {metadata['total_concepts']} concepts uniques")
        print(f"   • {metadata['total_atoms']} atomes sémantiques")
        print(f"   • {metadata['cross_source_concepts']} concepts multi-sources")
        print(f"   • {metadata['emergent_concepts']} concepts émergents")
        print(f"   • {metadata['concept_clusters']} clusters détectés")
        
        consensus_metrics = report['consensus_metrics']
        print(f"\n🎯 MÉTRIQUES CONSENSUS:")
        print(f"   • Score consensus moyen: {consensus_metrics['avg_cross_source_consensus']:.3f}")
        print(f"   • Taux accord sources: {consensus_metrics['source_agreement_rate']:.3f}")
        print(f"   • Taux émergence: {consensus_metrics['emergence_rate']:.3f}")
        
        return report

def main():
    print("🧠 ANALYSEUR CONSENSUS MULTI-SOURCES")
    print("====================================")
    
    analyzer = MultiSourceConsensusAnalyzer()
    
    # Chargement stores disponibles
    stores_to_load = [
        ("demo_semantic_store.json", "wikipedia"),
        ("arxiv_semantic_store.json", "arxiv")
    ]
    
    total_loaded = 0
    for filename, source_type in stores_to_load:
        if os.path.exists(filename):
            loaded = analyzer.load_store(filename, source_type)
            total_loaded += loaded
        else:
            print(f"⚠️  {filename} non trouvé - ignoré")
    
    if total_loaded == 0:
        print("❌ Aucun store sémantique trouvé")
        print("💡 Lancez d'abord:")
        print("   python collect_with_attribution.py")
        print("   python arxiv_collector.py")
        return
    
    print(f"\n🔍 Analyse consensus sur {total_loaded} atomes...")
    
    # Génération rapport complet
    analysis_file = "multi_source_consensus_analysis.json"
    report = analyzer.save_analysis(analysis_file)
    
    print(f"\n🎯 ANALYSE TERMINÉE")
    print(f"📄 Rapport détaillé: {analysis_file}")
    print(f"🌐 Mise à jour dashboard recommandée")

if __name__ == "__main__":
    main()
