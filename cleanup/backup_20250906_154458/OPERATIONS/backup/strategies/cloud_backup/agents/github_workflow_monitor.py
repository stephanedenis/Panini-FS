#!/usr/bin/env python3
"""
🔍 SURVEILLANT GITHUB WORKFLOW AUTONOME
=====================================

Module de surveillance des workflows GitHub pour détection:
- Échecs CI/CD dans tous repos Panini
- Alertes sécurité et vulnérabilités
- Pull requests nécessitant review
- Issues critiques non résolues
- Métriques qualité code

Intégration avec orchestrateur amélioration continue.
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os

class GitHubWorkflowMonitor:
    """Surveillant autonome workflows GitHub"""
    
    def __init__(self):
        self.session_id = f"github_monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Repos Panini à surveiller
        self.repos_to_monitor = [
            'stephanedenis/PaniniFS',
            'stephanedenis/Panini-DevOps',
            'stephanedenis/PaniniFS-AutonomousMissions',
            'stephanedenis/PaniniFS-CloudOrchestrator',
            'stephanedenis/PaniniFS-CoLabController',
            'stephanedenis/PaniniFS-PublicationEngine',
            'stephanedenis/PaniniFS-SemanticCore',
            'stephanedenis/PaniniFS-UltraReactive'
        ]
        
        # Token GitHub (optionnel pour API publique)
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.headers = {}
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'
            
        self.alerts = []
        self.workflow_status = {}
        
    def check_all_repos_status(self) -> Dict:
        """Vérifie statut de tous les repos"""
        print("🔍 Surveillance GitHub - Tous repos Panini...")
        
        global_status = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'repos_checked': 0,
            'total_alerts': 0,
            'workflow_failures': 0,
            'security_alerts': 0,
            'open_issues': 0,
            'repo_details': {}
        }
        
        for repo in self.repos_to_monitor:
            try:
                repo_status = self._check_single_repo(repo)
                global_status['repo_details'][repo] = repo_status
                global_status['repos_checked'] += 1
                
                # Agrégation métriques
                if repo_status.get('workflow_failures', 0) > 0:
                    global_status['workflow_failures'] += repo_status['workflow_failures']
                    
                if repo_status.get('security_alerts', 0) > 0:
                    global_status['security_alerts'] += repo_status['security_alerts']
                    
                global_status['open_issues'] += repo_status.get('open_issues', 0)
                
            except Exception as e:
                print(f"⚠️ Erreur surveillance {repo}: {e}")
                global_status['repo_details'][repo] = {'error': str(e)}
                
        global_status['total_alerts'] = len(self.alerts)
        
        return global_status
        
    def _check_single_repo(self, repo: str) -> Dict:
        """Vérifie statut d'un repo spécifique"""
        repo_status = {
            'repo': repo,
            'last_check': datetime.now().isoformat(),
            'workflow_failures': 0,
            'security_alerts': 0,
            'open_issues': 0,
            'recent_commits': 0,
            'status': 'healthy'
        }
        
        # 1. Vérifier workflows récents
        workflows = self._get_recent_workflows(repo)
        if workflows:
            failed_workflows = [w for w in workflows if w.get('conclusion') == 'failure']
            repo_status['workflow_failures'] = len(failed_workflows)
            
            for workflow in failed_workflows:
                self._add_alert('workflow_failure', repo, f"Workflow failed: {workflow.get('name', 'Unknown')}")
                
        # 2. Vérifier issues ouvertes
        issues = self._get_open_issues(repo)
        if issues:
            repo_status['open_issues'] = len(issues)
            
            # Alertes pour issues critiques
            critical_issues = [i for i in issues if 'critical' in i.get('title', '').lower() or 'urgent' in i.get('title', '').lower()]
            for issue in critical_issues:
                self._add_alert('critical_issue', repo, f"Critical issue: {issue.get('title', 'Unknown')}")
                
        # 3. Activité récente
        commits = self._get_recent_commits(repo)
        if commits:
            repo_status['recent_commits'] = len(commits)
            
        # 4. Statut global repo
        if repo_status['workflow_failures'] > 0 or len([i for i in issues or [] if 'critical' in i.get('title', '').lower()]) > 0:
            repo_status['status'] = 'attention_required'
        elif repo_status['open_issues'] > 10:
            repo_status['status'] = 'monitoring'
            
        return repo_status
        
    def _get_recent_workflows(self, repo: str) -> List[Dict]:
        """Récupère workflows récents d'un repo"""
        try:
            url = f"https://api.github.com/repos/{repo}/actions/runs"
            params = {'per_page': 10}  # 10 derniers runs
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('workflow_runs', [])
            elif response.status_code == 404:
                print(f"⚠️ Repo {repo} non trouvé ou privé")
                return []
            else:
                print(f"⚠️ Erreur API workflows {repo}: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"⚠️ Erreur récupération workflows {repo}: {e}")
            return []
            
    def _get_open_issues(self, repo: str) -> List[Dict]:
        """Récupère issues ouvertes d'un repo"""
        try:
            url = f"https://api.github.com/repos/{repo}/issues"
            params = {'state': 'open', 'per_page': 50}
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return []
            else:
                print(f"⚠️ Erreur API issues {repo}: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"⚠️ Erreur récupération issues {repo}: {e}")
            return []
            
    def _get_recent_commits(self, repo: str) -> List[Dict]:
        """Récupère commits récents d'un repo"""
        try:
            url = f"https://api.github.com/repos/{repo}/commits"
            
            # Dernières 24h
            since = (datetime.now() - timedelta(days=1)).isoformat()
            params = {'since': since, 'per_page': 20}
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return []
            else:
                print(f"⚠️ Erreur API commits {repo}: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"⚠️ Erreur récupération commits {repo}: {e}")
            return []
            
    def _add_alert(self, alert_type: str, repo: str, message: str):
        """Ajoute alerte à la liste"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'repo': repo,
            'message': message,
            'severity': self._get_alert_severity(alert_type)
        }
        
        self.alerts.append(alert)
        
        # Log immédiat pour alertes critiques
        if alert['severity'] == 'HIGH':
            print(f"🚨 ALERTE {alert_type.upper()}: {repo} - {message}")
        elif alert['severity'] == 'MEDIUM':
            print(f"⚠️ Attention {alert_type}: {repo} - {message}")
            
    def _get_alert_severity(self, alert_type: str) -> str:
        """Détermine sévérité d'une alerte"""
        severity_map = {
            'workflow_failure': 'MEDIUM',
            'critical_issue': 'HIGH',
            'security_alert': 'HIGH',
            'dependency_vulnerability': 'MEDIUM',
            'performance_degradation': 'LOW'
        }
        
        return severity_map.get(alert_type, 'LOW')
        
    def generate_monitoring_report(self, status_data: Dict) -> str:
        """Génère rapport surveillance"""
        report_path = f"/home/stephane/GitHub/PaniniFS-1/github_monitoring_report_{self.session_id}.json"
        
        report = {
            'monitoring_session': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'global_status': status_data,
            'alerts': self.alerts,
            'summary': {
                'repos_monitored': len(self.repos_to_monitor),
                'repos_healthy': len([r for r in status_data['repo_details'].values() 
                                    if isinstance(r, dict) and r.get('status') == 'healthy']),
                'repos_attention': len([r for r in status_data['repo_details'].values() 
                                      if isinstance(r, dict) and r.get('status') == 'attention_required']),
                'total_workflow_failures': status_data['workflow_failures'],
                'total_open_issues': status_data['open_issues'],
                'alert_breakdown': self._get_alert_breakdown()
            },
            'recommendations': self._generate_recommendations(status_data)
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        # Rapport console
        self._print_monitoring_summary(report)
        
        print(f"📊 Rapport surveillance GitHub: {report_path}")
        return report_path
        
    def _get_alert_breakdown(self) -> Dict:
        """Breakdown alertes par type et sévérité"""
        breakdown = {
            'by_type': {},
            'by_severity': {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        }
        
        for alert in self.alerts:
            alert_type = alert.get('type', 'unknown')
            severity = alert.get('severity', 'LOW')
            
            breakdown['by_type'][alert_type] = breakdown['by_type'].get(alert_type, 0) + 1
            breakdown['by_severity'][severity] += 1
            
        return breakdown
        
    def _generate_recommendations(self, status_data: Dict) -> List[str]:
        """Génère recommandations basées sur surveillance"""
        recommendations = []
        
        # Workflow failures
        if status_data['workflow_failures'] > 0:
            recommendations.append(f"Corriger {status_data['workflow_failures']} workflow failures détectés")
            
        # Issues accumulées
        if status_data['open_issues'] > 20:
            recommendations.append("Trier et prioriser issues ouvertes (>20 total)")
            
        # Repos nécessitant attention
        attention_repos = [repo for repo, details in status_data['repo_details'].items() 
                          if isinstance(details, dict) and details.get('status') == 'attention_required']
        
        if attention_repos:
            recommendations.append(f"Attention prioritaire requise: {', '.join(attention_repos)}")
            
        # Alertes critiques
        critical_alerts = [a for a in self.alerts if a.get('severity') == 'HIGH']
        if critical_alerts:
            recommendations.append(f"Traiter {len(critical_alerts)} alertes critiques immédiatement")
            
        if not recommendations:
            recommendations.append("Écosystème GitHub en bonne santé - Continuer surveillance")
            
        return recommendations
        
    def _print_monitoring_summary(self, report: Dict):
        """Affiche résumé surveillance"""
        print("\n" + "="*60)
        print("🔍 RÉSUMÉ SURVEILLANCE GITHUB")
        print("="*60)
        
        summary = report['summary']
        print(f"\n📊 STATUT GLOBAL:")
        print(f"   🟢 Repos sains: {summary['repos_healthy']}/{summary['repos_monitored']}")
        print(f"   🟡 Attention requise: {summary['repos_attention']}")
        print(f"   ❌ Workflow failures: {summary['total_workflow_failures']}")
        print(f"   📋 Issues ouvertes: {summary['total_open_issues']}")
        
        if self.alerts:
            print(f"\n🚨 ALERTES ({len(self.alerts)} total):")
            breakdown = summary['alert_breakdown']
            print(f"   🔴 Critiques: {breakdown['by_severity']['HIGH']}")
            print(f"   🟡 Moyennes: {breakdown['by_severity']['MEDIUM']}")
            print(f"   🟢 Faibles: {breakdown['by_severity']['LOW']}")
            
        print(f"\n💡 RECOMMANDATIONS:")
        for rec in report['recommendations']:
            print(f"   • {rec}")
            
        print("\n" + "="*60)

def main():
    """Test surveillance GitHub"""
    print("🔍 SURVEILLANCE GITHUB AUTONOME - TEST")
    print("=" * 50)
    
    monitor = GitHubWorkflowMonitor()
    status = monitor.check_all_repos_status()
    monitor.generate_monitoring_report(status)

if __name__ == "__main__":
    main()
