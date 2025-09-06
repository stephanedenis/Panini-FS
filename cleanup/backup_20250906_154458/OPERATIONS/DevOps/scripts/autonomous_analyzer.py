#!/usr/bin/env python3
"""
Script d'orchestration pour l'analyse autonome
Combine l'analyse des préférences et la collecte d'échantillons
pour fournir des recommandations d'amélioration du projet
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

# Importer les modules d'analyse
sys.path.append(str(Path(__file__).parent))
from analyze_preferences import PreferencesAnalyzer
from collect_samples import SampleCollector

@dataclass
class ProjectRecommendation:
    """Recommandation pour améliorer le projet"""
    category: str
    priority: str  # 'high', 'medium', 'low'
    title: str
    description: str
    rationale: str
    implementation_steps: List[str]
    estimated_effort: str
    sample_files: List[str]

class AutonomousAnalyzer:
    def __init__(self):
        self.preferences_analyzer = PreferencesAnalyzer()
        self.sample_collector = SampleCollector()
        self.recommendations = []
        
    def run_full_analysis(self):
        """Lance une analyse complète et génère des recommandations"""
        print("🚀 Démarrage de l'analyse autonome...")
        
        # Étape 1: Analyser les préférences
        print("\n📊 Analyse des préférences de développement...")
        self.preferences_analyzer.analyze_markdown_files()
        self.preferences_analyzer.analyze_config_files()
        self.preferences_analyzer.compute_global_patterns()
        preferences_report = self.preferences_analyzer.generate_report()
        
        # Étape 2: Collecter les échantillons
        print("\n📁 Collecte des échantillons de fichiers...")
        if self.sample_collector.pensine_path.exists():
            self.sample_collector.collect_samples()
        samples_report = self.sample_collector.generate_report()
        
        # Étape 3: Générer des recommandations
        print("\n🧠 Génération des recommandations...")
        self._generate_recommendations(preferences_report, samples_report)
        
        # Étape 4: Générer le rapport final
        print("\n📋 Génération du rapport final...")
        final_report = self._generate_final_report(preferences_report, samples_report)
        
        return final_report
    
    def _generate_recommendations(self, preferences: Dict, samples: Dict):
        """Génère des recommandations basées sur l'analyse"""
        
        # Recommandations basées sur les préférences
        self._analyze_architecture_patterns(preferences)
        self._analyze_language_usage(preferences)
        self._analyze_testing_gaps(preferences)
        
        # Recommandations basées sur les échantillons
        self._analyze_sample_diversity(samples)
        self._analyze_file_types_coverage(samples)
        self._analyze_test_scenarios(samples)
        
        # Recommandations pour PaniniFS spécifiquement
        self._generate_panini_fs_recommendations(preferences, samples)
    
    def _analyze_architecture_patterns(self, preferences: Dict):
        """Analyse les patterns d'architecture utilisés"""
        patterns = preferences.get('global_patterns', {}).get('architecture_patterns', {})
        
        if 'async' in patterns and patterns['async'] > 1:
            self.recommendations.append(ProjectRecommendation(
                category='architecture',
                priority='medium',
                title='Optimisation des patterns asynchrones',
                description='Vous utilisez fréquemment des patterns asynchrones. PaniniFS pourrait bénéficier d\'optimisations spécifiques.',
                rationale='Détection de l\'utilisation récurrente de Tokio et patterns async/await dans vos projets',
                implementation_steps=[
                    'Audit des performances des opérations async actuelles',
                    'Implémentation de pools de connexions pour les opérations I/O',
                    'Optimisation des verrous (Mutex) pour réduire la contention',
                    'Tests de charge avec différents patterns de concurrence'
                ],
                estimated_effort='1-2 semaines',
                sample_files=[]
            ))
        
        if 'microservices' in patterns:
            self.recommendations.append(ProjectRecommendation(
                category='architecture',
                priority='low',
                title='Architecture microservices pour PaniniFS',
                description='Considérer une architecture modulaire pour PaniniFS basée sur vos préférences microservices',
                rationale='Votre expérience avec les microservices pourrait être appliquée à PaniniFS',
                implementation_steps=[
                    'Identifier les modules indépendants dans PaniniFS',
                    'Définir les interfaces entre modules',
                    'Implémenter une communication inter-modules',
                    'Tests d\'intégration modulaire'
                ],
                estimated_effort='3-4 semaines',
                sample_files=[]
            ))
    
    def _analyze_language_usage(self, preferences: Dict):
        """Analyse l'utilisation des langages"""
        languages = preferences.get('global_patterns', {}).get('languages', {})
        
        if 'rust' in languages and languages['rust'] > 2:
            self.recommendations.append(ProjectRecommendation(
                category='language',
                priority='high',
                title='Optimisations Rust avancées',
                description='Exploiter davantage les fonctionnalités avancées de Rust pour PaniniFS',
                rationale='Votre expertise en Rust peut être mieux exploitée',
                implementation_steps=[
                    'Audit du code pour identifier les allocations inutiles',
                    'Utilisation de `Cow` pour réduire les clones',
                    'Implémentation de traits personnalisés pour les opérations communes',
                    'Optimisation des structures de données avec `Box`, `Rc`, `Arc`'
                ],
                estimated_effort='2-3 semaines',
                sample_files=[]
            ))
        
        if 'python' in languages:
            self.recommendations.append(ProjectRecommendation(
                category='tooling',
                priority='medium',
                title='Outils Python pour PaniniFS',
                description='Développer des outils Python pour faciliter l\'utilisation de PaniniFS',
                rationale='Votre expérience Python peut créer des outils complémentaires',
                implementation_steps=[
                    'Créer un client Python pour PaniniFS',
                    'Développer des scripts d\'analyse et de migration',
                    'Implémenter des tests d\'intégration en Python',
                    'Créer des outils de visualisation des données'
                ],
                estimated_effort='1-2 semaines',
                sample_files=[]
            ))
    
    def _analyze_testing_gaps(self, preferences: Dict):
        """Identifie les lacunes dans les tests"""
        self.recommendations.append(ProjectRecommendation(
            category='testing',
            priority='high',
            title='Stratégie de tests complète',
            description='Développer une stratégie de tests robuste pour PaniniFS',
            rationale='Tests critiques pour un système de fichiers',
            implementation_steps=[
                'Tests unitaires pour tous les modules core',
                'Tests d\'intégration pour les opérations FUSE',
                'Tests de performance et de charge',
                'Tests de récupération après panne',
                'Tests de compatibilité multi-plateforme'
            ],
            estimated_effort='3-4 semaines',
            sample_files=[]
        ))
    
    def _analyze_sample_diversity(self, samples: Dict):
        """Analyse la diversité des échantillons"""
        file_types = samples.get('statistics', {}).get('file_types', {})
        
        if len(file_types) > 10:
            self.recommendations.append(ProjectRecommendation(
                category='testing',
                priority='medium',
                title='Tests avec diversité de fichiers',
                description='Exploiter la diversité des types de fichiers pour des tests réalistes',
                rationale=f'Détection de {len(file_types)} types de fichiers différents',
                implementation_steps=[
                    'Créer des tests avec chaque type de fichier majeur',
                    'Tester les performances selon les types de fichiers',
                    'Valider la préservation des métadonnées',
                    'Tests de recherche sémantique sur différents formats'
                ],
                estimated_effort='1-2 semaines',
                sample_files=list(file_types.keys())[:10]
            ))
    
    def _analyze_file_types_coverage(self, samples: Dict):
        """Analyse la couverture des types de fichiers"""
        scenarios = samples.get('test_scenarios', [])
        
        if scenarios:
            self.recommendations.append(ProjectRecommendation(
                category='testing',
                priority='medium',
                title='Scénarios de test automatisés',
                description='Implémenter des tests automatisés basés sur les scénarios identifiés',
                rationale=f'Génération de {len(scenarios)} scénarios de test potentiels',
                implementation_steps=[
                    'Automatiser les scénarios de test générés',
                    'Créer des benchmarks par type de fichier',
                    'Implémenter des tests de régression',
                    'Valider les opérations sur différentes tailles de fichiers'
                ],
                estimated_effort='2-3 semaines',
                sample_files=[]
            ))
    
    def _analyze_test_scenarios(self, samples: Dict):
        """Analyse les scénarios de test possibles"""
        recommendations = samples.get('recommended_test_files', {})
        
        if recommendations.get('code_files_only'):
            self.recommendations.append(ProjectRecommendation(
                category='feature',
                priority='medium',
                title='Indexation intelligente du code source',
                description='Implémenter une indexation spécialisée pour les fichiers de code',
                rationale='Nombreux fichiers de code source disponibles pour les tests',
                implementation_steps=[
                    'Parser les fichiers de code pour extraire les symboles',
                    'Créer un index des fonctions, classes, et variables',
                    'Implémenter la recherche par signature de fonction',
                    'Ajouter la navigation dans le code (go-to-definition)'
                ],
                estimated_effort='4-5 semaines',
                sample_files=recommendations['code_files_only'][:5]
            ))
    
    def _generate_panini_fs_recommendations(self, preferences: Dict, samples: Dict):
        """Génère des recommandations spécifiques à PaniniFS"""
        
        # Recommandation basée sur l'état actuel du projet
        self.recommendations.append(ProjectRecommendation(
            category='priority',
            priority='high',
            title='Finalisation du système de stockage',
            description='Compléter l\'implémentation du système de stockage avec Sled',
            rationale='Base nécessaire pour toutes les autres fonctionnalités',
            implementation_steps=[
                'Finaliser les tests unitaires pour GitStorage',
                'Implémenter les opérations de recherche manquantes',
                'Ajouter la gestion des transactions',
                'Optimiser les performances des opérations batch',
                'Documenter l\'API de stockage'
            ],
            estimated_effort='2-3 semaines',
            sample_files=[]
        ))
        
        self.recommendations.append(ProjectRecommendation(
            category='feature',
            priority='high',
            title='Interface FUSE fonctionnelle',
            description='Implémenter une interface FUSE basique mais fonctionnelle',
            rationale='Objectif principal du projet PaniniFS',
            implementation_steps=[
                'Implémenter les opérations FUSE de base (read, write, list)',
                'Ajouter la gestion des métadonnées étendues',
                'Implémenter la recherche sémantique via des répertoires virtuels',
                'Tests avec différents types de fichiers',
                'Optimisation des performances I/O'
            ],
            estimated_effort='4-6 semaines',
            sample_files=[]
        ))
        
        self.recommendations.append(ProjectRecommendation(
            category='architecture',
            priority='medium',
            title='Architecture modulaire extensible',
            description='Refactorer l\'architecture pour faciliter l\'ajout de nouvelles fonctionnalités',
            rationale='Faciliter l\'évolution future du projet',
            implementation_steps=[
                'Définir des traits pour les modules extensibles',
                'Implémenter un système de plugins',
                'Séparer les couches (storage, semantic, vfs)',
                'Créer des interfaces standardisées',
                'Documentation de l\'architecture'
            ],
            estimated_effort='3-4 semaines',
            sample_files=[]
        ))
    
    def _generate_final_report(self, preferences: Dict, samples: Dict) -> Dict[str, Any]:
        """Génère le rapport final avec toutes les analyses et recommandations"""
        
        # Trier les recommandations par priorité
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        sorted_recommendations = sorted(
            self.recommendations, 
            key=lambda x: (priority_order.get(x.priority, 3), x.category)
        )
        
        report = {
            'analysis_metadata': {
                'timestamp': datetime.now().isoformat(),
                'analyzer_version': '1.0.0',
                'preferences_projects_analyzed': len(preferences.get('projects', {})),
                'sample_files_analyzed': len(samples.get('samples', [])),
            },
            'executive_summary': {
                'total_recommendations': len(self.recommendations),
                'high_priority_count': len([r for r in self.recommendations if r.priority == 'high']),
                'medium_priority_count': len([r for r in self.recommendations if r.priority == 'medium']),
                'low_priority_count': len([r for r in self.recommendations if r.priority == 'low']),
                'estimated_total_effort': self._calculate_total_effort(),
                'key_insights': self._generate_key_insights(preferences, samples)
            },
            'preferences_analysis': preferences,
            'samples_analysis': samples,
            'recommendations': [
                {
                    'category': rec.category,
                    'priority': rec.priority,
                    'title': rec.title,
                    'description': rec.description,
                    'rationale': rec.rationale,
                    'implementation_steps': rec.implementation_steps,
                    'estimated_effort': rec.estimated_effort,
                    'sample_files': rec.sample_files
                }
                for rec in sorted_recommendations
            ],
            'next_actions': self._generate_next_actions(),
            'risk_assessment': self._generate_risk_assessment()
        }
        
        return report
    
    def _calculate_total_effort(self) -> str:
        """Calcule l'effort total estimé"""
        # Simplifié - pourrait être plus sophistiqué
        high_count = len([r for r in self.recommendations if r.priority == 'high'])
        medium_count = len([r for r in self.recommendations if r.priority == 'medium'])
        low_count = len([r for r in self.recommendations if r.priority == 'low'])
        
        total_weeks = high_count * 3 + medium_count * 2 + low_count * 1
        return f"{total_weeks}-{total_weeks + 5} semaines"
    
    def _generate_key_insights(self, preferences: Dict, samples: Dict) -> List[str]:
        """Génère les insights clés de l'analyse"""
        insights = []
        
        # Insights sur les préférences
        summary = preferences.get('summary', {})
        if summary.get('most_used_language'):
            insights.append(f"Expertise principale détectée: {summary['most_used_language']}")
        
        if summary.get('preferred_architecture'):
            insights.append(f"Pattern d'architecture préféré: {summary['preferred_architecture']}")
        
        # Insights sur les échantillons
        stats = samples.get('statistics', {})
        if stats.get('file_types'):
            insights.append(f"Diversité des types de fichiers: {len(stats['file_types'])} types détectés")
        
        # Insights spécifiques à PaniniFS
        insights.append("PaniniFS est en phase de développement initial avec un potentiel important")
        insights.append("L'architecture modulaire facilitera l'ajout de fonctionnalités avancées")
        
        return insights
    
    def _generate_next_actions(self) -> List[str]:
        """Génère les prochaines actions recommandées"""
        high_priority = [r for r in self.recommendations if r.priority == 'high']
        
        actions = []
        if high_priority:
            actions.append(f"Prioriser: {high_priority[0].title}")
            actions.append("Mettre en place des tests automatisés complets")
            actions.append("Finaliser l'implémentation du stockage Sled")
            actions.append("Commencer le développement de l'interface FUSE")
        
        actions.append("Planifier les itérations de développement par priorité")
        actions.append("Documenter l'architecture actuelle")
        
        return actions
    
    def _generate_risk_assessment(self) -> Dict[str, Any]:
        """Génère une évaluation des risques"""
        return {
            'technical_risks': [
                "Complexité de l'interface FUSE peut ralentir le développement",
                "Performance des opérations sémantiques sur de gros volumes",
                "Compatibilité multi-plateforme non encore validée"
            ],
            'project_risks': [
                "Scope du projet potentiellement trop ambitieux",
                "Manque de tests d'intégration complets",
                "Documentation utilisateur insuffisante"
            ],
            'mitigation_strategies': [
                "Développement incrémental avec tests à chaque étape",
                "Benchmarks réguliers pour valider les performances",
                "Tests sur différents systèmes d'exploitation",
                "Création d'exemples d'utilisation concrets"
            ]
        }
    
    def save_report(self, output_file: str = "autonomous_analysis_report.json"):
        """Sauvegarde le rapport final"""
        report = self._generate_final_report({}, {})
        
        scripts_dir = Path("/home/stephane/GitHub/PaniniFS-1/scripts/scripts")
        scripts_dir.mkdir(exist_ok=True)
        output_path = scripts_dir / output_file
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"Rapport d'analyse autonome sauvegardé dans {output_path}")
        return output_path

def main():
    """Fonction principale"""
    analyzer = AutonomousAnalyzer()
    
    print("🤖 ANALYSE AUTONOME PANINI-FS")
    print("=" * 50)
    
    try:
        # Lancer l'analyse complète
        final_report = analyzer.run_full_analysis()
        
        # Sauvegarder le rapport
        report_path = analyzer.save_report()
        
        # Afficher le résumé exécutif
        summary = final_report.get('executive_summary', {})
        print(f"\n📈 RÉSUMÉ EXÉCUTIF")
        print(f"Recommandations générées: {summary.get('total_recommendations', 0)}")
        print(f"Priorité haute: {summary.get('high_priority_count', 0)}")
        print(f"Priorité moyenne: {summary.get('medium_priority_count', 0)}")
        print(f"Effort total estimé: {summary.get('estimated_total_effort', 'Non calculé')}")
        
        print(f"\n🎯 INSIGHTS CLÉS:")
        for insight in summary.get('key_insights', [])[:3]:
            print(f"  • {insight}")
        
        print(f"\n⚡ PROCHAINES ACTIONS:")
        for action in summary.get('next_actions', [])[:3]:
            print(f"  • {action}")
        
        print(f"\n📊 Rapport détaillé: {report_path}")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
