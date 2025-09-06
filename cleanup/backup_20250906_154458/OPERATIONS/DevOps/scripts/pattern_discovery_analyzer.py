#!/usr/bin/env python3
"""
Analyseur patterns sémantiques - Découverte autonome
"""

import json
import os
from collections import Counter, defaultdict
from typing import Dict, List, Set
import datetime

class PatternDiscovery:
    def __init__(self):
        self.concept_patterns = defaultdict(list)
        self.semantic_clusters = {}
        
    def load_all_sources(self):
        """Charge toutes sources pour analyse patterns"""
        sources = [
            "demo_semantic_store.json",
            "arxiv_semantic_store.json", 
            "historical_books_semantic_store.json",
            "news_semantic_store.json"
        ]
        
        all_atoms = []
        for source_file in sources:
            if os.path.exists(source_file):
                with open(source_file, 'r') as f:
                    store = json.load(f)
                    atoms = store.get('semantic_atoms', [])
                    all_atoms.extend(atoms)
        
        return all_atoms
    
    def discover_semantic_patterns(self, atoms: List[Dict]) -> Dict:
        """Découverte patterns sémantiques"""
        patterns = {
            "keyword_clusters": self.cluster_by_keywords(atoms),
            "definition_similarities": self.find_definition_patterns(atoms),
            "temporal_patterns": self.analyze_temporal_patterns(atoms),
            "source_specializations": self.analyze_source_patterns(atoms)
        }
        
        return patterns
    
    def cluster_by_keywords(self, atoms: List[Dict]) -> Dict:
        """Clustering par mots-clés"""
        keyword_groups = defaultdict(list)
        
        for atom in atoms:
            concept = atom['concept'].lower()
            definition = atom['definition'].lower()
            
            # Détection mots-clés techniques
            if any(word in concept + definition for word in ['learning', 'neural', 'ai', 'algorithm']):
                keyword_groups['artificial_intelligence'].append(atom['concept'])
            elif any(word in concept + definition for word in ['quantum', 'computing', 'processor']):
                keyword_groups['computing_systems'].append(atom['concept'])
            elif any(word in concept + definition for word in ['data', 'information', 'knowledge']):
                keyword_groups['information_systems'].append(atom['concept'])
            else:
                keyword_groups['general_concepts'].append(atom['concept'])
        
        return dict(keyword_groups)
    
    def find_definition_patterns(self, atoms: List[Dict]) -> List[Dict]:
        """Patterns dans définitions"""
        patterns = []
        
        # Analyse longueur définitions
        def_lengths = [len(atom['definition']) for atom in atoms]
        avg_length = sum(def_lengths) / len(def_lengths)
        
        patterns.append({
            "pattern_type": "definition_length",
            "average_length": avg_length,
            "short_definitions": len([l for l in def_lengths if l < avg_length * 0.7]),
            "long_definitions": len([l for l in def_lengths if l > avg_length * 1.3])
        })
        
        return patterns
    
    def analyze_temporal_patterns(self, atoms: List[Dict]) -> Dict:
        """Patterns temporels"""
        timestamps = [atom['provenance']['timestamp'][:10] for atom in atoms]
        daily_counts = Counter(timestamps)
        
        return {
            "collection_by_day": dict(daily_counts),
            "most_productive_day": daily_counts.most_common(1)[0] if daily_counts else None,
            "collection_consistency": len(set(timestamps))
        }
    
    def analyze_source_patterns(self, atoms: List[Dict]) -> Dict:
        """Patterns par source"""
        source_stats = defaultdict(lambda: {"count": 0, "avg_confidence": 0})
        
        for atom in atoms:
            source = atom.get('source_type', 'unknown')
            confidence = atom['provenance']['extraction_confidence']
            
            source_stats[source]["count"] += 1
            source_stats[source]["avg_confidence"] += confidence
        
        # Calcul moyennes
        for source, stats in source_stats.items():
            if stats["count"] > 0:
                stats["avg_confidence"] /= stats["count"]
        
        return dict(source_stats)
    
    def generate_pattern_report(self) -> Dict:
        """Génère rapport patterns complet"""
        atoms = self.load_all_sources()
        
        if not atoms:
            return {"error": "No data sources found"}
        
        patterns = self.discover_semantic_patterns(atoms)
        
        report = {
            "analysis_metadata": {
                "total_atoms_analyzed": len(atoms),
                "analysis_date": datetime.datetime.now().isoformat(),
                "pattern_discovery_version": "1.0"
            },
            "discovered_patterns": patterns,
            "insights": {
                "largest_cluster": max(patterns["keyword_clusters"].items(), key=lambda x: len(x[1])),
                "source_diversity": len(patterns["source_specializations"]),
                "temporal_span": len(patterns["temporal_patterns"]["collection_by_day"])
            }
        }
        
        with open("pattern_discovery_report.json", 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"🔍 Rapport patterns sauvé: {len(patterns)} types patterns découverts")
        return report

if __name__ == "__main__":
    discovery = PatternDiscovery()
    discovery.generate_pattern_report()
