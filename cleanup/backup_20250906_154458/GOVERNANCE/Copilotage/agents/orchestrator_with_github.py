#!/usr/bin/env python3
"""
🤖 ORCHESTRATEUR AVEC SURVEILLANCE GITHUB
=======================================

Orchestrateur autonome intégrant:
- Agent Recherche Théorique
- Agent Critique Adverse  
- Surveillance GitHub Workflows
- Cycles amélioration continue

Fonctionnement 100% autonome avec alertes GitHub.
"""

import asyncio
import json
import subprocess
import time
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Import surveillance GitHub
sys.path.append('/home/stephane/GitHub/PaniniFS-1/Copilotage/scripts')
from github_workflow_monitor import GitHubWorkflowMonitor

class AutonomousOrchestrator:
    """Orchestrateur autonome avec surveillance GitHub"""
    
    def __init__(self):
        self.session_id = f"orchestrator_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.base_path = Path("/home/stephane/GitHub/PaniniFS-1")
        self.agents_path = self.base_path / "Copilotage" / "agents"
        self.logs_path = self.base_path / "logs"
        
        # Surveillance GitHub
        self.github_monitor = GitHubWorkflowMonitor()
        self.last_github_check = None
        self.github_alert_threshold = 1  # Alertes avant action
        
        # Configuration cycles
        self.monitoring_active = True
        self.cycle_interval = 1800  # 30 minutes
        self.github_check_interval = 3600  # 1 heure
        
        # Statistiques
        self.stats = {
            'start_time': datetime.now().isoformat(),
            'cycles_completed': 0,
            'research_executions': 0,
            'critic_executions': 0,
            'github_checks': 0,
            'github_alerts_total': 0,
            'errors_encountered': 0
        }
        
        print(f"🤖 Orchestrateur Autonome - Session: {self.session_id}")
        print("   📡 Surveillance GitHub activée")
        print("   🔄 Cycles amélioration continue")
        self._log_event('initialization', 'INFO', 'Orchestrateur démarré avec surveillance GitHub')
        
    def run_autonomous_monitoring(self):
        """Lance monitoring autonome complet"""
        print("\n🚀 DÉMARRAGE MONITORING AUTONOME")
        print("=" * 60)
        print("  🔍 Surveillance GitHub workflows")  
        print("  📚 Agent recherche théorique (dimanche)")
        print("  🔥 Agent critique adverse (quotidien)")
        print("  ⏰ Cycles automatiques 30min")
        print("=" * 60)
        
        cycle_count = 0
        
        try:
            while self.monitoring_active:
                cycle_count += 1
                cycle_start = datetime.now()
                
                print(f"\n🔄 CYCLE #{cycle_count} - {cycle_start.strftime('%H:%M:%S')}")
                print("-" * 50)
                
                # 1. Surveillance GitHub (prioritaire)
                github_status = self._check_github_if_needed()
                
                # 2. Actions basées sur alertes GitHub
                if github_status and github_status.get('total_alerts', 0) >= self.github_alert_threshold:
                    print("🚨 Alertes GitHub détectées - Exécution critique prioritaire")
                    self._execute_critic_agent()
                    
                # 3. Cycles agents selon planning
                self._execute_scheduled_agents()
                
                # 4. Analyse et rapport
                self._generate_cycle_report(cycle_start, github_status)
                
                self.stats['cycles_completed'] += 1
                
                print(f"✅ Cycle #{cycle_count} terminé")
                print(f"⏰ Pause {self.cycle_interval//60} minutes...")
                
                # Pause avant prochain cycle
                time.sleep(self.cycle_interval)
                
        except KeyboardInterrupt:
            print("\n⛔ Arrêt orchestrateur demandé par utilisateur")
        except Exception as e:
            self.stats['errors_encountered'] += 1
            self._log_event('monitoring_error', 'ERROR', f'Erreur monitoring: {e}')
            print(f"❌ Erreur monitoring: {e}")
        finally:
            self._print_final_summary()
            
    def _check_github_if_needed(self) -> Optional[Dict]:
        """Vérifie GitHub si nécessaire"""
        now = datetime.now()
        
        # Vérification si interval écoulé
        if (self.last_github_check is None or 
            now - self.last_github_check >= timedelta(seconds=self.github_check_interval)):
            
            print("🔍 Surveillance GitHub...")
            
            try:
                status = self.github_monitor.check_all_repos_status()
                self.last_github_check = now
                self.stats['github_checks'] += 1
                
                # Traitement alertes
                if status.get('total_alerts', 0) > 0:
                    self.stats['github_alerts_total'] += status['total_alerts']
                    
                    # Génération rapport détaillé
                    report_path = self.github_monitor.generate_monitoring_report(status)
                    self._log_event('github_alerts', 'WARNING', 
                                  f"Alertes GitHub: {status['total_alerts']} - Rapport: {report_path}")
                    
                    print(f"⚠️ {status['total_alerts']} alertes GitHub détectées")
                    return status
                else:
                    print("✅ Écosystème GitHub sain")
                    return status
                    
            except Exception as e:
                self._log_event('github_error', 'ERROR', f'Erreur surveillance GitHub: {e}')
                print(f"❌ Erreur surveillance GitHub: {e}")
                return None
                
        return None
        
    def _execute_scheduled_agents(self):
        """Exécute agents selon planning"""
        now = datetime.now()
        
        # Agent recherche théorique (dimanche)
        if now.weekday() == 6:  # Dimanche
            print("📚 Exécution agent recherche théorique (dimanche)")
            if self._execute_research_agent():
                self.stats['research_executions'] += 1
                
        # Agent critique adverse (quotidien si pas d'alerte GitHub récente)
        last_github_alert = self.stats['github_alerts_total'] > 0
        if not last_github_alert or now.hour % 6 == 0:  # Toutes les 6h ou quotidien
            print("🔥 Exécution agent critique adverse")
            if self._execute_critic_agent():
                self.stats['critic_executions'] += 1
                
    def _execute_research_agent(self) -> bool:
        """Exécute agent recherche théorique"""
        try:
            agent_path = self.agents_path / "theoretical_research_agent.py"
            
            print(f"   🔬 Lancement: {agent_path}")
            
            result = subprocess.run([
                'python3', str(agent_path)
            ], capture_output=True, text=True, timeout=1800, cwd=str(self.base_path))
            
            if result.returncode == 0:
                print("   ✅ Agent recherche terminé avec succès")
                self._log_event('research_success', 'INFO', 'Recherche théorique complétée')
                return True
            else:
                print(f"   ❌ Erreur agent recherche: {result.stderr[:200]}")
                self._log_event('research_error', 'ERROR', f'Stderr: {result.stderr[:200]}')
                return False
                
        except subprocess.TimeoutExpired:
            print("   ⏰ Timeout agent recherche (30min)")
            self._log_event('research_timeout', 'WARNING', 'Timeout recherche 30min')
            return False
        except Exception as e:
            print(f"   ❌ Exception agent recherche: {e}")
            self._log_event('research_exception', 'ERROR', f'Exception: {e}')
            return False
            
    def _execute_critic_agent(self) -> bool:
        """Exécute agent critique adverse"""
        try:
            agent_path = self.agents_path / "adversarial_critic_agent.py"
            
            print(f"   🔥 Lancement: {agent_path}")
            
            result = subprocess.run([
                'python3', str(agent_path)
            ], capture_output=True, text=True, timeout=900, cwd=str(self.base_path))
            
            if result.returncode == 0:
                print("   ✅ Agent critique terminé avec succès")
                self._log_event('critic_success', 'INFO', 'Critique adverse complétée')
                return True
            else:
                print(f"   ❌ Erreur agent critique: {result.stderr[:200]}")
                self._log_event('critic_error', 'ERROR', f'Stderr: {result.stderr[:200]}')
                return False
                
        except subprocess.TimeoutExpired:
            print("   ⏰ Timeout agent critique (15min)")
            self._log_event('critic_timeout', 'WARNING', 'Timeout critique 15min')
            return False
        except Exception as e:
            print(f"   ❌ Exception agent critique: {e}")
            self._log_event('critic_exception', 'ERROR', f'Exception: {e}')
            return False
            
    def _generate_cycle_report(self, cycle_start: datetime, github_status: Optional[Dict]):
        """Génère rapport de cycle"""
        cycle_duration = datetime.now() - cycle_start
        
        report = {
            'session_id': self.session_id,
            'cycle_timestamp': cycle_start.isoformat(),
            'cycle_duration_seconds': cycle_duration.total_seconds(),
            'github_status_checked': github_status is not None,
            'github_alerts_in_cycle': github_status.get('total_alerts', 0) if github_status else 0,
            'session_stats': self.stats.copy()
        }
        
        # Sauvegarde rapport
        report_path = self.base_path / f"orchestrator_cycle_report_{cycle_start.strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        # Affichage résumé
        print(f"   📊 Durée cycle: {cycle_duration.total_seconds():.1f}s")
        if github_status:
            print(f"   🔍 GitHub: {github_status.get('total_alerts', 0)} alertes")
            
    def _log_event(self, event_type: str, level: str, message: str):
        """Log événements orchestrateur"""
        timestamp = datetime.now().isoformat()
        
        # Assurer répertoire logs
        self.logs_path.mkdir(exist_ok=True)
        
        log_entry = {
            'timestamp': timestamp,
            'session_id': self.session_id,
            'event_type': event_type,
            'level': level,
            'message': message
        }
        
        # Log fichier
        log_file = self.logs_path / "orchestrator.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} [{level}] {event_type}: {message}\n")
            
    def _print_final_summary(self):
        """Affiche résumé final"""
        duration = datetime.now() - datetime.fromisoformat(self.stats['start_time'])
        
        print("\n" + "="*60)
        print("📊 RÉSUMÉ SESSION ORCHESTRATEUR")
        print("="*60)
        print(f"⏱️  Durée session: {duration}")
        print(f"🔄 Cycles complétés: {self.stats['cycles_completed']}")
        print(f"📚 Recherches théoriques: {self.stats['research_executions']}")
        print(f"🔥 Critiques adverses: {self.stats['critic_executions']}")
        print(f"🔍 Vérifications GitHub: {self.stats['github_checks']}")
        print(f"🚨 Alertes GitHub totales: {self.stats['github_alerts_total']}")
        print(f"❌ Erreurs rencontrées: {self.stats['errors_encountered']}")
        print("="*60)
        
        # Sauvegarde statistiques finales
        stats_path = self.base_path / f"orchestrator_final_stats_{self.session_id}.json"
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
            
        print(f"💾 Statistiques sauvegardées: {stats_path}")

def main():
    """Point d'entrée principal"""
    print("🤖 ORCHESTRATEUR AUTONOME AVEC SURVEILLANCE GITHUB")
    print("=" * 60)
    
    orchestrator = AutonomousOrchestrator()
    orchestrator.run_autonomous_monitoring()

if __name__ == "__main__":
    main()
