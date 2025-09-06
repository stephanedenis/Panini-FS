#!/usr/bin/env python3
"""
💰 Budget Tracker PaniniFS
Surveillance coûts GitHub Actions + Cloud platforms
"""

import requests
import json
from datetime import datetime, timedelta

class BudgetTracker:
    def __init__(self):
        self.monthly_budget_cad = 40
        self.github_free_minutes = 2000
        
    def get_github_actions_usage(self):
        """Récupération usage GitHub Actions"""
        # Nécessite GitHub token avec permissions appropriées
        # Pour l'instant, simulation
        
        current_month_minutes = 150  # À récupérer via API
        percentage_used = (current_month_minutes / self.github_free_minutes) * 100
        
        return {
            'minutes_used': current_month_minutes,
            'minutes_total': self.github_free_minutes,
            'percentage_used': percentage_used,
            'estimated_monthly': current_month_minutes * 30 / datetime.now().day
        }
    
    def calculate_cloud_costs(self):
        """Calcul coûts cloud estimés"""
        costs = {
            'oracle_free': 0,  # Always free
            'azure_students': 0,  # Si éligible
            'gcp_free': 0,  # f1-micro always free
            'github_actions_overflow': 0,  # Calculé selon usage
            'storage_backup': 5,  # Estimation
            'cdn_pro': 0,  # Gratuit ou 20$ si upgrade
            'total_estimated': 5
        }
        
        return costs
    
    def generate_budget_report(self):
        """Génération rapport budget"""
        github_usage = self.get_github_actions_usage()
        cloud_costs = self.calculate_cloud_costs()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'monthly_budget_cad': self.monthly_budget_cad,
            'github_actions': github_usage,
            'cloud_costs': cloud_costs,
            'budget_status': {
                'used_percentage': (cloud_costs['total_estimated'] / self.monthly_budget_cad) * 100,
                'remaining_budget': self.monthly_budget_cad - cloud_costs['total_estimated'],
                'status': 'GREEN'  # GREEN/YELLOW/RED
            }
        }
        
        # Déterminer status couleur
        used_pct = report['budget_status']['used_percentage']
        if used_pct > 80:
            report['budget_status']['status'] = 'RED'
        elif used_pct > 60:
            report['budget_status']['status'] = 'YELLOW'
        
        return report
    
    def save_budget_report(self):
        """Sauvegarde rapport budget"""
        report = self.generate_budget_report()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"budget_report_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"💾 Budget report saved: {filename}")
        print(f"💰 Current spend: ${report['cloud_costs']['total_estimated']:.2f}/{self.monthly_budget_cad} CAD")
        print(f"📊 Status: {report['budget_status']['status']}")
        
        return filename

if __name__ == "__main__":
    tracker = BudgetTracker()
    tracker.save_budget_report()
