#!/usr/bin/env python3
"""
🤖 ORCHESTRATEUR AMÉLIORATION CONTINUE SIMPLIFIÉ
===============================================

Version simplifiée fonctionnelle pour externalisation totale.
Surveillance GitHub + agents autonomes.
"""

import json
import subprocess
import time
from datetime import datetime
import os
import requests

# Import headless environment loader
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
try:
    from headless_env_loader import HeadlessEnvLoader
    HEADLESS_LOADER = HeadlessEnvLoader()
except ImportError:
    HEADLESS_LOADER = None


class SimpleAutonomousOrchestrator:
    """Orchestrateur simplifié pour autonomie post-Totoro"""
    
    def __init__(self):
        self.session_id = f"simple_orchestrator_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.base_path = "/home/stephane/GitHub/PaniniFS-1"
        self.repos = ['stephanedenis/PaniniFS', 'stephanedenis/Panini-DevOps']
        self.log = []
        
        print(f"🤖 Orchestrateur Simplifié - Session: {self.session_id}")
        
    def run_autonomous_cycle(self):
        """Cycle autonome complet"""
        print("🚀 CYCLE AUTONOME DÉMARRÉ")
        
        # 1. Surveillance GitHub
        github_status = self.check_github_health()
        
        # 2. Si problèmes détectés -> Agent critique
        if github_status['total_failures'] > 0:
            print(f"🚨 {github_status['total_failures']} GitHub failures détectés")
            self.run_critic_agent()
        
        # 3. Agent recherche (si weekend)
        if datetime.now().weekday() == 6:  # Dimanche
            print("📚 Weekend détecté - Lancement recherche théorique")
            self.run_research_agent()
            
        # 4. Rapport
        self.generate_status_report()
        
        print("✅ Cycle autonome terminé")
        
    def check_github_health(self):
        """Surveillance santé GitHub"""
        print("👁️ Vérification GitHub...")
        
        total_failures = 0
        repo_status = {}
        
        for repo in self.repos:
            try:
                # API GitHub workflows
                url = f"https://api.github.com/repos/{repo}/actions/runs?per_page=10"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    failed_runs = [run for run in data.get('workflow_runs', []) 
                                 if run.get('conclusion') == 'failure']
                    
                    repo_status[repo] = {
                        'failures': len(failed_runs),
                        'status': 'OK' if len(failed_runs) == 0 else 'ISSUES'
                    }
                    
                    total_failures += len(failed_runs)
                    
                    if failed_runs:
                        print(f"⚠️ {repo}: {len(failed_runs)} workflows failed")
                    else:
                        print(f"✅ {repo}: OK")
                        
                else:
                    print(f"⚠️ {repo}: API error {response.status_code}")
                    repo_status[repo] = {'failures': 0, 'status': 'API_ERROR'}
                    
            except Exception as e:
                print(f"❌ Erreur GitHub {repo}: {e}")
                repo_status[repo] = {'failures': 0, 'status': 'ERROR'}
                
        return {
            'total_failures': total_failures,
            'repos': repo_status,
            'timestamp': datetime.now().isoformat()
        }
        
    def run_research_agent(self):
        """Lance agent recherche théorique"""
        try:
            print("🔬 Lancement Agent Recherche...")
            
            agent_script = os.path.join(self.base_path, "Copilotage/agents/theoretical_research_agent.py")
            
            if os.path.exists(agent_script):
                # Exécution avec timeout
                result = subprocess.run([
                    "python3", agent_script
                ], 
                capture_output=True, 
                text=True, 
                timeout=1800,  # 30 min max
                cwd=self.base_path
                )
                
                if result.returncode == 0:
                    print("✅ Agent recherche terminé avec succès")
                    self.log.append({
                        'timestamp': datetime.now().isoformat(),
                        'agent': 'research',
                        'status': 'success'
                    })
                else:
                    print(f"⚠️ Agent recherche: erreur {result.returncode}")
                    self.log.append({
                        'timestamp': datetime.now().isoformat(),
                        'agent': 'research', 
                        'status': 'error',
                        'error': result.stderr[:200]
                    })
            else:
                print(f"❌ Agent recherche non trouvé: {agent_script}")
                
        except subprocess.TimeoutExpired:
            print("⏰ Agent recherche: timeout 30 min")
        except Exception as e:
            print(f"❌ Erreur agent recherche: {e}")
            
    def run_critic_agent(self):
        """Lance agent critique adverse"""
        try:
            print("🔥 Lancement Agent Critique...")
            
            agent_script = os.path.join(self.base_path, "Copilotage/agents/adversarial_critic_simple.py")
            
            if os.path.exists(agent_script):
                # Exécution avec timeout
                result = subprocess.run([
                    "python3", agent_script
                ], 
                capture_output=True, 
                text=True, 
                timeout=600,  # 10 min max
                cwd=self.base_path
                )
                
                if result.returncode == 0:
                    print("✅ Agent critique terminé avec succès")
                    self.log.append({
                        'timestamp': datetime.now().isoformat(),
                        'agent': 'critic',
                        'status': 'success'
                    })
                else:
                    print(f"⚠️ Agent critique: erreur {result.returncode}")
                    self.log.append({
                        'timestamp': datetime.now().isoformat(),
                        'agent': 'critic',
                        'status': 'error', 
                        'error': result.stderr[:200]
                    })
            else:
                print(f"❌ Agent critique non trouvé: {agent_script}")
                
        except subprocess.TimeoutExpired:
            print("⏰ Agent critique: timeout 10 min")
        except Exception as e:
            print(f"❌ Erreur agent critique: {e}")
            
    def generate_status_report(self):
        """Génère rapport de statut"""
        report = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'github_health': self.check_github_health(),
            'log_entries': len(self.log),
            'last_activities': self.log[-5:] if self.log else [],
            'system_status': 'autonomous_operational'
        }
        
        # Sauvegarde rapport
        report_path = os.path.join(self.base_path, f"autonomous_status_{datetime.now().strftime('%Y%m%d')}.json")
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
                
            print(f"📊 Rapport sauvegardé: {report_path}")
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde rapport: {e}")
            
        return report

def main():
    """Test autonome immédiat"""
    print("🤖 TEST ORCHESTRATEUR AUTONOME SIMPLIFIÉ")
    print("=" * 50)
    
    orchestrator = SimpleAutonomousOrchestrator()
    orchestrator.run_autonomous_cycle()
    
    print("\n🎉 Test terminé - Système prêt pour autonomie totale!")

if __name__ == "__main__":
    main()
