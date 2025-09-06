#!/usr/bin/env python3
"""
Analyseur de consensus avec détection patterns
"""

import json
from collections import defaultdict
from typing import Dict, List
import re
import sys
import os

# Ajouter le répertoire parent pour imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ConsensusAnalyzer:
    def __init__(self, store_file: str):
        try:
            with open(store_file, 'r', encoding='utf-8') as f:
                self.store = json.load(f)
            self.atoms = self.store['semantic_atoms']
            print(f"📊 Chargé {len(self.atoms)} atomes sémantiques")
        except FileNotFoundError:
            print(f"❌ Fichier {store_file} non trouvé")
            self.store = {"semantic_atoms": []}
            self.atoms = []
        except Exception as e:
            print(f"❌ Erreur chargement: {e}")
            self.atoms = []
        
    def analyze_definition_patterns(self) -> Dict:
        """Détecte patterns dans définitions"""
        patterns = defaultdict(list)
        
        for atom in self.atoms:
            definition = atom['definition'].lower()
            concept = atom['concept']
            
            # Patterns linguistiques IA/informatique
            if any(word in definition for word in ['apprentissage', 'apprendre', 'learning']):
                patterns['learning_based'].append(concept)
            if any(word in definition for word in ['réseau', 'neurone', 'neuronal', 'network']):
                patterns['network_based'].append(concept)
            if any(word in definition for word in ['algorithme', 'algorithm', 'programme']):
                patterns['algorithmic'].append(concept)
            if any(word in definition for word in ['données', 'data', 'information']):
                patterns['data_driven'].append(concept)
            if any(word in definition for word in ['intelligence', 'intelligent', 'artificiel']):
                patterns['ai_related'].append(concept)
            if any(word in definition for word in ['système', 'system', 'informatique']):
                patterns['system_based'].append(concept)
                
        return dict(patterns)
        
    def detect_semantic_clusters(self) -> List[Dict]:
        """Clustering basique par mots-clés communs"""
        clusters = []
        
        if not self.atoms:
            return clusters
        
        # Extraction mots-clés par concept
        concept_keywords = {}
        for atom in self.atoms:
            # Extraction mots significatifs (4+ caractères)
            text = atom['definition'].lower() + " " + atom['context'][:200].lower()
            words = set(re.findall(r'\b\w{4,}\b', text))
            # Filtrer mots vides
            stop_words = {'cette', 'sont', 'pour', 'dans', 'avec', 'être', 'avoir', 'leur', 'leurs', 'elle', 'elles', 'plus', 'très', 'tout', 'tous', 'peut', 'faire', 'autre', 'même', 'aussi', 'bien', 'encore', 'alors', 'ainsi', 'depuis', 'pendant', 'avant', 'après'}
            words = words - stop_words
            concept_keywords[atom['concept']] = words
            
        # Similarité par intersection
        concepts = list(concept_keywords.keys())
        for i, concept1 in enumerate(concepts):
            cluster = {'core_concept': concept1, 'related': [], 'similarity_scores': [], 'shared_keywords': []}
            
            for j, concept2 in enumerate(concepts):
                if i != j:
                    words1 = concept_keywords[concept1]
                    words2 = concept_keywords[concept2]
                    
                    intersection = words1 & words2
                    union = words1 | words2
                    similarity = len(intersection) / len(union) if union else 0
                    
                    if similarity > 0.1:  # Seuil arbitraire
                        cluster['related'].append(concept2)
                        cluster['similarity_scores'].append(round(similarity, 3))
                        cluster['shared_keywords'].append(list(intersection)[:5])  # Top 5 mots communs
                        
            if cluster['related']:
                clusters.append(cluster)
                
        return clusters
        
    def extract_key_concepts(self) -> Dict:
        """Extraction concepts-clés par fréquence"""
        word_freq = defaultdict(int)
        concept_cooccurrence = defaultdict(list)
        
        for atom in self.atoms:
            text = atom['definition'].lower()
            words = re.findall(r'\b\w{5,}\b', text)  # Mots 5+ caractères
            
            for word in words:
                if word not in ['cette', 'sont', 'pour', 'dans', 'avec', 'intelligence', 'artificielle']:
                    word_freq[word] += 1
                    concept_cooccurrence[word].append(atom['concept'])
        
        # Top concepts par fréquence
        top_concepts = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'frequent_terms': top_concepts,
            'cross_concept_terms': {word: list(set(concepts)) for word, concepts in concept_cooccurrence.items() if len(set(concepts)) > 1}
        }
        
    def generate_consensus_report(self) -> Dict:
        """Rapport consensus avec métriques"""
        if not self.atoms:
            return {
                "error": "Aucun atome sémantique à analyser",
                "analysis_metadata": {
                    "total_concepts": 0,
                    "analysis_date": "2024-11-30",
                    "analyzer_version": "0.1.0"
                }
            }
            
        patterns = self.analyze_definition_patterns()
        clusters = self.detect_semantic_clusters()
        key_concepts = self.extract_key_concepts()
        
        # Métriques de diversité
        total_words = sum(len(atom['definition'].split()) for atom in self.atoms)
        avg_definition_length = total_words / len(self.atoms) if self.atoms else 0
        
        # Sources d'extraction
        sources = set(atom['provenance']['source_url'] for atom in self.atoms)
        agents = set(atom['provenance']['source_agent'] for atom in self.atoms)
        
        report = {
            "analysis_metadata": {
                "total_concepts": len(self.atoms),
                "unique_sources": len(sources),
                "unique_agents": len(agents),
                "avg_definition_length": round(avg_definition_length, 1),
                "analysis_date": "2024-11-30",
                "analyzer_version": "0.1.0"
            },
            "semantic_patterns": patterns,
            "concept_clusters": clusters,
            "key_concepts": key_concepts,
            "consensus_metrics": {
                "pattern_coverage": {pattern: len(concepts)/len(self.atoms) 
                                  for pattern, concepts in patterns.items()},
                "cluster_density": len(clusters) / len(self.atoms) if self.atoms else 0,
                "avg_cluster_size": sum(len(c['related']) for c in clusters) / len(clusters) if clusters else 0,
                "conceptual_diversity": len(set(atom['concept'] for atom in self.atoms)) / len(self.atoms) if self.atoms else 0
            },
            "provenance_analysis": {
                "source_distribution": list(sources),
                "agent_distribution": list(agents),
                "temporal_range": {
                    "earliest": min(atom['provenance']['timestamp'] for atom in self.atoms) if self.atoms else None,
                    "latest": max(atom['provenance']['timestamp'] for atom in self.atoms) if self.atoms else None
                }
            }
        }
        
        return report
        
    def save_analysis(self, filename: str):
        """Sauvegarde analyse"""
        report = self.generate_consensus_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Analyse consensus sauvée: {filename}")
        return report
        
    def print_summary(self, report: Dict):
        """Affichage résumé console"""
        print("\n🧠 ANALYSE PATTERNS SÉMANTIQUES")
        print("=" * 40)
        
        metadata = report.get('analysis_metadata', {})
        print(f"📊 Total concepts: {metadata.get('total_concepts', 0)}")
        print(f"🌐 Sources uniques: {metadata.get('unique_sources', 0)}")
        print(f"🤖 Agents uniques: {metadata.get('unique_agents', 0)}")
        print(f"📝 Longueur moy. définition: {metadata.get('avg_definition_length', 0)} mots")
        
        patterns = report.get('semantic_patterns', {})
        if patterns:
            print(f"\n🔍 PATTERNS DÉTECTÉS:")
            for pattern, concepts in patterns.items():
                print(f"  • {pattern}: {', '.join(concepts)}")
        
        clusters = report.get('concept_clusters', [])
        if clusters:
            print(f"\n🔗 CLUSTERS SÉMANTIQUES:")
            for cluster in clusters[:3]:  # Top 3
                core = cluster['core_concept']
                related = cluster['related'][:2]  # Top 2
                similarity = cluster['similarity_scores'][0] if cluster['similarity_scores'] else 0
                print(f"  • {core} → {related} (sim: {similarity:.2f})")
        
        key_concepts = report.get('key_concepts', {})
        frequent = key_concepts.get('frequent_terms', [])
        if frequent:
            print(f"\n🏆 CONCEPTS FRÉQUENTS:")
            for word, freq in frequent[:5]:
                print(f"  • {word}: {freq} occurrences")

def main():
    print("🧠 ANALYSEUR CONSENSUS SÉMANTIQUE")
    print("================================")
    
    store_file = "demo_semantic_store.json"
    if not os.path.exists(store_file):
        print(f"❌ Fichier {store_file} non trouvé")
        print("💡 Lancez d'abord: python collect_with_attribution.py")
        return
    
    analyzer = ConsensusAnalyzer(store_file)
    
    if not analyzer.atoms:
        print("❌ Aucun atome sémantique à analyser")
        return
    
    print(f"🔍 Analyse de {len(analyzer.atoms)} atomes...")
    
    analysis_file = "consensus_analysis.json"
    report = analyzer.save_analysis(analysis_file)
    
    # Affichage résumé
    analyzer.print_summary(report)
    
    print(f"\n🎯 ANALYSE TERMINÉE")
    print(f"📄 Rapport détaillé: {analysis_file}")
    print(f"🔧 Prochaine étape: python traceability_dashboard.py")

if __name__ == "__main__":
    main()
