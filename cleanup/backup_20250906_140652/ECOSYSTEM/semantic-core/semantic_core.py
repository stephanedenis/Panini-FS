#!/usr/bin/env python3
"""
🧠 PANINI SEMANTIC CORE
Primitives sémantiques universelles pour l'IA moderne

GitHub: https://github.com/stephanedenis/PaniniFS-SemanticCore
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import time

class UniversalSemanticProcessor:
    """
    Processeur sémantique universel basé sur les primitives découvertes
    """
    
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.semantic_cache = {}
        self.universal_patterns = {}
        
    def extract_semantic_primitives(self, texts: List[str]) -> Dict[str, Any]:
        """
        Extraction des primitives sémantiques universelles
        
        Returns:
            Dict avec embeddings, clusters, patterns universels
        """
        
        # Génération embeddings
        embeddings = self.model.encode(texts)
        
        # Détection patterns universels
        patterns = self._detect_universal_patterns(embeddings, texts)
        
        # Clustering sémantique
        clusters = self._semantic_clustering(embeddings, texts)
        
        return {
            'embeddings': embeddings,
            'patterns': patterns,
            'clusters': clusters,
            'universality_score': self._calculate_universality(patterns),
            'metadata': {
                'model': self.model,
                'texts_count': len(texts),
                'processing_time': time.time()
            }
        }
    
    def _detect_universal_patterns(self, embeddings: np.ndarray, texts: List[str]) -> Dict:
        """Détection des patterns universellement applicables"""
        
        # Calcul similarités
        similarities = cosine_similarity(embeddings)
        
        # Identification concepts publics vs privés
        public_concepts = []
        private_concepts = []
        
        for i, text in enumerate(texts):
            avg_similarity = np.mean(similarities[i])
            
            if avg_similarity > 0.7:  # Très similaire = concept universel
                public_concepts.append({
                    'text': text,
                    'embedding': embeddings[i],
                    'universality': avg_similarity
                })
            else:  # Spécifique = concept privé
                private_concepts.append({
                    'text': text,
                    'embedding': embeddings[i],
                    'specificity': 1 - avg_similarity
                })
        
        return {
            'public_concepts': public_concepts,
            'private_concepts': private_concepts,
            'public_ratio': len(public_concepts) / len(texts)
        }
    
    def _semantic_clustering(self, embeddings: np.ndarray, texts: List[str]) -> Dict:
        """Clustering sémantique intelligent"""
        from sklearn.cluster import DBSCAN
        
        # Clustering DBSCAN pour densité variable
        clustering = DBSCAN(eps=0.3, min_samples=2, metric='cosine')
        cluster_labels = clustering.fit_predict(embeddings)
        
        # Organisation par clusters
        clusters = {}
        for i, label in enumerate(cluster_labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append({
                'text': texts[i],
                'embedding': embeddings[i],
                'index': i
            })
        
        return clusters
    
    def _calculate_universality(self, patterns: Dict) -> float:
        """Score d'universalité des patterns détectés"""
        return patterns['public_ratio']
    
    def quick_semantic_search(self, query: str, corpus: List[str], top_k: int = 5) -> List[Dict]:
        """
        Recherche sémantique rapide optimisée
        """
        
        # Embedding requête
        query_embedding = self.model.encode([query])
        
        # Embeddings corpus (avec cache)
        corpus_key = str(hash(str(corpus)))
        if corpus_key in self.semantic_cache:
            corpus_embeddings = self.semantic_cache[corpus_key]
        else:
            corpus_embeddings = self.model.encode(corpus)
            self.semantic_cache[corpus_key] = corpus_embeddings
        
        # Calcul similarités
        similarities = cosine_similarity(query_embedding, corpus_embeddings)[0]
        
        # Top-K résultats
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                'text': corpus[idx],
                'similarity': similarities[idx],
                'index': idx,
                'universality': self._estimate_concept_universality(corpus[idx])
            })
        
        return results
    
    def _estimate_concept_universality(self, text: str) -> float:
        """Estimation rapide universalité d'un concept"""
        
        # Heuristiques basées sur la découverte des primitives
        universal_indicators = [
            'search', 'find', 'process', 'analyze', 'optimize',
            'create', 'generate', 'transform', 'validate', 'execute'
        ]
        
        score = 0
        for indicator in universal_indicators:
            if indicator.lower() in text.lower():
                score += 0.1
        
        return min(score, 1.0)

# 🧪 DEMO SYSTÈME
def demo_semantic_core():
    print("🧠 DEMO SEMANTIC CORE")
    print("=" * 50)
    
    processor = UniversalSemanticProcessor()
    
    # Corpus test
    texts = [
        "semantic search in documents",
        "find relevant information quickly", 
        "process natural language efficiently",
        "my private database credentials",
        "internal company meeting notes",
        "optimize machine learning models"
    ]
    
    # Extraction primitives
    print("\n🔍 Extraction Primitives Sémantiques...")
    primitives = processor.extract_semantic_primitives(texts)
    
    print(f"✅ Concepts publics: {len(primitives['patterns']['public_concepts'])}")
    print(f"✅ Concepts privés: {len(primitives['patterns']['private_concepts'])}")
    print(f"✅ Score universalité: {primitives['universality_score']:.2f}")
    
    # Recherche sémantique
    print("\n🔎 Recherche Sémantique...")
    query = "search for information"
    results = processor.quick_semantic_search(query, texts, top_k=3)
    
    for i, result in enumerate(results):
        print(f"{i+1}. {result['text']} (sim: {result['similarity']:.3f}, univ: {result['universality']:.2f})")
    
    print("\n🏁 Demo completed!")

if __name__ == "__main__":
    demo_semantic_core()
