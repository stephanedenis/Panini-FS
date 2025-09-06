#!/usr/bin/env python3
"""
Collecteur Livres avec traçabilité complète - Project Gutenberg + Archive.org
Focus: Concepts historiques, évolution temporelle, consensus littéraire
"""

import json
import datetime
import hashlib
import time
import urllib.request
import urllib.parse
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import os
import sys

# Import structures communes
sys.path.append('/home/stephane/GitHub/PaniniFS-1/scripts/scripts')
from collect_with_attribution import Agent, ProvenanceRecord, SemanticAtom

@dataclass
class BookMetadata:
    id: str
    title: str
    author: str
    year: str
    language: str
    subject: List[str]
    url: str
    text_sample: str  # Premier chapitre/excerpt

class BooksCollector:
    def __init__(self, agent_profile: Agent):
        self.agent = agent_profile
        self.atoms = []
        
        # Sources livres gratuites
        self.gutenberg_api = "https://www.gutenberg.org/ebooks/search/"
        self.archive_api = "https://archive.org/advancedsearch.php"
        
    def search_philosophy_books(self, max_books: int = 30) -> List[BookMetadata]:
        """Recherche livres philosophie/sciences pour concepts historiques"""
        print(f"📚 Recherche livres philosophie/sciences (max {max_books})")
        
        # Simulation données (Gutenberg réel nécessiterait parsing HTML complexe)
        classic_books = [
            {
                "id": "gutenberg_1",
                "title": "The Origin of Species",
                "author": "Charles Darwin", 
                "year": "1859",
                "language": "english",
                "subject": ["evolution", "natural selection", "biology"],
                "url": "https://www.gutenberg.org/ebooks/1228",
                "text_sample": "When on board H.M.S. 'Beagle,' as naturalist, I was much struck with certain facts in the distribution of the inhabitants of South America, and in the geological relations of the present to the past inhabitants of that continent. These facts seemed to me to throw some light on the origin of species—that mystery of mysteries, as it has been called by one of our greatest philosophers."
            },
            {
                "id": "gutenberg_2", 
                "title": "A Treatise of Human Nature",
                "author": "David Hume",
                "year": "1739",
                "language": "english", 
                "subject": ["philosophy", "empiricism", "causation"],
                "url": "https://www.gutenberg.org/ebooks/4705",
                "text_sample": "Nothing is more usual and more natural for those, who pretend to discover anything new to the world in philosophy and the sciences, than to insinuate the praises of their own systems, by decrying all those, which have been advanced before them."
            },
            {
                "id": "gutenberg_3",
                "title": "The Wealth of Nations", 
                "author": "Adam Smith",
                "year": "1776",
                "language": "english",
                "subject": ["economics", "capitalism", "invisible hand"],
                "url": "https://www.gutenberg.org/ebooks/3300",
                "text_sample": "The greatest improvement in the productive powers of labour, and the greater part of the skill, dexterity, and judgment with which it is any where directed, or applied, seem to have been the effects of the division of labour."
            },
            {
                "id": "gutenberg_4",
                "title": "Critique of Pure Reason",
                "author": "Immanuel Kant", 
                "year": "1781",
                "language": "english",
                "subject": ["philosophy", "metaphysics", "epistemology"],
                "url": "https://www.gutenberg.org/ebooks/4280",
                "text_sample": "Human reason, in one sphere of its cognition, is called upon to consider questions, which it cannot decline, as they are presented by its own nature, but which it cannot answer, as they transcend every faculty of the mind."
            },
            {
                "id": "gutenberg_5",
                "title": "On the Principles of Political Economy",
                "author": "John Stuart Mill",
                "year": "1848", 
                "language": "english",
                "subject": ["economics", "utilitarianism", "liberty"],
                "url": "https://www.gutenberg.org/ebooks/30107",
                "text_sample": "The science of Political Economy stands in closer connexion with the higher departments of human intellect than any other branch of the speculative philosophy."
            }
        ]
        
        books = []
        for book_data in classic_books[:max_books]:
            book = BookMetadata(**book_data)
            books.append(book)
            
        print(f"  ✅ {len(books)} livres classiques récupérés")
        return books
    
    def extract_historical_concepts(self, books: List[BookMetadata]) -> List[SemanticAtom]:
        """Extraction concepts historiques depuis livres classiques"""
        print(f"🧠 Extraction concepts historiques depuis {len(books)} livres...")
        
        extracted_atoms = []
        
        for i, book in enumerate(books, 1):
            print(f"  [{i}/{len(books)}] {book.title} ({book.year})")
            
            # Extraction concepts depuis sample + sujets
            concepts = self._extract_concepts_from_book(book)
            
            for concept in concepts:
                # Génération ID unique
                atom_id = hashlib.md5(f"{concept}_{book.id}_{datetime.datetime.now()}".encode()).hexdigest()[:8]
                
                # Contexte enrichi historique
                context = f"Livre: {book.title} ({book.year})\nAuteur: {book.author}\nSujets: {', '.join(book.subject)}\nExtrait: {book.text_sample[:300]}..."
                
                # Définition contextuelle
                definition = self._extract_historical_definition(concept, book)
                
                # Création atome sémantique historique
                atom = SemanticAtom(
                    id=atom_id,
                    concept=concept,
                    definition=definition,
                    context=context,
                    provenance=ProvenanceRecord(
                        source_agent=self.agent.id,
                        timestamp=datetime.datetime.now().isoformat(),
                        method=f"historical_books_extraction_{self.agent.version}",
                        source_url=book.url,
                        extraction_confidence=self._calculate_historical_confidence(concept, book),
                        parent_sources=[book.url, f"historical_year_{book.year}"]
                    )
                )
                
                extracted_atoms.append(atom)
                
            time.sleep(0.1)  # Rate limiting
        
        self.atoms.extend(extracted_atoms)
        print(f"  ✅ {len(extracted_atoms)} concepts historiques extraits")
        return extracted_atoms
    
    def _extract_concepts_from_book(self, book: BookMetadata) -> List[str]:
        """Extraction concepts depuis métadonnées + échantillon livre"""
        concepts = set()
        
        # Concepts depuis sujets explicites
        for subject in book.subject:
            concepts.add(subject.lower())
            
        # Concepts depuis texte sample (philosophiques/scientifiques)
        text = book.text_sample.lower()
        
        # Patterns concepts philosophiques/scientifiques
        patterns = [
            r'\b(reason|reasoning)\b',
            r'\b(nature|natural)\b', 
            r'\b(knowledge|science)\b',
            r'\b(truth|reality)\b',
            r'\b(experience|empirical)\b',
            r'\b(cause|causation)\b',
            r'\b(principle|law)\b',
            r'\b(theory|hypothesis)\b',
            r'\b(observation|experiment)\b',
            r'\b(mind|consciousness)\b'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) > 3:
                    concepts.add(match)
        
        # Filtrage et limitation
        filtered = [c for c in concepts if len(c) >= 4 and c not in {'that', 'with', 'have', 'been', 'this', 'they'}]
        return list(filtered)[:8]  # Top 8 par livre
    
    def _extract_historical_definition(self, concept: str, book: BookMetadata) -> str:
        """Extraction définition contextuelle historique"""
        # Définition contextuelle avec époque
        return f"{concept.title()} selon {book.author} ({book.year}): concept développé dans '{book.title}'"
    
    def _calculate_historical_confidence(self, concept: str, book: BookMetadata) -> float:
        """Calcul confiance extraction historique"""
        confidence = 0.75  # Base historique
        
        # Bonus si concept dans sujets explicites
        if concept in [s.lower() for s in book.subject]:
            confidence += 0.15
            
        # Bonus auteurs reconnus
        famous_authors = ['darwin', 'kant', 'hume', 'smith', 'mill', 'aristotle', 'plato']
        if any(author in book.author.lower() for author in famous_authors):
            confidence += 0.1
            
        # Bonus périodes importantes
        year = int(book.year) if book.year.isdigit() else 1800
        if 1750 <= year <= 1900:  # Période Lumières/Révolution industrielle
            confidence += 0.05
            
        return min(confidence, 0.95)
    
    def save_historical_store(self, filename: str, books_metadata: List[BookMetadata]):
        """Sauvegarde avec métadonnées historiques"""
        store = {
            "collection_metadata": {
                "collector_agent": asdict(self.agent),
                "collection_date": datetime.datetime.now().isoformat(),
                "total_atoms": len(self.atoms),
                "source_type": "historical_books",
                "books_count": len(books_metadata),
                "temporal_range": {
                    "earliest": min(book.year for book in books_metadata if book.year.isdigit()),
                    "latest": max(book.year for book in books_metadata if book.year.isdigit())
                },
                "version": "0.3.0"
            },
            "source_books": [asdict(book) for book in books_metadata],
            "semantic_atoms": [asdict(atom) for atom in self.atoms]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(store, f, indent=2, ensure_ascii=False)
            
        print(f"✅ {len(self.atoms)} atomes + {len(books_metadata)} livres sauvés dans {filename}")

def main():
    print("📚 COLLECTEUR LIVRES HISTORIQUES AVEC TRAÇABILITÉ")
    print("================================================")
    
    # Configuration agent collecteur livres
    agent = Agent(
        id="books_collector_v1",
        type="machine", 
        name="PaniniFS Historical Books Collector",
        version="1.0.0",
        bias_profile={
            "source": "historical_books_gutenberg", 
            "language": "english", 
            "cultural_context": "western_classical",
            "extraction_method": "historical_context_analysis",
            "temporal_focus": "1700-1900_classical_period"
        }
    )
    
    print(f"🤖 Agent configuré: {agent.name} v{agent.version}")
    
    collector = BooksCollector(agent)
    
    print(f"\n📊 Collecte livres historiques:")
    
    # Recherche livres philosophie/sciences
    books = collector.search_philosophy_books(max_books=5)
    
    # Extraction concepts historiques
    if books:
        collector.extract_historical_concepts(books)
    
    # Sauvegarde avec contexte historique
    store_file = "historical_books_semantic_store.json"
    collector.save_historical_store(store_file, books)
    
    print(f"\n🎯 COLLECTE LIVRES HISTORIQUES TERMINÉE")
    print(f"✨ {len(collector.atoms)} concepts historiques extraits")
    print(f"📚 {len(books)} livres classiques analysés") 
    print(f"💾 Données: {store_file}")
    print(f"⏰ Perspective temporelle: concepts 1700-1900")

if __name__ == "__main__":
    main()
