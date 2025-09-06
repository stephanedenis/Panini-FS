#!/usr/bin/env python3
"""
Collecteur sémantique avec traçabilité complète
Usage: python collect_with_attribution.py --source wikipedia --concept "intelligence artificielle"
"""

import json
import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import hashlib
import sys
import os

# Ajouter le répertoire parent pour imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@dataclass
class Agent:
    id: str
    type: str  # human, machine, collective
    name: str
    version: Optional[str] = None
    bias_profile: Optional[Dict] = None

@dataclass 
class ProvenanceRecord:
    source_agent: str
    timestamp: str
    method: str
    source_url: str
    extraction_confidence: float
    parent_sources: List[str]

@dataclass
class SemanticAtom:
    id: str
    concept: str
    definition: str
    context: str
    provenance: ProvenanceRecord
    
class AttributionCollector:
    def __init__(self, agent_profile: Agent):
        self.agent = agent_profile
        self.atoms = []
        
    def extract_from_wikipedia(self, concept: str) -> List[SemanticAtom]:
        """Extraction Wikipedia avec attribution complète"""
        try:
            import wikipedia
            wikipedia.set_lang("fr")  # Français par défaut
        except ImportError:
            print("⚠️  wikipedia module non installé. Installation...")
            os.system("pip install wikipedia")
            import wikipedia
            wikipedia.set_lang("fr")
        
        # Récupération page
        try:
            print(f"  🔍 Recherche Wikipedia: {concept}")
            page = wikipedia.page(concept)
            content = page.content[:2000]  # Premier paragraphe
            
            # Génération ID unique
            atom_id = hashlib.md5(f"{concept}_{page.url}_{datetime.datetime.now()}".encode()).hexdigest()[:8]
            
            # Extraction première phrase comme définition
            sentences = content.split('.')
            definition = sentences[0] if sentences else content[:200]
            
            # Création atome sémantique
            atom = SemanticAtom(
                id=atom_id,
                concept=concept,
                definition=definition.strip(),
                context=content,
                provenance=ProvenanceRecord(
                    source_agent=self.agent.id,
                    timestamp=datetime.datetime.now().isoformat(),
                    method=f"wikipedia_extraction_{self.agent.version}",
                    source_url=page.url,
                    extraction_confidence=0.85,  # Heuristique
                    parent_sources=[page.url]
                )
            )
            
            self.atoms.append(atom)
            print(f"    ✅ Extrait: {definition[:100]}...")
            return [atom]
            
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"    ⚠️  Ambiguïté pour '{concept}', utilisation première option: {e.options[0]}")
            return self.extract_from_wikipedia(e.options[0])
            
        except wikipedia.exceptions.PageError:
            print(f"    ❌ Page non trouvée pour: {concept}")
            return []
            
        except Exception as e:
            print(f"    ❌ Erreur extraction {concept}: {e}")
            return []
            
    def save_to_store(self, filename: str):
        """Sauvegarde avec métadonnées complètes"""
        store = {
            "collection_metadata": {
                "collector_agent": asdict(self.agent),
                "collection_date": datetime.datetime.now().isoformat(),
                "total_atoms": len(self.atoms),
                "version": "0.1.0"
            },
            "semantic_atoms": [asdict(atom) for atom in self.atoms]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(store, f, indent=2, ensure_ascii=False)
            
        print(f"✅ {len(self.atoms)} atomes sauvés dans {filename}")

def main():
    print("🚀 COLLECTEUR SÉMANTIQUE AVEC TRAÇABILITÉ")
    print("=========================================")
    
    # Configuration agent collecteur
    agent = Agent(
        id="autonomous_copilot_v1",
        type="machine", 
        name="PaniniFS Autonomous Copilot",
        version="1.0.0",
        bias_profile={
            "source": "wikipedia_fr", 
            "language": "french", 
            "cultural_context": "western",
            "extraction_method": "first_sentence_heuristic"
        }
    )
    
    print(f"🤖 Agent configuré: {agent.name} v{agent.version}")
    
    # Collecte concepts test
    collector = AttributionCollector(agent)
    
    concepts = [
        "intelligence artificielle",
        "machine learning", 
        "réseaux de neurones",
        "apprentissage profond",
        "transformers",
        "blockchain",
        "algorithme"
    ]
    
    print(f"\n📊 Collecte de {len(concepts)} concepts:")
    for i, concept in enumerate(concepts, 1):
        print(f"[{i}/{len(concepts)}] {concept}")
        collector.extract_from_wikipedia(concept)
    
    # Sauvegarde avec traçabilité
    store_file = "demo_semantic_store.json"
    collector.save_to_store(store_file)
    
    print(f"\n🎯 COLLECTE TERMINÉE")
    print(f"✨ {len(collector.atoms)} atomes sémantiques tracés")
    print(f"📄 Données sauvées: {store_file}")
    print(f"🔍 Chaque atome contient: concept, définition, contexte, provenance complète")
    
    # Affichage exemple
    if collector.atoms:
        example = collector.atoms[0]
        print(f"\n📋 EXEMPLE D'ATOME SÉMANTIQUE:")
        print(f"   ID: {example.id}")
        print(f"   Concept: {example.concept}")
        print(f"   Définition: {example.definition[:100]}...")
        print(f"   Agent: {example.provenance.source_agent}")
        print(f"   Timestamp: {example.provenance.timestamp}")
        print(f"   Source: {example.provenance.source_url}")
        print(f"   Confiance: {example.provenance.extraction_confidence}")

if __name__ == "__main__":
    main()
