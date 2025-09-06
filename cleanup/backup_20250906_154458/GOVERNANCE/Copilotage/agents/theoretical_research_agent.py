#!/usr/bin/env python3
"""
🔬 AGENT DE RECHERCHE THÉORIQUE AUTONOME
====================================

Agent spécialisé dans la recherche bibliographique et théorique pour :
- Mise à jour des connaissances linguistiques (Panini, Mel'čuk, sémantique computationnelle)
- Identification des travaux similaires et état de l'art
- Évaluation de l'originalité des approches PaniniFS
- Appui scientifique aux hypothèses

Fonctionnement 100% autonome et externalisé via APIs académiques.
"""

import json
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional
import os
import asyncio
import aiohttp
from dataclasses import dataclass, asdict

@dataclass
class ResearchQuery:
    """Structure d'une requête de recherche théorique"""
    domain: str
    keywords: List[str]
    time_range: str  # "1990-2025", "2020-2025", etc.
    priority: str    # "HIGH", "MEDIUM", "LOW"
    focus: str       # "update", "similarity", "validation", "contradiction"

@dataclass
class TheoreticalPaper:
    """Structure d'un article théorique trouvé"""
    title: str
    authors: List[str]
    year: int
    abstract: str
    keywords: List[str]
    doi: Optional[str]
    relevance_score: float
    similarity_to_panini: float
    theoretical_contribution: str
    potential_validation: str
    potential_contradiction: str

class TheoreticalResearchAgent:
    """Agent autonome de recherche théorique"""
    
    def __init__(self):
        self.session_id = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.research_apis = {
            'arxiv': 'http://export.arxiv.org/api/query',
            'semantic_scholar': 'https://api.semanticscholar.org/graph/v1',
            'crossref': 'https://api.crossref.org/works',
            'openalex': 'https://api.openalex.org/works',
            # Note: APIs académiques gratuites pour recherche autonome
        }
        
        # Domaines de recherche prioritaires basés sur l'audit conceptuel
        self.research_domains = {
            'panini_grammar': {
                'keywords': ['Panini grammar', 'Sanskrit grammar', 'generative grammar', 
                           'dependency grammar', 'computational grammar'],
                'priority': 'HIGH',
                'gap_severity': 'CRITICAL'
            },
            'melcuk_theory': {
                'keywords': ['Meaning-Text Theory', 'MTT', 'Igor Mel\'čuk', 
                           'semantic networks', 'lexical functions'],
                'priority': 'HIGH', 
                'gap_severity': 'CRITICAL'
            },
            'semantic_compression': {
                'keywords': ['semantic compression', 'text compression', 
                           'linguistic compression', 'semantic encoding'],
                'priority': 'HIGH',
                'gap_severity': 'MAJOR'
            },
            'computational_linguistics': {
                'keywords': ['computational linguistics', 'NLP', 'semantic analysis',
                           'linguistic algorithms', 'grammar formalization'],
                'priority': 'MEDIUM',
                'gap_severity': 'MEDIUM'
            },
            'autonomous_agents': {
                'keywords': ['autonomous agents', 'linguistic agents', 
                           'multi-agent systems', 'computational agents'],
                'priority': 'LOW',
                'gap_severity': 'LOW'
            }
        }
        
        self.findings_db = []
        self.research_log = []
        
    async def autonomous_research_cycle(self):
        """Cycle de recherche autonome complet"""
        print(f"🔬 DÉMARRAGE RECHERCHE THÉORIQUE AUTONOME - Session {self.session_id}")
        
        # Phase 1: Recherche par domaine prioritaire
        for domain, config in self.research_domains.items():
            print(f"\n📚 Recherche domaine: {domain} (Priorité: {config['priority']})")
            await self._research_domain(domain, config)
            
        # Phase 2: Analyse croisée et similarités
        await self._analyze_cross_references()
        
        # Phase 3: Évaluation originalité PaniniFS
        await self._evaluate_originality()
        
        # Phase 4: Génération rapport théorique
        await self._generate_theoretical_report()
        
        print(f"\n✅ RECHERCHE THÉORIQUE TERMINÉE - {len(self.findings_db)} articles analysés")
        
    async def _research_domain(self, domain: str, config: Dict):
        """Recherche dans un domaine spécifique"""
        queries = []
        
        # Génération requêtes multiples pour couverture maximale
        for keyword in config['keywords']:
            # Recherche mise à jour (dernières 5 ans)
            queries.append(ResearchQuery(
                domain=domain,
                keywords=[keyword, 'computational', 'algorithm'],
                time_range="2020-2025",
                priority=config['priority'],
                focus="update"
            ))
            
            # Recherche similarité avec PaniniFS
            queries.append(ResearchQuery(
                domain=domain,
                keywords=[keyword, 'filesystem', 'compression', 'semantic'],
                time_range="1990-2025", 
                priority=config['priority'],
                focus="similarity"
            ))
            
        # Exécution parallèle des requêtes
        tasks = [self._execute_research_query(query) for query in queries]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filtrage et stockage résultats
        valid_results = [r for r in results if not isinstance(r, Exception)]
        for papers in valid_results:
            if papers:
                self.findings_db.extend(papers)
                
    async def _execute_research_query(self, query: ResearchQuery) -> List[TheoreticalPaper]:
        """Exécute une requête de recherche sur les APIs"""
        papers = []
        
        try:
            # ArXiv search
            arxiv_papers = await self._search_arxiv(query)
            papers.extend(arxiv_papers)
            
            # Semantic Scholar search 
            ss_papers = await self._search_semantic_scholar(query)
            papers.extend(ss_papers)
            
            # OpenAlex search
            oa_papers = await self._search_openalex(query)
            papers.extend(oa_papers)
            
            # Déduplication par titre
            unique_papers = self._deduplicate_papers(papers)
            
            self.research_log.append({
                'timestamp': datetime.now().isoformat(),
                'query': asdict(query),
                'results_count': len(unique_papers)
            })
            
            return unique_papers
            
        except Exception as e:
            print(f"⚠️ Erreur recherche {query.domain}: {e}")
            return []
            
    async def _search_arxiv(self, query: ResearchQuery) -> List[TheoreticalPaper]:
        """Recherche sur ArXiv"""
        search_terms = ' AND '.join(query.keywords)
        url = f"{self.research_apis['arxiv']}?search_query=all:{search_terms}&start=0&max_results=50"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        xml_content = await response.text()
                        return self._parse_arxiv_results(xml_content, query)
            except Exception as e:
                print(f"⚠️ Erreur ArXiv: {e}")
                
        return []
        
    async def _search_semantic_scholar(self, query: ResearchQuery) -> List[TheoreticalPaper]:
        """Recherche sur Semantic Scholar"""
        search_terms = '+'.join(query.keywords)
        url = f"{self.research_apis['semantic_scholar']}/paper/search?query={search_terms}&limit=50"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_semantic_scholar_results(data, query)
            except Exception as e:
                print(f"⚠️ Erreur Semantic Scholar: {e}")
                
        return []
        
    async def _search_openalex(self, query: ResearchQuery) -> List[TheoreticalPaper]:
        """Recherche sur OpenAlex"""
        search_terms = ' '.join(query.keywords)
        url = f"{self.research_apis['openalex']}?search={search_terms}&per-page=50"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_openalex_results(data, query)
            except Exception as e:
                print(f"⚠️ Erreur OpenAlex: {e}")
                
        return []
        
    def _parse_arxiv_results(self, xml_content: str, query: ResearchQuery) -> List[TheoreticalPaper]:
        """Parse résultats ArXiv (XML)"""
        # Simplified parsing - in production use proper XML parser
        papers = []
        # TODO: Implement proper XML parsing
        return papers
        
    def _parse_semantic_scholar_results(self, data: Dict, query: ResearchQuery) -> List[TheoreticalPaper]:
        """Parse résultats Semantic Scholar"""
        papers = []
        for paper_data in data.get('data', []):
            try:
                paper = TheoreticalPaper(
                    title=paper_data.get('title', ''),
                    authors=[author.get('name', '') for author in paper_data.get('authors', [])],
                    year=paper_data.get('year', 0),
                    abstract=paper_data.get('abstract', ''),
                    keywords=[],  # Extract from abstract if available
                    doi=paper_data.get('doi'),
                    relevance_score=self._calculate_relevance(paper_data, query),
                    similarity_to_panini=self._calculate_panini_similarity(paper_data),
                    theoretical_contribution='',  # To be analyzed
                    potential_validation='',      # To be analyzed
                    potential_contradiction=''    # To be analyzed
                )
                papers.append(paper)
            except Exception as e:
                print(f"⚠️ Erreur parsing paper: {e}")
                
        return papers
        
    def _parse_openalex_results(self, data: Dict, query: ResearchQuery) -> List[TheoreticalPaper]:
        """Parse résultats OpenAlex"""
        papers = []
        for work in data.get('results', []):
            try:
                paper = TheoreticalPaper(
                    title=work.get('title', ''),
                    authors=[author.get('display_name', '') for author in work.get('authorships', [])],
                    year=work.get('publication_year', 0),
                    abstract=work.get('abstract', ''),
                    keywords=work.get('keywords', []),
                    doi=work.get('doi'),
                    relevance_score=self._calculate_relevance(work, query),
                    similarity_to_panini=self._calculate_panini_similarity(work),
                    theoretical_contribution='',
                    potential_validation='',
                    potential_contradiction=''
                )
                papers.append(paper)
            except Exception as e:
                print(f"⚠️ Erreur parsing work: {e}")
                
        return papers
        
    def _calculate_relevance(self, paper_data: Dict, query: ResearchQuery) -> float:
        """Calcule score de pertinence d'un article"""
        score = 0.0
        title = paper_data.get('title', '').lower()
        abstract = paper_data.get('abstract', '').lower()
        text = f"{title} {abstract}"
        
        # Score basé sur présence mots-clés
        for keyword in query.keywords:
            if keyword.lower() in text:
                score += 1.0
                
        # Normalisation
        return min(score / len(query.keywords), 1.0)
        
    def _calculate_panini_similarity(self, paper_data: Dict) -> float:
        """Calcule similarité avec approche PaniniFS"""
        title = paper_data.get('title', '').lower()
        abstract = paper_data.get('abstract', '').lower()
        text = f"{title} {abstract}"
        
        panini_indicators = [
            'panini', 'sanskrit', 'grammar', 'dependency',
            'semantic', 'compression', 'filesystem', 'linguistic',
            'meaning-text', 'mel\'čuk', 'lexical functions'
        ]
        
        score = 0.0
        for indicator in panini_indicators:
            if indicator in text:
                score += 1.0
                
        return min(score / len(panini_indicators), 1.0)
        
    def _deduplicate_papers(self, papers: List[TheoreticalPaper]) -> List[TheoreticalPaper]:
        """Supprime doublons par titre"""
        seen_titles = set()
        unique_papers = []
        
        for paper in papers:
            title_key = paper.title.lower().strip()
            if title_key not in seen_titles and title_key:
                seen_titles.add(title_key)
                unique_papers.append(paper)
                
        return unique_papers
        
    async def _analyze_cross_references(self):
        """Analyse croisée des références trouvées"""
        print("\n🔄 Analyse croisée des références...")
        
        # Groupement par domaine
        domain_papers = {}
        for paper in self.findings_db:
            # Simple domain inference from keywords
            domain = self._infer_domain(paper)
            if domain not in domain_papers:
                domain_papers[domain] = []
            domain_papers[domain].append(paper)
            
        # Recherche connections inter-domaines
        cross_refs = []
        for d1, papers1 in domain_papers.items():
            for d2, papers2 in domain_papers.items():
                if d1 != d2:
                    connections = self._find_connections(papers1, papers2)
                    if connections:
                        cross_refs.append({
                            'domain1': d1,
                            'domain2': d2, 
                            'connections': connections
                        })
                        
        self.cross_references = cross_refs
        
    def _infer_domain(self, paper: TheoreticalPaper) -> str:
        """Infère le domaine d'un article"""
        text = f"{paper.title} {paper.abstract}".lower()
        
        if any(word in text for word in ['panini', 'sanskrit', 'grammar']):
            return 'panini_grammar'
        elif any(word in text for word in ['mel\'čuk', 'meaning-text', 'mtt']):
            return 'melcuk_theory'
        elif any(word in text for word in ['compression', 'encoding']):
            return 'semantic_compression'
        elif any(word in text for word in ['agent', 'autonomous']):
            return 'autonomous_agents'
        else:
            return 'computational_linguistics'
            
    def _find_connections(self, papers1: List[TheoreticalPaper], papers2: List[TheoreticalPaper]) -> List[Dict]:
        """Trouve connections entre deux groupes d'articles"""
        connections = []
        
        for p1 in papers1:
            for p2 in papers2:
                # Similarité par auteurs communs
                common_authors = set(p1.authors) & set(p2.authors)
                if common_authors:
                    connections.append({
                        'type': 'common_authors',
                        'paper1': p1.title,
                        'paper2': p2.title,
                        'authors': list(common_authors)
                    })
                    
                # Similarité sémantique (simple)
                semantic_sim = self._simple_semantic_similarity(p1, p2)
                if semantic_sim > 0.3:
                    connections.append({
                        'type': 'semantic_similarity',
                        'paper1': p1.title,
                        'paper2': p2.title,
                        'similarity': semantic_sim
                    })
                    
        return connections
        
    def _simple_semantic_similarity(self, p1: TheoreticalPaper, p2: TheoreticalPaper) -> float:
        """Similarité sémantique simple entre deux articles"""
        text1 = f"{p1.title} {p1.abstract}".lower().split()
        text2 = f"{p2.title} {p2.abstract}".lower().split()
        
        words1 = set(text1)
        words2 = set(text2)
        
        if not words1 or not words2:
            return 0.0
            
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union)
        
    async def _evaluate_originality(self):
        """Évalue l'originalité de l'approche PaniniFS"""
        print("\n🎯 Évaluation originalité PaniniFS...")
        
        # Recherche travaux similaires
        similar_works = [p for p in self.findings_db if p.similarity_to_panini > 0.3]
        
        self.originality_assessment = {
            'similar_works_count': len(similar_works),
            'highest_similarity': max([p.similarity_to_panini for p in self.findings_db] + [0]),
            'unique_aspects': self._identify_unique_aspects(similar_works),
            'potential_predecessors': self._identify_predecessors(similar_works),
            'novelty_score': self._calculate_novelty_score(similar_works)
        }
        
    def _identify_unique_aspects(self, similar_works: List[TheoreticalPaper]) -> List[str]:
        """Identifie aspects uniques de PaniniFS"""
        panini_features = {
            'semantic_filesystem', 'panini_grammar_compression',
            'mel\'čuk_implementation', 'autonomous_linguistic_agents',
            'distributed_semantic_storage'
        }
        
        found_features = set()
        for work in similar_works:
            text = f"{work.title} {work.abstract}".lower()
            for feature in panini_features:
                if feature.replace('_', ' ') in text:
                    found_features.add(feature)
                    
        unique_aspects = list(panini_features - found_features)
        return unique_aspects
        
    def _identify_predecessors(self, similar_works: List[TheoreticalPaper]) -> List[Dict]:
        """Identifie travaux précurseurs potentiels"""
        predecessors = []
        
        for work in similar_works:
            if work.similarity_to_panini > 0.5:
                predecessors.append({
                    'title': work.title,
                    'authors': work.authors,
                    'year': work.year,
                    'similarity': work.similarity_to_panini,
                    'type': 'strong_similarity'
                })
            elif work.similarity_to_panini > 0.3:
                predecessors.append({
                    'title': work.title,
                    'authors': work.authors,
                    'year': work.year,
                    'similarity': work.similarity_to_panini,
                    'type': 'moderate_similarity'
                })
                
        return sorted(predecessors, key=lambda x: x['similarity'], reverse=True)
        
    def _calculate_novelty_score(self, similar_works: List[TheoreticalPaper]) -> float:
        """Calcule score de nouveauté (0-1)"""
        if not similar_works:
            return 1.0
            
        max_similarity = max([w.similarity_to_panini for w in similar_works])
        novelty = 1.0 - max_similarity
        
        # Bonus pour combinaison unique de concepts
        unique_combination_bonus = 0.2 if len(self.originality_assessment.get('unique_aspects', [])) > 3 else 0
        
        return min(novelty + unique_combination_bonus, 1.0)
        
    async def _generate_theoretical_report(self):
        """Génère rapport théorique complet"""
        print("\n📊 Génération rapport théorique...")
        
        report = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'research_summary': {
                'total_papers_found': len(self.findings_db),
                'domains_covered': len(self.research_domains),
                'apis_used': list(self.research_apis.keys()),
                'research_duration': self._calculate_research_duration()
            },
            'domain_analysis': self._analyze_domains(),
            'key_findings': self._extract_key_findings(),
            'theoretical_gaps': self._identify_theoretical_gaps(),
            'validation_opportunities': self._identify_validation_opportunities(),
            'contradiction_alerts': self._identify_contradictions(),
            'originality_assessment': getattr(self, 'originality_assessment', {}),
            'cross_references': getattr(self, 'cross_references', []),
            'recommendations': self._generate_recommendations(),
            'next_research_priorities': self._define_next_priorities()
        }
        
        # Sauvegarde rapport
        report_path = f"/home/stephane/GitHub/PaniniFS-1/theoretical_research_report_{self.session_id}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        # Rapport humain-lisible
        self._generate_human_readable_report(report)
        
        print(f"✅ Rapport sauvegardé: {report_path}")
        
    def _analyze_domains(self) -> Dict:
        """Analyse par domaine de recherche"""
        domain_stats = {}
        
        for domain in self.research_domains:
            domain_papers = [p for p in self.findings_db if self._infer_domain(p) == domain]
            
            domain_stats[domain] = {
                'papers_found': len(domain_papers),
                'avg_relevance': sum([p.relevance_score for p in domain_papers]) / len(domain_papers) if domain_papers else 0,
                'recent_papers': len([p for p in domain_papers if p.year >= 2020]),
                'high_relevance_papers': len([p for p in domain_papers if p.relevance_score > 0.7]),
                'top_papers': sorted(domain_papers, key=lambda x: x.relevance_score, reverse=True)[:5]
            }
            
        return domain_stats
        
    def _extract_key_findings(self) -> List[Dict]:
        """Extrait findings clés"""
        # Top papers par pertinence
        top_papers = sorted(self.findings_db, key=lambda x: x.relevance_score, reverse=True)[:10]
        
        key_findings = []
        for paper in top_papers:
            key_findings.append({
                'title': paper.title,
                'authors': paper.authors,
                'year': paper.year,
                'relevance_score': paper.relevance_score,
                'similarity_to_panini': paper.similarity_to_panini,
                'key_contribution': self._extract_key_contribution(paper),
                'implications_for_panini': self._analyze_implications(paper)
            })
            
        return key_findings
        
    def _extract_key_contribution(self, paper: TheoreticalPaper) -> str:
        """Extrait contribution clé d'un article"""
        # Simple extraction from abstract
        abstract = paper.abstract.lower()
        
        if 'novel' in abstract or 'new' in abstract:
            return "Novel approach or method"
        elif 'improve' in abstract or 'enhance' in abstract:
            return "Improvement of existing methods"
        elif 'analysis' in abstract or 'study' in abstract:
            return "Analytical or empirical study"
        else:
            return "Theoretical contribution"
            
    def _analyze_implications(self, paper: TheoreticalPaper) -> str:
        """Analyse implications pour PaniniFS"""
        text = f"{paper.title} {paper.abstract}".lower()
        
        implications = []
        
        if any(word in text for word in ['compression', 'encoding']):
            implications.append("Potential compression algorithm improvement")
        if any(word in text for word in ['grammar', 'linguistic']):
            implications.append("Linguistic foundation enhancement")
        if any(word in text for word in ['semantic', 'meaning']):
            implications.append("Semantic processing optimization")
        if any(word in text for word in ['filesystem', 'storage']):
            implications.append("Storage architecture insights")
            
        return "; ".join(implications) if implications else "General theoretical relevance"
        
    def _identify_theoretical_gaps(self) -> List[Dict]:
        """Identifie gaps théoriques à partir de la recherche"""
        gaps = []
        
        # Gap 1: Peu de travaux sur compression sémantique + filesystem
        compression_fs_papers = [p for p in self.findings_db 
                                if 'compression' in f"{p.title} {p.abstract}".lower() 
                                and 'filesystem' in f"{p.title} {p.abstract}".lower()]
        
        if len(compression_fs_papers) < 5:
            gaps.append({
                'gap_type': 'semantic_filesystem_compression',
                'severity': 'HIGH',
                'description': 'Très peu de travaux sur compression sémantique appliquée aux filesystems',
                'papers_found': len(compression_fs_papers),
                'opportunity': 'Domaine novateur avec peu de concurrence'
            })
            
        # Gap 2: Panini grammar + computational applications
        panini_comp_papers = [p for p in self.findings_db 
                            if 'panini' in f"{p.title} {p.abstract}".lower() 
                            and any(word in f"{p.title} {p.abstract}".lower() 
                                  for word in ['computational', 'algorithm', 'implementation'])]
        
        if len(panini_comp_papers) < 10:
            gaps.append({
                'gap_type': 'panini_computational_applications',
                'severity': 'MEDIUM',
                'description': 'Applications computationnelles de la grammaire Panini sous-exploitées',
                'papers_found': len(panini_comp_papers),
                'opportunity': 'Pont entre linguistique historique et informatique moderne'
            })
            
        return gaps
        
    def _identify_validation_opportunities(self) -> List[Dict]:
        """Identifie opportunités de validation"""
        validations = []
        
        # Recherche papers supportant approche PaniniFS
        supportive_papers = [p for p in self.findings_db if p.similarity_to_panini > 0.4]
        
        for paper in supportive_papers:
            validations.append({
                'paper_title': paper.title,
                'validation_type': self._categorize_validation(paper),
                'strength': 'STRONG' if paper.similarity_to_panini > 0.6 else 'MODERATE',
                'citation_potential': 'HIGH' if paper.year >= 2015 else 'MEDIUM'
            })
            
        return validations
        
    def _categorize_validation(self, paper: TheoreticalPaper) -> str:
        """Catégorise type de validation offerte par un paper"""
        text = f"{paper.title} {paper.abstract}".lower()
        
        if 'compression' in text and 'semantic' in text:
            return 'semantic_compression_validation'
        elif 'grammar' in text and 'computational' in text:
            return 'computational_grammar_validation'
        elif 'filesystem' in text and 'linguistic' in text:
            return 'linguistic_filesystem_validation'
        else:
            return 'general_theoretical_support'
            
    def _identify_contradictions(self) -> List[Dict]:
        """Identifie contradictions potentielles"""
        contradictions = []
        
        # Recherche papers contradictoires
        for paper in self.findings_db:
            text = f"{paper.title} {paper.abstract}".lower()
            
            # Contradiction 1: Compression sémantique impossible/inefficace
            if any(phrase in text for phrase in ['semantic compression', 'meaningless', 'ineffective']):
                if 'impossible' in text or 'ineffective' in text:
                    contradictions.append({
                        'paper_title': paper.title,
                        'contradiction_type': 'semantic_compression_skepticism',
                        'severity': 'HIGH',
                        'description': 'Remet en question efficacité compression sémantique'
                    })
                    
            # Contradiction 2: Grammaire Panini trop ancienne/inadaptée
            if 'panini' in text and any(word in text for word in ['outdated', 'ancient', 'inadequate']):
                contradictions.append({
                    'paper_title': paper.title,
                    'contradiction_type': 'panini_relevance_question',
                    'severity': 'MEDIUM', 
                    'description': 'Questionne pertinence grammaire Panini pour informatique moderne'
                })
                
        return contradictions
        
    def _generate_recommendations(self) -> List[Dict]:
        """Génère recommandations basées sur recherche"""
        recommendations = []
        
        # Rec 1: Papers à citer prioritairement
        top_citation_papers = sorted(self.findings_db, 
                                   key=lambda x: (x.relevance_score + x.similarity_to_panini) / 2, 
                                   reverse=True)[:10]
        
        recommendations.append({
            'type': 'priority_citations',
            'description': 'Articles à citer prioritairement pour appuyer approche PaniniFS',
            'action': 'Intégrer citations dans publications et documentation',
            'papers': [{'title': p.title, 'authors': p.authors, 'year': p.year} for p in top_citation_papers]
        })
        
        # Rec 2: Domaines à approfondir
        weak_domains = [domain for domain, config in self.research_domains.items() 
                       if len([p for p in self.findings_db if self._infer_domain(p) == domain]) < 10]
        
        if weak_domains:
            recommendations.append({
                'type': 'research_deepening',
                'description': 'Domaines nécessitant recherche approfondie',
                'action': 'Élargir recherche bibliographique dans ces domaines',
                'domains': weak_domains
            })
            
        # Rec 3: Collaborations potentielles
        frequent_authors = self._find_frequent_authors()
        if frequent_authors:
            recommendations.append({
                'type': 'collaboration_opportunities',
                'description': 'Auteurs apparaissant fréquemment - collaborations potentielles',
                'action': 'Contacter pour échanges ou collaborations',
                'authors': frequent_authors
            })
            
        return recommendations
        
    def _find_frequent_authors(self) -> List[Dict]:
        """Trouve auteurs fréquents dans les résultats"""
        author_count = {}
        
        for paper in self.findings_db:
            for author in paper.authors:
                if author not in author_count:
                    author_count[author] = 0
                author_count[author] += 1
                
        # Auteurs avec 3+ papers
        frequent = [{'name': author, 'papers_count': count} 
                   for author, count in author_count.items() if count >= 3]
        
        return sorted(frequent, key=lambda x: x['papers_count'], reverse=True)[:10]
        
    def _define_next_priorities(self) -> List[Dict]:
        """Définit priorités recherche future"""
        priorities = []
        
        # Basé sur gaps identifiés
        for gap in self._identify_theoretical_gaps():
            priorities.append({
                'priority': 'HIGH' if gap['severity'] == 'HIGH' else 'MEDIUM',
                'focus': gap['gap_type'],
                'action': f"Recherche approfondie: {gap['description']}",
                'timeline': '1-2 weeks' if gap['severity'] == 'HIGH' else '1 month'
            })
            
        # Suivi des développements récents
        priorities.append({
            'priority': 'ONGOING',
            'focus': 'recent_developments',
            'action': 'Surveillance continue publications récentes dans domaines clés',
            'timeline': 'Weekly monitoring'
        })
        
        return priorities
        
    def _generate_human_readable_report(self, report: Dict):
        """Génère rapport lisible pour humains"""
        readable_path = f"/home/stephane/GitHub/PaniniFS-1/theoretical_research_summary_{self.session_id}.md"
        
        with open(readable_path, 'w', encoding='utf-8') as f:
            f.write(f"# 🔬 RAPPORT RECHERCHE THÉORIQUE - {self.session_id}\n\n")
            f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## 📊 RÉSUMÉ EXÉCUTIF\n\n")
            f.write(f"- **Articles analysés**: {report['research_summary']['total_papers_found']}\n")
            f.write(f"- **Domaines couverts**: {report['research_summary']['domains_covered']}\n")
            f.write(f"- **Score originalité**: {report['originality_assessment']['novelty_score']:.2f}/1.0\n\n")
            
            f.write("## 🎯 PRINCIPALES DÉCOUVERTES\n\n")
            for finding in report['key_findings'][:5]:
                f.write(f"### {finding['title']}\n")
                f.write(f"**Auteurs**: {', '.join(finding['authors'])}\n")
                f.write(f"**Année**: {finding['year']}\n")
                f.write(f"**Pertinence**: {finding['relevance_score']:.2f}\n")
                f.write(f"**Similarité PaniniFS**: {finding['similarity_to_panini']:.2f}\n")
                f.write(f"**Implications**: {finding['implications_for_panini']}\n\n")
                
            f.write("## ⚠️ GAPS THÉORIQUES IDENTIFIÉS\n\n")
            for gap in report['theoretical_gaps']:
                f.write(f"### {gap['gap_type']} (Sévérité: {gap['severity']})\n")
                f.write(f"{gap['description']}\n")
                f.write(f"**Papers trouvés**: {gap['papers_found']}\n")
                f.write(f"**Opportunité**: {gap['opportunity']}\n\n")
                
            f.write("## 💡 RECOMMANDATIONS\n\n")
            for rec in report['recommendations']:
                f.write(f"### {rec['type']}\n")
                f.write(f"{rec['description']}\n")
                f.write(f"**Action**: {rec['action']}\n\n")
                
            f.write("## 🚀 PROCHAINES PRIORITÉS\n\n")
            for priority in report['next_research_priorities']:
                f.write(f"- **{priority['focus']}** ({priority['priority']}): {priority['action']}\n")
                
        print(f"✅ Rapport lisible sauvegardé: {readable_path}")
        
    def _calculate_research_duration(self) -> str:
        """Calcule durée de recherche"""
        if self.research_log:
            start_time = datetime.fromisoformat(self.research_log[0]['timestamp'])
            end_time = datetime.fromisoformat(self.research_log[-1]['timestamp'])
            duration = end_time - start_time
            return f"{duration.total_seconds():.0f} seconds"
        return "Unknown"

async def main():
    """Fonction principale - exécution autonome"""
    agent = TheoreticalResearchAgent()
    await agent.autonomous_research_cycle()

if __name__ == "__main__":
    print("🔬 DÉMARRAGE AGENT RECHERCHE THÉORIQUE AUTONOME")
    print("=" * 50)
    asyncio.run(main())
