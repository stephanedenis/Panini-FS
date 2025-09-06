#!/usr/bin/env python3
"""
Script d'affichage des recommandations
Affiche les recommandations d'analyse de manière lisible
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def load_analysis_report(report_path: str = None):
    """Charge le rapport d'analyse"""
    if not report_path:
        scripts_dir = Path(__file__).parent
        report_path = scripts_dir / "autonomous_analysis_report.json"
    
    if not Path(report_path).exists():
        print(f"❌ Rapport non trouvé: {report_path}")
        return None
    
    with open(report_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def display_executive_summary(report):
    """Affiche le résumé exécutif"""
    summary = report.get('executive_summary', {})
    
    print("📈 RÉSUMÉ EXÉCUTIF")
    print("=" * 50)
    print(f"📊 Total des recommandations: {summary.get('total_recommendations', 0)}")
    print(f"🔴 Priorité haute: {summary.get('high_priority_count', 0)}")
    print(f"🟡 Priorité moyenne: {summary.get('medium_priority_count', 0)}")
    print(f"🟢 Priorité basse: {summary.get('low_priority_count', 0)}")
    print(f"⏱️  Effort total estimé: {summary.get('estimated_total_effort', 'Non calculé')}")
    print()
    
    insights = summary.get('key_insights', [])
    if insights:
        print("🎯 INSIGHTS CLÉS:")
        for insight in insights:
            print(f"  • {insight}")
        print()

def display_recommendations(report, priority_filter=None, category_filter=None):
    """Affiche les recommandations avec filtres optionnels"""
    recommendations = report.get('recommendations', [])
    
    # Filtrer par priorité
    if priority_filter:
        recommendations = [r for r in recommendations if r.get('priority') == priority_filter]
    
    # Filtrer par catégorie
    if category_filter:
        recommendations = [r for r in recommendations if r.get('category') == category_filter]
    
    if not recommendations:
        print("Aucune recommandation trouvée avec ces filtres.")
        return
    
    # Symboles pour les priorités
    priority_symbols = {
        'high': '🔴',
        'medium': '🟡',
        'low': '🟢'
    }
    
    # Symboles pour les catégories
    category_symbols = {
        'priority': '⭐',
        'feature': '🚀',
        'testing': '🧪',
        'architecture': '🏗️',
        'language': '⚙️',
        'tooling': '🔧'
    }
    
    for i, rec in enumerate(recommendations, 1):
        priority_sym = priority_symbols.get(rec.get('priority', ''), '⚪')
        category_sym = category_symbols.get(rec.get('category', ''), '📋')
        
        print(f"{category_sym} {priority_sym} {rec.get('title', 'Sans titre')}")
        print(f"   Catégorie: {rec.get('category', 'Non spécifiée')}")
        print(f"   Priorité: {rec.get('priority', 'Non spécifiée')}")
        print(f"   Effort estimé: {rec.get('estimated_effort', 'Non spécifié')}")
        print(f"   💡 {rec.get('description', 'Pas de description')}")
        print(f"   🔍 Justification: {rec.get('rationale', 'Pas de justification')}")
        
        steps = rec.get('implementation_steps', [])
        if steps:
            print("   📝 Étapes d'implémentation:")
            for step in steps:
                print(f"      • {step}")
        
        sample_files = rec.get('sample_files', [])
        if sample_files:
            print(f"   📁 Fichiers d'exemple: {', '.join(sample_files[:3])}")
            if len(sample_files) > 3:
                print(f"      ... et {len(sample_files) - 3} autres")
        
        print()

def display_next_actions(report):
    """Affiche les prochaines actions recommandées"""
    next_actions = report.get('next_actions', [])
    
    if next_actions:
        print("⚡ PROCHAINES ACTIONS RECOMMANDÉES")
        print("=" * 50)
        for i, action in enumerate(next_actions, 1):
            print(f"{i}. {action}")
        print()

def display_risk_assessment(report):
    """Affiche l'évaluation des risques"""
    risks = report.get('risk_assessment', {})
    
    if risks:
        print("⚠️  ÉVALUATION DES RISQUES")
        print("=" * 50)
        
        tech_risks = risks.get('technical_risks', [])
        if tech_risks:
            print("🔧 Risques techniques:")
            for risk in tech_risks:
                print(f"  • {risk}")
            print()
        
        project_risks = risks.get('project_risks', [])
        if project_risks:
            print("📋 Risques projet:")
            for risk in project_risks:
                print(f"  • {risk}")
            print()
        
        mitigations = risks.get('mitigation_strategies', [])
        if mitigations:
            print("🛡️  Stratégies d'atténuation:")
            for mitigation in mitigations:
                print(f"  • {mitigation}")
            print()

def display_preferences_summary(report):
    """Affiche un résumé des préférences analysées"""
    preferences = report.get('preferences_analysis', {})
    summary = preferences.get('summary', {})
    
    if summary:
        print("👤 RÉSUMÉ DES PRÉFÉRENCES DÉVELOPPEUR")
        print("=" * 50)
        
        if summary.get('most_used_language'):
            print(f"🗣️  Langage principal: {summary['most_used_language']}")
        
        if summary.get('most_used_framework'):
            print(f"🏗️  Framework principal: {summary['most_used_framework']}")
        
        if summary.get('preferred_architecture'):
            print(f"🎨 Architecture préférée: {summary['preferred_architecture']}")
        
        print(f"📁 Projets analysés: {summary.get('total_projects', 0)}")
        print()

def main():
    """Fonction principale"""
    # Parser les arguments de ligne de commande
    priority_filter = None
    category_filter = None
    show_all = True
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ['high', 'medium', 'low']:
            priority_filter = sys.argv[1]
            show_all = False
        elif sys.argv[1] in ['feature', 'testing', 'architecture', 'language', 'tooling', 'priority']:
            category_filter = sys.argv[1]
            show_all = False
        elif sys.argv[1] == 'help':
            print("Usage: python3 display_recommendations.py [high|medium|low|feature|testing|architecture|language|tooling|priority]")
            print("Exemples:")
            print("  python3 display_recommendations.py high        # Recommandations haute priorité")
            print("  python3 display_recommendations.py feature     # Recommandations de fonctionnalités")
            print("  python3 display_recommendations.py             # Toutes les recommandations")
            return
    
    # Charger le rapport
    report = load_analysis_report()
    if not report:
        return
    
    print("🤖 RAPPORT D'ANALYSE AUTONOME PANINI-FS")
    print("=" * 70)
    
    # Métadonnées
    metadata = report.get('analysis_metadata', {})
    if metadata.get('timestamp'):
        timestamp = metadata['timestamp']
        print(f"📅 Généré le: {timestamp}")
    print()
    
    # Afficher les sections
    if show_all:
        display_executive_summary(report)
        display_preferences_summary(report)
        display_next_actions(report)
        print("🎯 RECOMMANDATIONS DÉTAILLÉES")
        print("=" * 50)
    
    display_recommendations(report, priority_filter, category_filter)
    
    if show_all:
        display_risk_assessment(report)
        
        print("💡 AIDE")
        print("=" * 50)
        print("Pour voir seulement les recommandations haute priorité:")
        print("  python3 display_recommendations.py high")
        print()
        print("Pour voir seulement les recommandations de test:")
        print("  python3 display_recommendations.py testing")

if __name__ == "__main__":
    main()
