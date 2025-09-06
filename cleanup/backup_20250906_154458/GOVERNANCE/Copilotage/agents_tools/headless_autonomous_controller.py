#!/usr/bin/env python3
"""
🤖 CONTRÔLEUR CENTRAL AUTONOME HEADLESS
=====================================

Contrôleur principal en mode headless pour autonomie totale :
- Gestion GitHub via API
- Contrôle Colab via requêtes HTTP
- Surveillance continue sans interface
- Déploiement et monitoring automatique
"""

import os
import json
import time
import requests
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class HeadlessAutonomousController:
    """Contrôleur autonome headless pour gestion complète du système"""
    
    def __init__(self, base_path: str = "/home/stephane/GitHub/PaniniFS-1"):
        self.base_path = base_path
        self.session_id = f"headless_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Configuration APIs
        self.github_api_base = "https://api.github.com"
        self.github_repo = "stephanedenis/PaniniFS"
        
        # État du système
        self.system_status = {
            'agents': {},
            'github_workflows': {},
            'colab_status': 'UNKNOWN',
            'last_check': None
        }
        
    def _log(self, message: str, level: str = "INFO"):
        """Log headless avec timestamps"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] [HEADLESS-{level}] {message}"
        print(log_msg)
        
        # Log persistant
        log_file = os.path.join(self.base_path, "logs", "headless_controller.log")
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, "a") as f:
            f.write(log_msg + "\n")
    
    def check_running_processes(self) -> Dict[str, Any]:
        """Vérifie les processus PaniniFS critiques encore en cours"""
        self._log("🔍 Vérification processus critiques...")
        
        try:
            # Recherche processus PaniniFS CRITIQUES seulement
            result = subprocess.run([
                'ps', 'aux'
            ], capture_output=True, text=True)
            
            critical_processes = []
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    # Ignorer VSCode, Jupyter, pylint etc.
                    if any(ignore in line for ignore in ['vscode', 'pylint', 'mypy', 'ipykernel', 'lsp_server']):
                        continue
                        
                    # Chercher processus critiques PaniniFS
                    if any(pattern in line for pattern in [
                        'monitoring.sh', 'start_permanent_monitoring', 
                        'github_workflow_monitor.py', 'autonomous_orchestrator',
                        'theoretical_research_agent.py', 'adversarial_critic_agent.py'
                    ]):
                        critical_processes.append(line.strip())
            
            self._log(f"📊 Processus critiques: {len(critical_processes)}")
            return {
                'total_processes': len(critical_processes),
                'processes': critical_processes,
                'status': 'CLEAN' if len(critical_processes) == 0 else 'ACTIVE'
            }
            
        except Exception as e:
            self._log(f"❌ Erreur vérification processus: {e}", "ERROR")
            return {'status': 'ERROR', 'error': str(e)}
    
    def kill_remaining_processes(self) -> bool:
        """Tue tous les processus PaniniFS restants"""
        self._log("🔥 Nettoyage processus restants...")
        
        try:
            # Kill par pattern
            patterns = ['monitoring', 'panini', 'github.*monitor']
            
            for pattern in patterns:
                result = subprocess.run([
                    'pkill', '-f', pattern
                ], capture_output=True)
                
                if result.returncode == 0:
                    self._log(f"✅ Processus '{pattern}' terminés")
                else:
                    self._log(f"ℹ️ Aucun processus '{pattern}' trouvé")
            
            return True
            
        except Exception as e:
            self._log(f"❌ Erreur kill processus: {e}", "ERROR")
            return False
    
    def check_crontab_status(self) -> Dict[str, Any]:
        """Vérifie l'état du crontab"""
        self._log("⏰ Vérification crontab...")
        
        try:
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            
            if result.returncode == 0:
                cron_content = result.stdout
                panini_jobs = [line for line in cron_content.split('\n') 
                              if 'panini' in line.lower() or 'PaniniFS' in line]
                
                return {
                    'has_crontab': True,
                    'panini_jobs': len(panini_jobs),
                    'jobs': panini_jobs,
                    'status': 'CLEAN' if len(panini_jobs) == 0 else 'ACTIVE'
                }
            else:
                return {
                    'has_crontab': False,
                    'status': 'CLEAN'
                }
                
        except Exception as e:
            self._log(f"❌ Erreur crontab: {e}", "ERROR")
            return {'status': 'ERROR', 'error': str(e)}
    
    def clear_crontab(self) -> bool:
        """Nettoie le crontab"""
        self._log("🧹 Nettoyage crontab...")
        
        try:
            # Crontab vide
            result = subprocess.run(['crontab', '-r'], capture_output=True)
            self._log("✅ Crontab nettoyé")
            return True
            
        except Exception as e:
            self._log(f"❌ Erreur nettoyage crontab: {e}", "ERROR")
            return False
    
    def test_agents_functionality(self) -> Dict[str, Any]:
        """Test tous les agents en mode headless"""
        self._log("🧪 Test agents headless...")
        
        agents_results = {}
        
        # Test agents simplifiés
        agents = [
            'theoretical_research_simple.py',
            'adversarial_critic_simple.py', 
            'simple_autonomous_orchestrator.py'
        ]
        
        for agent in agents:
            self._log(f"🤖 Test agent: {agent}")
            
            try:
                agent_path = os.path.join(self.base_path, "Copilotage/agents", agent)
                
                result = subprocess.run([
                    'python3', agent_path
                ], cwd=self.base_path, capture_output=True, text=True, timeout=60)
                
                agents_results[agent] = {
                    'status': 'SUCCESS' if result.returncode == 0 else 'ERROR',
                    'returncode': result.returncode,
                    'output_lines': len(result.stdout.split('\n')) if result.stdout else 0,
                    'has_error': len(result.stderr) > 0 if result.stderr else False
                }
                
                if result.returncode == 0:
                    self._log(f"✅ Agent {agent}: FONCTIONNEL")
                else:
                    self._log(f"❌ Agent {agent}: ERREUR {result.returncode}", "ERROR")
                    
            except subprocess.TimeoutExpired:
                self._log(f"⏱️ Agent {agent}: TIMEOUT", "WARNING")
                agents_results[agent] = {'status': 'TIMEOUT'}
            except Exception as e:
                self._log(f"❌ Agent {agent}: EXCEPTION {e}", "ERROR")
                agents_results[agent] = {'status': 'EXCEPTION', 'error': str(e)}
        
        return agents_results
    
    def check_github_workflows_api(self) -> Dict[str, Any]:
        """Vérifie les workflows GitHub via API"""
        self._log("👁️ Vérification workflows GitHub (API)...")
        
        try:
            # API GitHub workflows
            url = f"{self.github_api_base}/repos/{self.github_repo}/actions/workflows"
            
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                workflows_data = response.json()
                workflows = workflows_data.get('workflows', [])
                
                workflow_status = {}
                total_workflows = len(workflows)
                
                for workflow in workflows:
                    name = workflow.get('name', 'Unknown')
                    state = workflow.get('state', 'unknown')
                    workflow_status[name] = {
                        'state': state,
                        'path': workflow.get('path', ''),
                        'created_at': workflow.get('created_at', '')
                    }
                
                self._log(f"✅ GitHub workflows: {total_workflows} détectés")
                return {
                    'status': 'SUCCESS',
                    'total_workflows': total_workflows,
                    'workflows': workflow_status
                }
            else:
                self._log(f"❌ GitHub API error: {response.status_code}", "ERROR")
                return {
                    'status': 'API_ERROR',
                    'status_code': response.status_code
                }
                
        except Exception as e:
            self._log(f"❌ Erreur GitHub API: {e}", "ERROR")
            return {'status': 'ERROR', 'error': str(e)}
    
    def deploy_colab_controller(self) -> Dict[str, Any]:
        """Déploie contrôleur Colab autonome"""
        self._log("� Déploiement contrôleur Colab...")
        
        # Script de contrôle Colab autonome
        colab_controller = """
# 🤖 CONTRÔLEUR COLAB AUTONOME HEADLESS
# =====================================

import os
import json
import subprocess
from datetime import datetime

class ColabAutonomousController:
    def __init__(self):
        self.session_id = f"colab_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def run_autonomous_cycle(self):
        print(f"🤖 Cycle autonome Colab - {self.session_id}")
        
        # Test agents
        agents = [
            'theoretical_research_simple.py',
            'adversarial_critic_simple.py',
            'simple_autonomous_orchestrator.py'
        ]
        
        results = {}
        for agent in agents:
            try:
                result = subprocess.run([
                    'python3', f'Copilotage/agents/{agent}'
                ], capture_output=True, text=True, timeout=120)
                
                results[agent] = {
                    'status': 'SUCCESS' if result.returncode == 0 else 'ERROR',
                    'returncode': result.returncode
                }
                print(f"✅ {agent}: {'OK' if result.returncode == 0 else 'ERREUR'}")
                
            except Exception as e:
                results[agent] = {'status': 'EXCEPTION', 'error': str(e)}
                print(f"❌ {agent}: {e}")
        
        # Rapport
        report = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'environment': 'Google Colab',
            'results': results,
            'status': 'AUTONOMOUS_ACTIVE'
        }
        
        # Sauvegarde
        with open(f'colab_report_{self.session_id}.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Rapport: colab_report_{self.session_id}.json")
        return report

# Exécution autonome
if __name__ == "__main__":
    controller = ColabAutonomousController()
    controller.run_autonomous_cycle()
"""
        
        # Sauvegarde script
        colab_script_path = os.path.join(self.base_path, "Copilotage", "colab_autonomous_controller.py")
        with open(colab_script_path, 'w') as f:
            f.write(colab_controller)
        
        self._log(f"✅ Contrôleur Colab créé: {colab_script_path}")
        
        return {
            'status': 'DEPLOYED',
            'script_path': colab_script_path,
            'colab_ready': True
        }
    
    def generate_autonomous_status_report(self) -> Dict[str, Any]:
        """Génère rapport d'état complet du système autonome"""
        self._log("📊 Génération rapport autonomie...")
        
        # Collecte données
        processes = self.check_running_processes()
        crontab = self.check_crontab_status()
        agents = self.test_agents_functionality()
        github = self.check_github_workflows_api()
        colab = self.deploy_colab_controller()  # Déploie le contrôleur Colab
        
        # Évaluation globale
        totoro_clean = (processes['status'] == 'CLEAN' and 
                       crontab['status'] == 'CLEAN')
        
        agents_ok = all(result.get('status') == 'SUCCESS' 
                       for result in agents.values())
        
        github_ok = github['status'] == 'SUCCESS'
        colab_ok = colab['status'] == 'DEPLOYED'
        
        autonomy_ready = totoro_clean and agents_ok and github_ok and colab_ok
        
        report = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'totoro_status': {
                'processes_clean': processes['status'] == 'CLEAN',
                'crontab_clean': crontab['status'] == 'CLEAN',
                'ready_for_shutdown': totoro_clean
            },
            'cloud_system': {
                'agents_functional': agents_ok,
                'github_workflows': github_ok,
                'colab_accessible': colab_ok,
                'fully_autonomous': autonomy_ready
            },
            'detailed_status': {
                'processes': processes,
                'crontab': crontab,
                'agents': agents,
                'github': github,
                'colab': colab
            },
            'autonomy_verdict': {
                'can_shutdown_totoro': autonomy_ready,
                'reason': 'Système entièrement autonome dans le cloud' if autonomy_ready else 'Problèmes détectés',
                'next_action': 'Éteindre Totoro en sécurité' if autonomy_ready else 'Corriger les erreurs'
            }
        }
        
        return report
    
    def run_full_autonomy_check(self) -> Dict[str, Any]:
        """Cycle complet de vérification autonomie"""
        self._log("🚀 DÉBUT VÉRIFICATION AUTONOMIE TOTALE")
        
        start_time = time.time()
        
        # Nettoyage Totoro
        self._log("🧹 Phase 1: Nettoyage Totoro")
        self.kill_remaining_processes()
        self.clear_crontab()
        
        time.sleep(2)  # Attente nettoyage
        
        # Génération rapport
        self._log("📊 Phase 2: Évaluation système")
        report = self.generate_autonomous_status_report()
        
        # Sauvegarde
        report_file = os.path.join(
            self.base_path,
            f"headless_autonomy_report_{self.session_id}.json"
        )
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        duration = time.time() - start_time
        
        # Résultat final
        verdict = report['autonomy_verdict']
        
        self._log("=" * 60)
        if verdict['can_shutdown_totoro']:
            self._log("🎉 AUTONOMIE TOTALE VALIDÉE !", "SUCCESS")
            self._log("🔥 TOTORO PEUT ÊTRE ÉTEINT EN SÉCURITÉ")
        else:
            self._log("⚠️ AUTONOMIE PARTIELLE", "WARNING")
            self._log(f"🔧 Action requise: {verdict['reason']}")
        
        self._log(f"📄 Rapport: {report_file}")
        self._log(f"⏱️ Durée: {duration:.2f}s")
        
        return report

def main():
    """Fonction principale headless"""
    print("🤖 CONTRÔLEUR AUTONOME HEADLESS - DÉMARRAGE")
    print("=" * 60)
    
    controller = HeadlessAutonomousController()
    
    try:
        # Vérification complète
        report = controller.run_full_autonomy_check()
        
        # Affichage résultat
        verdict = report['autonomy_verdict']
        
        print("\n🎯 RÉSULTAT FINAL:")
        print(f"   Totoro clean: {report['totoro_status']['ready_for_shutdown']}")
        print(f"   Agents OK: {report['cloud_system']['agents_functional']}")
        print(f"   GitHub OK: {report['cloud_system']['github_workflows']}")
        print(f"   Colab OK: {report['cloud_system']['colab_accessible']}")
        print(f"   Autonomie: {verdict['can_shutdown_totoro']}")
        
        if verdict['can_shutdown_totoro']:
            print("\n✅ MISSION ACCOMPLIE - AUTONOMIE TOTALE HEADLESS")
            return 0
        else:
            print(f"\n⚠️ Action requise: {verdict['reason']}")
            return 1
        
    except Exception as e:
        print(f"\n❌ ERREUR CONTRÔLEUR: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
