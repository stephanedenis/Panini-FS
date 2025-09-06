#!/usr/bin/env python3
"""
Tableau de Bord PaniniFS : Visualisation État Architecture
📊 Dashboard complet statut composants + convergences + sécurité analogique
"""

import json
import os
import datetime
from typing import Dict, List, Any, Optional
import subprocess

class PaniniFSDashboard:
    def __init__(self, base_path: str = "/home/stephane/GitHub/PaniniFS-1/scripts/scripts"):
        self.base_path = base_path
        self.architecture_data = None
        self.dashboard_metrics = {}
        
    def load_unified_architecture(self) -> bool:
        """Chargement architecture unifiée la plus récente"""
        print("📋 CHARGEMENT ARCHITECTURE UNIFIÉE...")
        
        # Recherche fichier architecture le plus récent
        architecture_files = []
        for file in os.listdir(self.base_path):
            if file.startswith("panini_unified_architecture_") and file.endswith(".json"):
                full_path = os.path.join(self.base_path, file)
                mod_time = os.path.getmtime(full_path)
                architecture_files.append((file, mod_time, full_path))
        
        if not architecture_files:
            print("   ❌ Aucun fichier architecture trouvé")
            return False
        
        # Sélection plus récent
        latest_file = max(architecture_files, key=lambda x: x[1])
        print(f"   📂 Chargement: {latest_file[0]}")
        
        try:
            with open(latest_file[2], 'r', encoding='utf-8') as f:
                self.architecture_data = json.load(f)
            print(f"   ✅ Architecture chargée avec succès")
            return True
        except Exception as e:
            print(f"   ❌ Erreur chargement: {e}")
            return False
    
    def calculate_dashboard_metrics(self) -> Dict:
        """Calcul métriques dashboard"""
        if not self.architecture_data:
            return {}
        
        metadata = self.architecture_data.get("integration_metadata", {})
        atoms = self.architecture_data.get("unified_semantic_atoms", {})
        convergences = self.architecture_data.get("cross_domain_relations", [])
        principles = self.architecture_data.get("architectural_principles", [])
        
        # Métriques générales
        total_atoms = len(atoms)
        total_convergences = len(convergences)
        total_principles = len(principles)
        
        # Métriques par composant
        component_metrics = {}
        layer_metrics = {}
        
        for atom_id, atom_data in atoms.items():
            component = atom_data.get("component_source", "unknown")
            layer = atom_data.get("architectural_layer", "unknown")
            
            if component not in component_metrics:
                component_metrics[component] = {
                    "atoms_count": 0,
                    "last_update": None,
                    "concepts": []
                }
            
            component_metrics[component]["atoms_count"] += 1
            component_metrics[component]["concepts"].append(atom_data.get("concept", ""))
            
            layer_metrics[layer] = layer_metrics.get(layer, 0) + 1
        
        # Métriques convergences
        convergence_strength = {}
        for conv in convergences:
            keyword = conv.get("convergence_keyword", "unknown")
            strength = conv.get("cross_domain_strength", 0)
            convergence_strength[keyword] = strength
        
        # Score santé globale
        health_score = self._calculate_health_score(total_atoms, total_convergences, component_metrics)
        
        self.dashboard_metrics = {
            "general_metrics": {
                "total_atoms": total_atoms,
                "total_convergences": total_convergences,
                "total_principles": total_principles,
                "health_score": health_score,
                "last_integration": metadata.get("integration_date", "unknown")
            },
            "component_metrics": component_metrics,
            "layer_metrics": layer_metrics,
            "convergence_strength": convergence_strength,
            "theoretical_foundations": metadata.get("theoretical_foundations", []),
            "safety_mechanisms": metadata.get("safety_mechanisms", [])
        }
        
        return self.dashboard_metrics
    
    def _calculate_health_score(self, atoms: int, convergences: int, components: Dict) -> float:
        """Calcul score santé architecture"""
        score = 0.0
        
        # Points atomes (max 30 points)
        if atoms > 0:
            score += min(atoms / 50.0 * 30, 30)
        
        # Points convergences (max 25 points)
        if convergences > 0:
            score += min(convergences / 10.0 * 25, 25)
        
        # Points diversité composants (max 20 points)
        active_components = len([c for c in components.values() if c["atoms_count"] > 0])
        score += min(active_components / 6.0 * 20, 20)
        
        # Points distribution équilibrée (max 25 points)
        if components:
            atom_counts = [c["atoms_count"] for c in components.values()]
            if atom_counts:
                mean_atoms = sum(atom_counts) / len(atom_counts)
                variance = sum((x - mean_atoms) ** 2 for x in atom_counts) / len(atom_counts)
                balance_score = max(0, 25 - variance / 10)
                score += balance_score
        
        return min(score, 100.0)
    
    def display_dashboard(self):
        """Affichage dashboard complet"""
        if not self.dashboard_metrics:
            print("❌ Aucune métrique disponible")
            return
        
        print("\n🎛️ TABLEAU DE BORD PANINI-FS")
        print("=" * 50)
        
        # Section métriques générales
        general = self.dashboard_metrics["general_metrics"]
        print(f"\n📊 MÉTRIQUES GÉNÉRALES")
        print(f"   🧠 Atomes sémantiques: {general['total_atoms']}")
        print(f"   🔗 Convergences détectées: {general['total_convergences']}")
        print(f"   🏗️ Principes architecturaux: {general['total_principles']}")
        print(f"   ❤️ Score santé: {general['health_score']:.1f}/100")
        print(f"   🕐 Dernière intégration: {general['last_integration'][:19] if general['last_integration'] != 'unknown' else 'unknown'}")
        
        # Barre santé visuelle
        health_bar = self._generate_health_bar(general['health_score'])
        print(f"   📈 Santé: {health_bar}")
        
        # Section composants
        print(f"\n🔧 ÉTAT COMPOSANTS")
        components = self.dashboard_metrics["component_metrics"]
        for comp_name, comp_data in components.items():
            status_icon = "✅" if comp_data["atoms_count"] > 0 else "⚠️"
            print(f"   {status_icon} {comp_name}: {comp_data['atoms_count']} atomes")
            
            # Top concepts
            if comp_data["concepts"]:
                top_concepts = comp_data["concepts"][:3]
                concepts_str = ", ".join(top_concepts)
                if len(concepts_str) > 60:
                    concepts_str = concepts_str[:57] + "..."
                print(f"      📝 Concepts: {concepts_str}")
        
        # Section couches architecturales
        print(f"\n🏗️ COUCHES ARCHITECTURALES")
        layers = self.dashboard_metrics["layer_metrics"]
        total_layer_atoms = sum(layers.values())
        for layer_name, atom_count in sorted(layers.items(), key=lambda x: x[1], reverse=True):
            percentage = (atom_count / total_layer_atoms * 100) if total_layer_atoms > 0 else 0
            layer_bar = self._generate_percentage_bar(percentage)
            print(f"   📊 {layer_name}: {atom_count} atomes ({percentage:.1f}%) {layer_bar}")
        
        # Section convergences
        print(f"\n🔗 FORCE CONVERGENCES")
        convergences = self.dashboard_metrics["convergence_strength"]
        if convergences:
            for keyword, strength in sorted(convergences.items(), key=lambda x: x[1], reverse=True):
                strength_bar = self._generate_strength_bar(strength)
                print(f"   🎯 {keyword}: force {strength} {strength_bar}")
        else:
            print("   ⚠️ Aucune convergence détectée")
        
        # Section fondations théoriques
        print(f"\n🧮 FONDATIONS THÉORIQUES")
        foundations = self.dashboard_metrics["theoretical_foundations"]
        for foundation in foundations:
            print(f"   ✅ {foundation}")
        
        # Section mécanismes sécurité
        print(f"\n🛡️ MÉCANISMES SÉCURITÉ")
        safety = self.dashboard_metrics["safety_mechanisms"]
        for mechanism in safety:
            print(f"   🔒 {mechanism}")
        
        # Section recommandations
        recommendations = self._generate_recommendations()
        if recommendations:
            print(f"\n💡 RECOMMANDATIONS")
            for rec in recommendations:
                print(f"   {rec}")
    
    def _generate_health_bar(self, score: float) -> str:
        """Génération barre santé visuelle"""
        bar_length = 20
        filled = int(score / 100 * bar_length)
        empty = bar_length - filled
        
        if score >= 80:
            color = "🟢"
        elif score >= 60:
            color = "🟡"
        elif score >= 40:
            color = "🟠"
        else:
            color = "🔴"
        
        return f"{color}{'█' * filled}{'░' * empty} {score:.1f}%"
    
    def _generate_percentage_bar(self, percentage: float) -> str:
        """Génération barre pourcentage"""
        bar_length = 10
        filled = int(percentage / 100 * bar_length)
        empty = bar_length - filled
        return f"{'█' * filled}{'░' * empty}"
    
    def _generate_strength_bar(self, strength: int) -> str:
        """Génération barre force convergence"""
        max_strength = 5
        bar_length = 10
        filled = int(min(strength, max_strength) / max_strength * bar_length)
        empty = bar_length - filled
        return f"{'🔗' * (filled // 2)}{'░' * (empty // 2)}"
    
    def _generate_recommendations(self) -> List[str]:
        """Génération recommandations basées sur métriques"""
        recommendations = []
        general = self.dashboard_metrics["general_metrics"]
        components = self.dashboard_metrics["component_metrics"]
        
        # Recommandations santé
        if general["health_score"] < 50:
            recommendations.append("⚠️ Score santé faible - augmenter nombre atomes et convergences")
        elif general["health_score"] < 80:
            recommendations.append("📈 Score santé moyen - améliorer équilibrage composants")
        else:
            recommendations.append("✅ Excellente santé architecturale")
        
        # Recommandations composants
        inactive_components = [name for name, data in components.items() if data["atoms_count"] == 0]
        if inactive_components:
            recommendations.append(f"🔧 Activer composants inactifs: {', '.join(inactive_components[:2])}")
        
        # Recommandations convergences
        if general["total_convergences"] < 3:
            recommendations.append("🔗 Enrichir convergences cross-domaines")
        
        # Recommandations générales
        if general["total_atoms"] < 30:
            recommendations.append("📚 Collecter plus d'atomes sémantiques")
        
        return recommendations
    
    def generate_status_summary(self) -> Dict:
        """Génération résumé statut pour exports"""
        if not self.dashboard_metrics:
            return {"error": "No metrics available"}
        
        general = self.dashboard_metrics["general_metrics"]
        components = self.dashboard_metrics["component_metrics"]
        
        # Statut composants
        component_status = {}
        for comp_name, comp_data in components.items():
            component_status[comp_name] = {
                "status": "active" if comp_data["atoms_count"] > 0 else "inactive",
                "atoms_count": comp_data["atoms_count"],
                "health": "good" if comp_data["atoms_count"] > 5 else "needs_attention"
            }
        
        # Évaluation globale
        overall_status = "excellent" if general["health_score"] >= 80 else \
                        "good" if general["health_score"] >= 60 else \
                        "needs_improvement" if general["health_score"] >= 40 else "critical"
        
        summary = {
            "overall_status": overall_status,
            "health_score": general["health_score"],
            "total_atoms": general["total_atoms"],
            "total_convergences": general["total_convergences"],
            "component_status": component_status,
            "active_components": len([c for c in component_status.values() if c["status"] == "active"]),
            "theoretical_coverage": len(self.dashboard_metrics["theoretical_foundations"]),
            "safety_coverage": len(self.dashboard_metrics["safety_mechanisms"]),
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        return summary
    
    def save_dashboard_report(self, output_path: str = None) -> str:
        """Sauvegarde rapport dashboard"""
        if not output_path:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"/home/stephane/GitHub/PaniniFS-1/scripts/scripts/panini_dashboard_report_{timestamp}.json"
        
        report = {
            "dashboard_metadata": {
                "generation_date": datetime.datetime.now().isoformat(),
                "panini_version": "2.0-architectural",
                "report_type": "dashboard_metrics"
            },
            "metrics": self.dashboard_metrics,
            "status_summary": self.generate_status_summary(),
            "architecture_data": self.architecture_data
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Rapport dashboard sauvegardé: {output_path}")
        return output_path

def main():
    print("🎛️ DASHBOARD PANINI-FS")
    print("======================")
    print("📊 Visualisation complète état architecture")
    print("")
    
    # Initialisation dashboard
    dashboard = PaniniFSDashboard()
    
    # Chargement architecture
    if not dashboard.load_unified_architecture():
        print("❌ Impossible de charger l'architecture")
        return
    
    # Calcul métriques
    metrics = dashboard.calculate_dashboard_metrics()
    print(f"📊 {len(metrics)} groupes métriques calculées")
    
    # Affichage dashboard
    dashboard.display_dashboard()
    
    # Sauvegarde rapport
    report_path = dashboard.save_dashboard_report()
    
    # Résumé final
    summary = dashboard.generate_status_summary()
    print(f"\n🏆 RÉSUMÉ FINAL")
    print(f"   Status global: {summary['overall_status']} ({summary['health_score']:.1f}/100)")
    print(f"   Composants actifs: {summary['active_components']}/6")
    print(f"   Couverture théorique: {summary['theoretical_coverage']} fondations")
    print(f"   Couverture sécurité: {summary['safety_coverage']} mécanismes")
    print(f"📁 Rapport: {os.path.basename(report_path)}")

if __name__ == "__main__":
    main()
