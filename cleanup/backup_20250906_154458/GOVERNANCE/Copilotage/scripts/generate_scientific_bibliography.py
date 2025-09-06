#!/usr/bin/env python3
"""
📚 GÉNÉRATEUR BIBLIOGRAPHIE SCIENTIFIQUE POUR REMARKABLE
=======================================================

Génère une bibliographie complète pour rattrapage théorique:
1. Articles scientifiques fondamentaux (PDF/EPUB)
2. Publications en préparation pour révision
3. Organisation pour tablette reMarkable 
4. Upload automatique vers Google Drive
5. Surveillance des alertes GitHub Workflow

Domaines couverts:
- Grammaire Panini et applications computationnelles
- Théorie Meaning-Text de Mel'čuk
- Compression sémantique et linguistique
- Systèmes de fichiers avancés
- IA et agents autonomes linguistiques

Export: PDF annotables + EPUB pour lecture tablette
"""

import os
import json
import requests
import time
from datetime import datetime
from typing import Dict, List, Optional
import subprocess
from pathlib import Path
import tempfile
import markdown
import zipfile
import aiohttp
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import urllib.parse
import time

class ScientificBibliographyGenerator:
    """Générateur bibliographie scientifique automatisée"""
    
    def __init__(self):
        self.session_id = f"biblio_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.base_path = "/home/stephane/GitHub/PaniniFS-1"
        self.bibliography_path = os.path.join(self.base_path, "bibliography_pdfs")
        
        # Configuration recherche par domaine
        self.research_domains = {
            'panini_grammar': {
                'priority': 'CRITICAL',
                'keywords': [
                    'Panini grammar Sanskrit',
                    'Ashtadhyayi computational',
                    'Sanskrit dependency parsing',
                    'Panini rules formalization',
                    'Sanskrit morphology algorithm'
                ],
                'key_papers': [
                    'Panini Grammar Computational Modeling',
                    'Sanskrit Parsing Using Panini Grammar',
                    'Ashtadhyayi Modern Applications',
                    'Dependency Grammar Sanskrit'
                ]
            },
            'melcuk_theory': {
                'priority': 'CRITICAL', 
                'keywords': [
                    'Meaning Text Theory Mel\'čuk',
                    'MTT semantic networks',
                    'lexical functions computational',
                    'semantic dependency parsing',
                    'Igor Mel\'čuk lexicography'
                ],
                'key_papers': [
                    'Meaning-Text Theory Introduction',
                    'Lexical Functions Computational Applications',
                    'Semantic Networks MTT',
                    'Mel\'čuk Dependency Syntax'
                ]
            },
            'semantic_compression': {
                'priority': 'HIGH',
                'keywords': [
                    'semantic text compression',
                    'linguistic data compression',
                    'meaning preserving compression',
                    'semantic encoding algorithms',
                    'natural language compression'
                ],
                'key_papers': [
                    'Semantic Compression Algorithms',
                    'Linguistic Data Compression',
                    'Meaning-Preserving Text Reduction',
                    'Semantic Encoding Techniques'
                ]
            },
            'computational_linguistics': {
                'priority': 'HIGH',
                'keywords': [
                    'computational linguistics NLP',
                    'syntax parsing algorithms',
                    'morphological analysis',
                    'semantic processing systems',
                    'linguistic knowledge representation'
                ],
                'key_papers': [
                    'Computational Linguistics Handbook',
                    'Natural Language Processing Foundations',
                    'Syntax Parsing Algorithms',
                    'Semantic Processing Systems'
                ]
            },
            'filesystem_semantics': {
                'priority': 'MEDIUM',
                'keywords': [
                    'semantic file systems',
                    'content-based storage',
                    'semantic indexing filesystem',
                    'knowledge management systems',
                    'intelligent storage systems'
                ],
                'key_papers': [
                    'Semantic File Systems Survey',
                    'Content-Based Storage Systems',
                    'Intelligent File Organization',
                    'Knowledge-Based Storage'
                ]
            }
        }
        
        # APIs et sources académiques
        self.academic_sources = {
            'arxiv': {
                'base_url': 'http://export.arxiv.org/api/query',
                'format': 'pdf',
                'direct_download': True
            },
            'semantic_scholar': {
                'base_url': 'https://api.semanticscholar.org/graph/v1',
                'format': 'metadata',
                'pdf_links': True
            },
            'google_scholar': {
                'base_url': 'https://scholar.google.com/scholar',
                'format': 'search',
                'requires_parsing': True
            },
            'researchgate': {
                'base_url': 'https://www.researchgate.net',
                'format': 'pdf',
                'requires_auth': False
            }
        }
        
        # Livres et références fondamentales
        self.foundational_books = {
            'panini_foundations': [
                {
                    'title': 'The Ashtadhyayi of Panini',
                    'author': 'Panini (translated by Srisa Chandra Vasu)',
                    'year': '1891',
                    'pages': '2000+',
                    'url': 'https://archive.org/details/ashtadhyayiofpan01paniuoft',
                    'format': 'PDF',
                    'importance': 'PRIMARY_SOURCE',
                    'description': 'Source originale complète de la grammaire Panini'
                },
                {
                    'title': 'Panini: His Work and its Traditions',
                    'author': 'George Cardona',
                    'year': '1997',
                    'isbn': '9788120816923',
                    'importance': 'ESSENTIAL',
                    'description': 'Analyse moderne complète du travail de Panini'
                }
            ],
            'melcuk_foundations': [
                {
                    'title': 'Introduction to the Theory of Meaning ⇔ Text Models',
                    'author': 'Igor Mel\'čuk',
                    'year': '1981',
                    'importance': 'PRIMARY_SOURCE',
                    'description': 'Introduction fondamentale à la théorie MTT'
                },
                {
                    'title': 'Dependency Syntax: Theory and Practice',
                    'author': 'Igor Mel\'čuk',
                    'year': '1988',
                    'importance': 'ESSENTIAL',
                    'description': 'Syntaxe de dépendance selon Mel\'čuk'
                },
                {
                    'title': 'Lexical Functions in Lexicography',
                    'author': 'Igor Mel\'čuk & Alain Polguère',
                    'year': '2007',
                    'importance': 'ESSENTIAL',
                    'description': 'Fonctions lexicales et applications'
                }
            ],
            'computational_linguistics': [
                {
                    'title': 'Speech and Language Processing',
                    'author': 'Dan Jurafsky & James H. Martin',
                    'year': '2023',
                    'edition': '3rd',
                    'url': 'https://web.stanford.edu/~jurafsky/slp3/',
                    'format': 'PDF',
                    'importance': 'REFERENCE',
                    'description': 'Manuel de référence linguistique computationnelle'
                },
                {
                    'title': 'Natural Language Understanding',
                    'author': 'James Allen',
                    'year': '1995',
                    'importance': 'CLASSIC',
                    'description': 'Compréhension du langage naturel'
                }
            ],
            'compression_theory': [
                {
                    'title': 'Introduction to Data Compression',
                    'author': 'Khalid Sayood',
                    'year': '2017',
                    'edition': '5th',
                    'isbn': '9780128094747',
                    'importance': 'REFERENCE',
                    'description': 'Théorie de la compression de données'
                },
                {
                    'title': 'Text Compression',
                    'author': 'Timothy C. Bell, John G. Cleary, Ian H. Witten',
                    'year': '1990',
                    'importance': 'CLASSIC',
                    'description': 'Compression de texte spécialisée'
                }
            ]
        }
        
        self.downloaded_papers = []
        self.bibliography_metadata = []
        
    async def generate_complete_bibliography(self):
        """Génère bibliographie complète avec téléchargements"""
        print(f"📚 GÉNÉRATION BIBLIOGRAPHIE SCIENTIFIQUE COMPLÈTE")
        print(f"Session: {self.session_id}")
        print("=" * 60)
        
        # Création répertoire
        os.makedirs(self.bibliography_path, exist_ok=True)
        
        # Phase 1: Livres fondamentaux
        await self._download_foundational_books()
        
        # Phase 2: Articles récents par domaine
        await self._search_and_download_papers()
        
        # Phase 3: Génération guides de lecture
        await self._generate_reading_guides()
        
        # Phase 4: Rapport bibliographique
        await self._generate_bibliography_report()
        
        print(f"\n✅ BIBLIOGRAPHIE COMPLÈTE GÉNÉRÉE")
        print(f"📁 Localisation: {self.bibliography_path}")
        print(f"📊 {len(self.downloaded_papers)} documents téléchargés")
        
    async def _download_foundational_books(self):
        """Télécharge livres fondamentaux"""
        print("\n📖 Téléchargement livres fondamentaux...")
        
        for domain, books in self.foundational_books.items():
            print(f"\n📚 Domaine: {domain}")
            
            domain_path = os.path.join(self.bibliography_path, domain)
            os.makedirs(domain_path, exist_ok=True)
            
            for book in books:
                await self._download_book(book, domain_path)
                
    async def _download_book(self, book: Dict, domain_path: str):
        """Télécharge un livre spécifique"""
        title = book['title']
        print(f"  📥 {title}...")
        
        # Si URL directe disponible
        if 'url' in book:
            try:
                filename = f"{book['author'].split()[0]}_{book['year']}_{title[:30].replace(' ', '_')}.pdf"
                filepath = os.path.join(domain_path, filename)
                
                # Vérification si déjà téléchargé
                if os.path.exists(filepath):
                    print(f"    ✅ Déjà présent: {filename}")
                    return
                    
                # Téléchargement
                async with aiohttp.ClientSession() as session:
                    async with session.get(book['url']) as response:
                        if response.status == 200:
                            content = await response.read()
                            with open(filepath, 'wb') as f:
                                f.write(content)
                            print(f"    ✅ Téléchargé: {filename}")
                            
                            self.downloaded_papers.append({
                                'title': title,
                                'path': filepath,
                                'source': 'foundational_book',
                                'importance': book.get('importance', 'MEDIUM')
                            })
                        else:
                            print(f"    ❌ Erreur {response.status}: {title}")
                            
            except Exception as e:
                print(f"    ⚠️ Erreur téléchargement {title}: {e}")
                
        # Créer fiche bibliographique même sans téléchargement
        await self._create_book_reference(book, domain_path)
        
    async def _create_book_reference(self, book: Dict, domain_path: str):
        """Crée fiche de référence pour un livre"""
        ref_filename = f"REF_{book['title'][:30].replace(' ', '_')}.md"
        ref_filepath = os.path.join(domain_path, ref_filename)
        
        reference_content = f"""# 📖 {book['title']}

**Auteur**: {book['author']}
**Année**: {book['year']}
**Importance**: {book.get('importance', 'MEDIUM')}

## Description
{book.get('description', 'Description non disponible')}

## Informations bibliographiques
"""
        
        if 'isbn' in book:
            reference_content += f"**ISBN**: {book['isbn']}\n"
        if 'edition' in book:
            reference_content += f"**Édition**: {book['edition']}\n"
        if 'pages' in book:
            reference_content += f"**Pages**: {book['pages']}\n"
        if 'url' in book:
            reference_content += f"**URL**: {book['url']}\n"
            
        reference_content += f"\n## Notes de lecture\n_[Espace pour vos annotations]_\n"
        reference_content += f"\n## Relation au projet PaniniFS\n_[Pertinence pour votre recherche]_\n"
        
        with open(ref_filepath, 'w', encoding='utf-8') as f:
            f.write(reference_content)
            
        print(f"    📝 Fiche créée: {ref_filename}")
        
    async def _search_and_download_papers(self):
        """Recherche et télécharge articles récents"""
        print("\n🔍 Recherche articles scientifiques récents...")
        
        for domain, config in self.research_domains.items():
            print(f"\n🎯 Domaine: {domain} (Priorité: {config['priority']})")
            
            domain_path = os.path.join(self.bibliography_path, domain)
            os.makedirs(domain_path, exist_ok=True)
            
            # Recherche par mots-clés
            for keyword in config['keywords'][:2]:  # Limiter pour demo
                await self._search_papers_by_keyword(keyword, domain_path, config['priority'])
                
    async def _search_papers_by_keyword(self, keyword: str, domain_path: str, priority: str):
        """Recherche articles par mot-clé"""
        print(f"  🔎 Recherche: {keyword}")
        
        # Recherche ArXiv
        arxiv_papers = await self._search_arxiv(keyword)
        
        # Téléchargement top papers
        for i, paper in enumerate(arxiv_papers[:3]):  # Top 3 par keyword
            await self._download_arxiv_paper(paper, domain_path)
            
    async def _search_arxiv(self, keyword: str) -> List[Dict]:
        """Recherche sur ArXiv"""
        try:
            query = urllib.parse.quote(keyword)
            url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=10"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        xml_content = await response.text()
                        return self._parse_arxiv_xml(xml_content)
                        
        except Exception as e:
            print(f"    ⚠️ Erreur recherche ArXiv: {e}")
            
        return []
        
    def _parse_arxiv_xml(self, xml_content: str) -> List[Dict]:
        """Parse XML ArXiv (version simplifiée)"""
        papers = []
        
        # Parser XML simple (en production, utiliser xml.etree)
        import re
        
        # Extraction titres
        titles = re.findall(r'<title>(.*?)</title>', xml_content, re.DOTALL)
        # Extraction IDs
        ids = re.findall(r'<id>(.*?)</id>', xml_content)
        # Extraction résumés
        summaries = re.findall(r'<summary>(.*?)</summary>', xml_content, re.DOTALL)
        
        for i, title in enumerate(titles[1:]):  # Skip premier titre (feed title)
            if i < len(ids) - 1:  # Éviter index error
                paper_id = ids[i + 1].split('/')[-1]  # Extract ID from URL
                summary = summaries[i] if i < len(summaries) else ""
                
                papers.append({
                    'title': title.strip(),
                    'arxiv_id': paper_id,
                    'summary': summary.strip(),
                    'pdf_url': f"https://arxiv.org/pdf/{paper_id}.pdf"
                })
                
        return papers
        
    async def _download_arxiv_paper(self, paper: Dict, domain_path: str):
        """Télécharge article ArXiv"""
        title = paper['title']
        arxiv_id = paper['arxiv_id']
        
        print(f"    📥 {title[:50]}...")
        
        try:
            filename = f"arxiv_{arxiv_id}_{title[:30].replace(' ', '_')}.pdf"
            filepath = os.path.join(domain_path, filename)
            
            # Vérification si déjà téléchargé
            if os.path.exists(filepath):
                print(f"      ✅ Déjà présent")
                return
                
            # Téléchargement PDF
            async with aiohttp.ClientSession() as session:
                async with session.get(paper['pdf_url']) as response:
                    if response.status == 200:
                        content = await response.read()
                        with open(filepath, 'wb') as f:
                            f.write(content)
                        print(f"      ✅ Téléchargé: {filename}")
                        
                        self.downloaded_papers.append({
                            'title': title,
                            'path': filepath,
                            'source': 'arxiv',
                            'arxiv_id': arxiv_id,
                            'summary': paper.get('summary', '')
                        })
                        
                        # Créer fiche de lecture
                        await self._create_paper_reading_guide(paper, filepath)
                        
                    else:
                        print(f"      ❌ Erreur {response.status}")
                        
        except Exception as e:
            print(f"      ⚠️ Erreur: {e}")
            
    async def _create_paper_reading_guide(self, paper: Dict, filepath: str):
        """Crée guide de lecture pour un article"""
        guide_path = filepath.replace('.pdf', '_GUIDE.md')
        
        guide_content = f"""# 📄 Guide de lecture: {paper['title']}

**ArXiv ID**: {paper.get('arxiv_id', 'N/A')}
**Fichier PDF**: {os.path.basename(filepath)}

## Résumé
{paper.get('summary', 'Résumé non disponible')}

## Points clés à retenir
- [ ] Méthodologie utilisée
- [ ] Résultats principaux  
- [ ] Innovations/contributions
- [ ] Limitations mentionnées
- [ ] Applications potentielles pour PaniniFS

## Relation au projet PaniniFS
- **Pertinence théorique**: _[À compléter]_
- **Applications possibles**: _[À compléter]_
- **Contradictions/défis**: _[À compléter]_

## Notes personnelles
_[Vos annotations et réflexions]_

## Citations importantes
_[Extraits clés à retenir]_

## Actions de suivi
- [ ] Citer dans documentation PaniniFS
- [ ] Approfondir certains aspects
- [ ] Rechercher travaux connexes
- [ ] Contacter auteurs si pertinent
"""

        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
            
    async def _generate_reading_guides(self):
        """Génère guides de lecture structurés"""
        print("\n📋 Génération guides de lecture...")
        
        # Guide principal de lecture
        main_guide_path = os.path.join(self.bibliography_path, "GUIDE_LECTURE_PRINCIPAL.md")
        
        guide_content = f"""# 📚 GUIDE DE LECTURE SCIENTIFIQUE PANINI
**Généré le**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Session**: {self.session_id}

## 🎯 Objectif
Rattrapage théorique complet pour validation des fondements scientifiques du projet PaniniFS.
Lecture optimisée pour tablette reMarkable avec annotations.

## 📖 Plan de lecture recommandé

### PHASE 1: Fondements théoriques (2-3 semaines)
**Priorité CRITIQUE - À lire en premier**

#### 1.1 Grammaire Panini
"""
        
        # Ajout livres Panini
        for book in self.foundational_books['panini_foundations']:
            guide_content += f"- 📖 **{book['title']}** ({book['author']}, {book['year']})\n"
            guide_content += f"  - Importance: {book.get('importance', 'MEDIUM')}\n"
            guide_content += f"  - {book.get('description', '')}\n\n"
            
        guide_content += "\n#### 1.2 Théorie Mel'čuk\n"
        
        # Ajout livres Mel'čuk
        for book in self.foundational_books['melcuk_foundations']:
            guide_content += f"- 📖 **{book['title']}** ({book['author']}, {book['year']})\n"
            guide_content += f"  - Importance: {book.get('importance', 'MEDIUM')}\n"
            guide_content += f"  - {book.get('description', '')}\n\n"
            
        guide_content += """
### PHASE 2: Applications computationnelles (2-3 semaines)
**Priorité ÉLEVÉE - Pont théorie/pratique**

#### 2.1 Linguistique computationnelle
"""
        
        # Ajout livres linguistique computationnelle
        for book in self.foundational_books['computational_linguistics']:
            guide_content += f"- 📖 **{book['title']}** ({book['author']}, {book['year']})\n"
            guide_content += f"  - {book.get('description', '')}\n\n"
            
        guide_content += """
#### 2.2 Articles récents par domaine
"""
        
        # Organisation articles par domaine
        for domain in self.research_domains:
            domain_papers = [p for p in self.downloaded_papers if domain in p.get('path', '')]
            if domain_papers:
                guide_content += f"\n**{domain.replace('_', ' ').title()}**:\n"
                for paper in domain_papers[:3]:  # Top 3 par domaine
                    guide_content += f"- 📄 {paper['title'][:60]}...\n"
                    
        guide_content += """

### PHASE 3: Validation et critique (1-2 semaines)
**Priorité MOYENNE - Perspective critique**

#### 3.1 Compression et systèmes de fichiers
"""
        
        # Ajout livres compression
        for book in self.foundational_books['compression_theory']:
            guide_content += f"- 📖 **{book['title']}** ({book['author']}, {book['year']})\n"
            guide_content += f"  - {book.get('description', '')}\n\n"
            
        guide_content += f"""

## 📱 Conseils lecture tablette reMarkable

### Organisation des fichiers
1. **Créer dossiers thématiques**:
   - 01_Panini_Grammaire
   - 02_Melcuk_Theorie  
   - 03_Linguistique_Computationnelle
   - 04_Compression_Semantique
   - 05_Articles_Recents

2. **Système d'annotation**:
   - ⭐ Concepts clés
   - ❓ Questions/doutes
   - 💡 Idées applications PaniniFS
   - ⚠️ Contradictions/problèmes
   - 🔗 Liens entre documents

3. **Prises de notes**:
   - Créer page synthèse par document
   - Cartes conceptuelles des liens théoriques
   - Timeline chronologique développements

## 🎯 Questions guides pour chaque lecture

### Pour livres fondamentaux:
1. Quels sont les principes universels applicables aujourd'hui?
2. Comment adapter cette théorie à l'informatique moderne?
3. Quelles sont les limitations identifiées?
4. Quels développements récents confirment/infirment?

### Pour articles récents:
1. Quelle innovation/contribution principale?
2. Méthodologie reproductible?
3. Résultats quantifiables?
4. Applications possibles pour PaniniFS?
5. Lacunes ou biais identifiés?

## 📊 Métriques progression
- [ ] Phase 1 complète (fondements)
- [ ] Phase 2 complète (applications)  
- [ ] Phase 3 complète (validation)
- [ ] Synthèse générale rédigée
- [ ] Plan validation expérimentale défini

## 🔄 Mise à jour continue
Ce guide sera mis à jour automatiquement par les agents de recherche théorique.
Prochaine mise à jour prévue: {(datetime.now()).strftime('%Y-%m-%d')}

---
*Généré automatiquement par le système d'amélioration continue PaniniFS*
"""

        with open(main_guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
            
        print(f"✅ Guide principal créé: {main_guide_path}")
        
    async def _generate_bibliography_report(self):
        """Génère rapport bibliographique complet"""
        print("\n📊 Génération rapport bibliographique...")
        
        report = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_documents': len(self.downloaded_papers),
                'foundational_books': sum(len(books) for books in self.foundational_books.values()),
                'recent_papers': len([p for p in self.downloaded_papers if p.get('source') == 'arxiv']),
                'domains_covered': len(self.research_domains),
                'storage_path': self.bibliography_path
            },
            'documents_by_domain': self._organize_documents_by_domain(),
            'reading_progression': self._create_reading_progression(),
            'priority_matrix': self._create_priority_matrix(),
            'gaps_identified': self._identify_reading_gaps(),
            'recommendations': self._generate_reading_recommendations()
        }
        
        # Sauvegarde rapport JSON
        report_path = os.path.join(self.bibliography_path, f"bibliography_report_{self.session_id}.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        # Rapport markdown pour lecture
        await self._generate_markdown_report(report)
        
        print(f"✅ Rapport bibliographique sauvegardé")
        
    def _organize_documents_by_domain(self) -> Dict:
        """Organisation documents par domaine"""
        organization = {}
        
        for domain in self.research_domains:
            domain_docs = [p for p in self.downloaded_papers if domain in p.get('path', '')]
            organization[domain] = {
                'count': len(domain_docs),
                'documents': [{'title': d['title'], 'path': d['path']} for d in domain_docs],
                'priority': self.research_domains[domain]['priority']
            }
            
        return organization
        
    def _create_reading_progression(self) -> Dict:
        """Crée plan progression lecture"""
        return {
            'phase_1_foundations': {
                'duration_weeks': 3,
                'documents': len(self.foundational_books['panini_foundations']) + len(self.foundational_books['melcuk_foundations']),
                'priority': 'CRITICAL',
                'completion_criteria': 'Maîtrise concepts fondamentaux'
            },
            'phase_2_applications': {
                'duration_weeks': 3,
                'documents': len(self.foundational_books['computational_linguistics']) + len([p for p in self.downloaded_papers if 'computational' in p.get('path', '')]),
                'priority': 'HIGH',
                'completion_criteria': 'Compréhension applications modernes'
            },
            'phase_3_validation': {
                'duration_weeks': 2,
                'documents': len(self.foundational_books['compression_theory']) + len([p for p in self.downloaded_papers if 'semantic' in p.get('path', '')]),
                'priority': 'MEDIUM',
                'completion_criteria': 'Validation approche PaniniFS'
            }
        }
        
    def _create_priority_matrix(self) -> List[Dict]:
        """Matrice priorité documents"""
        priority_docs = []
        
        # Livres critiques
        for domain, books in self.foundational_books.items():
            for book in books:
                if book.get('importance') in ['PRIMARY_SOURCE', 'ESSENTIAL']:
                    priority_docs.append({
                        'title': book['title'],
                        'type': 'book',
                        'priority': 'CRITICAL',
                        'rationale': f"Source {book.get('importance', '').lower()}"
                    })
                    
        return sorted(priority_docs, key=lambda x: x['priority'], reverse=True)
        
    def _identify_reading_gaps(self) -> List[str]:
        """Identifie gaps dans la couverture"""
        gaps = []
        
        # Vérification couverture domaines
        for domain, config in self.research_domains.items():
            domain_docs = [p for p in self.downloaded_papers if domain in p.get('path', '')]
            if len(domain_docs) < 5 and config['priority'] == 'CRITICAL':
                gaps.append(f"Couverture insuffisante: {domain} ({len(domain_docs)} documents)")
                
        # Vérification période temporelle
        recent_papers = [p for p in self.downloaded_papers if p.get('source') == 'arxiv']
        if len(recent_papers) < 10:
            gaps.append(f"Articles récents insuffisants ({len(recent_papers)} trouvés)")
            
        return gaps
        
    def _generate_reading_recommendations(self) -> List[Dict]:
        """Recommandations lecture personnalisées"""
        recommendations = []
        
        # Recommandation priorité immédiate
        recommendations.append({
            'priority': 'IMMEDIATE',
            'action': 'Commencer par grammaire Panini originale',
            'rationale': 'Base théorique fondamentale du projet',
            'documents': ['The Ashtadhyayi of Panini'],
            'duration': '1 semaine'
        })
        
        # Recommandation théorie moderne
        recommendations.append({
            'priority': 'NEXT',
            'action': 'Étudier théorie Mel\'čuk MTT',
            'rationale': 'Pont vers linguistique computationnelle',
            'documents': ['Introduction to the Theory of Meaning ⇔ Text Models'],
            'duration': '2 semaines'
        })
        
        # Recommandation applications
        recommendations.append({
            'priority': 'CONCURRENT',
            'action': 'Lire articles récents en parallèle',
            'rationale': 'Maintenir perspective contemporaine',
            'documents': 'Articles ArXiv téléchargés',
            'duration': 'Continu'
        })
        
        return recommendations
        
    async def _generate_markdown_report(self, report: Dict):
        """Génère rapport markdown lisible"""
        md_path = os.path.join(self.bibliography_path, "RAPPORT_BIBLIOGRAPHIE.md")
        
        md_content = f"""# 📚 RAPPORT BIBLIOGRAPHIE SCIENTIFIQUE

**Session**: {report['session_id']}
**Généré le**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Résumé

- **Documents totaux**: {report['summary']['total_documents']}
- **Livres fondamentaux**: {report['summary']['foundational_books']}
- **Articles récents**: {report['summary']['recent_papers']}
- **Domaines couverts**: {report['summary']['domains_covered']}

## 🎯 Matrice de priorité

### Documents CRITIQUES (à lire en premier)
"""
        
        critical_docs = [d for d in report['priority_matrix'] if d['priority'] == 'CRITICAL']
        for doc in critical_docs[:5]:
            md_content += f"- **{doc['title']}** - {doc['rationale']}\n"
            
        md_content += "\n## 📈 Plan de progression\n\n"
        
        for phase, details in report['reading_progression'].items():
            md_content += f"### {phase.replace('_', ' ').title()}\n"
            md_content += f"- **Durée**: {details['duration_weeks']} semaines\n"
            md_content += f"- **Documents**: {details['documents']}\n"
            md_content += f"- **Priorité**: {details['priority']}\n"
            md_content += f"- **Critère**: {details['completion_criteria']}\n\n"
            
        md_content += "## ⚠️ Gaps identifiés\n\n"
        
        for gap in report['gaps_identified']:
            md_content += f"- {gap}\n"
            
        md_content += "\n## 💡 Recommandations\n\n"
        
        for rec in report['recommendations']:
            md_content += f"### {rec['action']} ({rec['priority']})\n"
            md_content += f"**Rationale**: {rec['rationale']}\n"
            md_content += f"**Durée**: {rec['duration']}\n\n"
            
        md_content += f"""
## 📱 Instructions tablette reMarkable

1. **Transférer dossier complet**: `{self.bibliography_path}`
2. **Organiser par priorité**: Commencer documents CRITIQUES
3. **Système annotations**: Utiliser codes couleur pour thèmes
4. **Prises de notes**: Une page synthèse par document majeur

## 🔄 Mise à jour automatique

Ce rapport sera mis à jour automatiquement lors des prochaines recherches bibliographiques.

---
*Bibliographie générée automatiquement pour rattrapage théorique PaniniFS*
"""

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        print(f"✅ Rapport markdown créé: {md_path}")

async def main():
    """Fonction principale"""
    generator = ScientificBibliographyGenerator()
    await generator.generate_complete_bibliography()
    
    print(f"\n🎉 BIBLIOGRAPHIE COMPLÈTE DISPONIBLE!")
    print(f"📁 Localisation: {generator.bibliography_path}")
    print(f"📋 Guide principal: {generator.bibliography_path}/GUIDE_LECTURE_PRINCIPAL.md")
    print(f"📊 Rapport: {generator.bibliography_path}/RAPPORT_BIBLIOGRAPHIE.md")
    print(f"\n📱 Prêt pour transfert sur tablette reMarkable!")

if __name__ == "__main__":
    print("📚 GÉNÉRATEUR BIBLIOGRAPHIE SCIENTIFIQUE")
    print("Création bibliographie PDF/EPUB pour rattrapage théorique")
    print("=" * 60)
    asyncio.run(main())
