#!/usr/bin/env python3
"""
Collecteur arXiv avec traçabilité complète pour recherche sémantique avancée
Usage: python arxiv_collector.py --domain "machine learning" --max-papers 50
"""

import json
import datetime
import hashlib
import sys
import os
import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re

# Import structures communes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from collect_with_attribution import Agent, ProvenanceRecord, SemanticAtom

@dataclass
class ArXivPaper:
    id: str
    title: str
    authors: List[str]
    abstract: str
    published: str
    categories: List[str]
    url: str

class ArXivCollector:
    def __init__(self, agent_profile: Agent):
        self.agent = agent_profile
        self.atoms = []
        self.base_url = "http://export.arxiv.org/api/query"
        
    def search_papers(self, query: str, max_results: int = 50) -> List[ArXivPaper]:
        """Recherche papers arXiv avec query semantique"""
        print(f"🔍 Recherche arXiv: '{query}' (max {max_results} papers)")
        
        # Construction requête arXiv API
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        url = f"{self.base_url}?{urllib.parse.urlencode(params)}"
        
        try:
            with urllib.request.urlopen(url) as response:
                xml_content = response.read()
                
            # Parse XML response
            root = ET.fromstring(xml_content)
            papers = []
            
            # Namespace arXiv
            ns = {'atom': 'http://www.w3.org/2005/Atom',
                  'arxiv': 'http://arxiv.org/schemas/atom'}
            
            for entry in root.findall('atom:entry', ns):
                paper = self._parse_paper_entry(entry, ns)
                if paper:
                    papers.append(paper)
                    
            print(f"  ✅ {len(papers)} papers récupérés")
            return papers
            
        except Exception as e:
            print(f"  ❌ Erreur API arXiv: {e}")
            return []
    
    def _parse_paper_entry(self, entry, ns) -> Optional[ArXivPaper]:
        """Parse une entrée XML arXiv en structure Paper"""
        try:
            # ID (nettoyer URL)
            id_elem = entry.find('atom:id', ns)
            paper_id = id_elem.text.split('/')[-1] if id_elem is not None else "unknown"
            
            # Titre
            title_elem = entry.find('atom:title', ns)
            title = title_elem.text.strip().replace('\n', ' ') if title_elem is not None else "No title"
            
            # Abstract  
            summary_elem = entry.find('atom:summary', ns)
            abstract = summary_elem.text.strip().replace('\n', ' ') if summary_elem is not None else ""
            
            # Auteurs
            authors = []
            for author in entry.findall('atom:author', ns):
                name_elem = author.find('atom:name', ns)
                if name_elem is not None:
                    authors.append(name_elem.text)
            
            # Date publication
            published_elem = entry.find('atom:published', ns)
            published = published_elem.text if published_elem is not None else ""
            
            # Catégories
            categories = []
            for category in entry.findall('atom:category', ns):
                term = category.get('term')
                if term:
                    categories.append(term)
            
            # URL
            url = f"https://arxiv.org/abs/{paper_id}"
            
            return ArXivPaper(
                id=paper_id,
                title=title,
                authors=authors,
                abstract=abstract,
                published=published,
                categories=categories,
                url=url
            )
            
        except Exception as e:
            print(f"    ⚠️  Erreur parsing paper: {e}")
            return None
    
    def extract_concepts_from_papers(self, papers: List[ArXivPaper], domain: str) -> List[SemanticAtom]:
        """Extraction concepts sémantiques depuis papers arXiv"""
        print(f"🧠 Extraction concepts depuis {len(papers)} papers...")
        
        extracted_atoms = []
        
        for i, paper in enumerate(papers, 1):
            print(f"  [{i}/{len(papers)}] {paper.title[:50]}...")
            
            # Extraction concepts depuis titre + abstract
            concepts = self._extract_concepts_from_text(paper.title + ". " + paper.abstract)
            
            for concept in concepts:
                # Génération ID unique
                atom_id = hashlib.md5(f"{concept}_{paper.id}_{datetime.datetime.now()}".encode()).hexdigest()[:8]
                
                # Contexte enrichi avec métadonnées paper
                context = f"Paper: {paper.title}\nAuthors: {', '.join(paper.authors[:3])}\nCategories: {', '.join(paper.categories)}\nAbstract: {paper.abstract[:500]}..."
                
                # Création atome sémantique
                atom = SemanticAtom(
                    id=atom_id,
                    concept=concept,
                    definition=self._extract_definition(concept, paper.abstract),
                    context=context,
                    provenance=ProvenanceRecord(
                        source_agent=self.agent.id,
                        timestamp=datetime.datetime.now().isoformat(),
                        method=f"arxiv_extraction_{self.agent.version}",
                        source_url=paper.url,
                        extraction_confidence=self._calculate_confidence(concept, paper),
                        parent_sources=[paper.url]
                    )
                )
                
                extracted_atoms.append(atom)
                
            # Rate limiting pour être gentil avec arXiv
            time.sleep(0.1)
        
        self.atoms.extend(extracted_atoms)
        print(f"  ✅ {len(extracted_atoms)} concepts extraits")
        return extracted_atoms
    
    def _extract_concepts_from_text(self, text: str) -> List[str]:
        """Extraction heuristique concepts depuis texte"""
        # Patterns pour concepts techniques
        patterns = [
            r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b',  # "Deep Learning", "Machine Learning"
            r'\b([a-z]+-[a-z]+)\b',            # "self-attention", "cross-validation"  
            r'\b([A-Z]{2,})\b',                # "GAN", "CNN", "RNN"
            r'\b([a-z]+ing)\b',                # "learning", "training", "clustering"
            r'\b([a-z]+tion)\b',               # "classification", "optimization"
        ]
        
        concepts = set()
        text_lower = text.lower()
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) > 3 and match.lower() not in ['the', 'and', 'for', 'with', 'that', 'this']:
                    concepts.add(match.lower())
        
        # Filtrage concepts pertinents (longueur, mots vides)
        filtered = [c for c in concepts if len(c) >= 4 and c not in {'using', 'based', 'paper', 'show', 'method', 'approach', 'results'}]
        
        return list(filtered)[:10]  # Top 10 concepts par paper
    
    def _extract_definition(self, concept: str, abstract: str) -> str:
        """Extraction définition contextuelle du concept"""
        # Cherche phrases contenant le concept
        sentences = abstract.split('.')
        for sentence in sentences:
            if concept.lower() in sentence.lower():
                return sentence.strip()
        
        # Fallback: première phrase abstract
        return sentences[0].strip() if sentences else f"Concept: {concept}"
    
    def _calculate_confidence(self, concept: str, paper: ArXivPaper) -> float:
        """Calcul score confiance extraction"""
        confidence = 0.7  # Base
        
        # Bonus si concept dans titre
        if concept.lower() in paper.title.lower():
            confidence += 0.2
            
        # Bonus si catégories pertinentes
        relevant_cats = ['cs.LG', 'cs.AI', 'cs.CL', 'cs.CV', 'stat.ML']
        if any(cat in paper.categories for cat in relevant_cats):
            confidence += 0.1
            
        # Bonus si auteurs multiples (collaboration)
        if len(paper.authors) > 2:
            confidence += 0.05
            
        return min(confidence, 0.95)  # Max 95%
    
    def save_enhanced_store(self, filename: str, domain: str, papers_metadata: List[ArXivPaper]):
        """Sauvegarde avec métadonnées arXiv enrichies"""
        store = {
            "collection_metadata": {
                "collector_agent": asdict(self.agent),
                "collection_date": datetime.datetime.now().isoformat(),
                "total_atoms": len(self.atoms),
                "source_domain": domain,
                "source_type": "arxiv_papers",
                "papers_count": len(papers_metadata),
                "version": "0.2.0"
            },
            "source_papers": [asdict(paper) for paper in papers_metadata],
            "semantic_atoms": [asdict(atom) for atom in self.atoms]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(store, f, indent=2, ensure_ascii=False)
            
        print(f"✅ {len(self.atoms)} atomes + {len(papers_metadata)} papers sauvés dans {filename}")

def main():
    print("🚀 COLLECTEUR ARXIV AVEC TRAÇABILITÉ")
    print("===================================")
    
    # Configuration agent collecteur arXiv
    agent = Agent(
        id="arxiv_collector_v1",
        type="machine", 
        name="PaniniFS arXiv Semantic Collector",
        version="1.0.0",
        bias_profile={
            "source": "arxiv_papers", 
            "language": "english", 
            "cultural_context": "academic_scientific",
            "extraction_method": "heuristic_nlp_patterns",
            "domain_focus": "computer_science_ai"
        }
    )
    
    print(f"🤖 Agent configuré: {agent.name} v{agent.version}")
    
    # Domaines de recherche
    research_domains = [
        "machine learning",
        "deep learning", 
        "neural networks",
        "natural language processing",
        "computer vision",
        "reinforcement learning"
    ]
    
    collector = ArXivCollector(agent)
    all_papers = []
    
    print(f"\n📊 Collecte sur {len(research_domains)} domaines:")
    
    for i, domain in enumerate(research_domains, 1):
        print(f"\n[{i}/{len(research_domains)}] Domaine: {domain}")
        
        # Recherche papers pour ce domaine
        papers = collector.search_papers(domain, max_results=20)  # 20 papers/domaine
        all_papers.extend(papers)
        
        # Extraction concepts
        if papers:
            collector.extract_concepts_from_papers(papers, domain)
        
        # Rate limiting entre domaines
        time.sleep(1)
    
    # Sauvegarde avec métadonnées complètes
    store_file = "arxiv_semantic_store.json"
    collector.save_enhanced_store(store_file, "ai_computer_science", all_papers)
    
    print(f"\n🎯 COLLECTE ARXIV TERMINÉE")
    print(f"✨ {len(collector.atoms)} concepts sémantiques extraits")
    print(f"📄 {len(all_papers)} papers académiques analysés") 
    print(f"💾 Données: {store_file}")
    print(f"🔍 Prochaine étape: Analyse consensus multi-sources")

if __name__ == "__main__":
    main()
