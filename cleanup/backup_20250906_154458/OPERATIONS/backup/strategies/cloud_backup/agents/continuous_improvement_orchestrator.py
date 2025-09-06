#!/usr/bin/env python3
"""
🤖 ORCHESTRATEUR AGENTS AMÉLIORATION CONTINUE
===========================================

Orchestrateur autonome pour coordination:
- Agent Recherche Théorique (mise à jour connaissances)
- Agent Critique Adverse (amélioration continue)
- Cycles de validation et amélioration
- Fonctionnement 100% autonome et externalisé

Objectif: Amélioration continue autonome de l'écosystème PaniniFS
via recherche théorique et critique constructive.
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
from typing import Dict, List, Optional
import os
from pathlib import Path
import schedule
import threading

class ContinuousImprovementOrchestrator:
    """Orchestrateur principal amélioration continue"""
    
    def __init__(self):
        self.session_id = f"orchestrator_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.base_path = Path("/home/stephane/GitHub/PaniniFS-1")
        self.agents_path = self.base_path / "Copilotage" / "agents"
        self.logs_path = self.base_path / "logs"
        
        # Configuration surveillance
        self.monitoring_active = True
        self.last_github_check = None
        self.github_monitor = GitHubWorkflowMonitor()
        
        # Statistiques session
        self.session_stats = {
            'start_time': datetime.now().isoformat(),
            'research_cycles': 0,
            'critic_cycles': 0,
            'github_checks': 0,
            'improvements_identified': 0,
            'errors_encountered': 0
        }
        
        print(f"🤖 Orchestrateur initialisé - Session: {self.session_id}")
        self._log_orchestrator_event('initialization', 'INFO', 'Orchestrateur démarré avec surveillance GitHub')
            
    def _setup_scheduling(self):
        """Configure planning automatique des agents"""
        print("📅 Configuration planning automatique...")
        
        # Agent recherche théorique - hebdomadaire
        schedule.every().sunday.at(self.schedule_config['research_time']).do(
            self._execute_research_agent
        )
        
        # Agent critique - quotidien
        schedule.every().day.at(self.schedule_config['criticism_time']).do(
            self._execute_critic_agent
        )
        
        # Rapport quotidien
        schedule.every().day.at(self.schedule_config['report_time']).do(
            self._generate_daily_report
        )
        
        print("✅ Planning configuré:")
        print(f"  📚 Recherche théorique: {self.schedule_config['research_day']} {self.schedule_config['research_time']}")
        print(f"  🔥 Critique adverse: quotidien {self.schedule_config['criticism_time']}")
        print(f"  📊 Rapport: quotidien {self.schedule_config['report_time']}")
        
    def _execute_initial_cycle(self):
        """Exécute le cycle initial complet d'amélioration"""
        print("🔄 CYCLE INITIAL AMÉLIORATION CONTINUE")
        print("=" * 50)
        
        try:
            # 1. Surveillance GitHub workflows
            github_status = self._monitor_github_workflows()
            
            # 2. Recherche théorique
            if self._execute_research_agent():
                print("✅ Agent recherche théorique terminé")
            else:
                print("❌ Échec agent recherche")
                
            # 3. Analyse critique
            if self._execute_critic_agent():
                print("✅ Agent critique adverse terminé")  
            else:
                print("❌ Échec agent critique")
                
            # 4. Analyse croisée
            self._cross_analysis_research_criticism()
            
            # 5. Surveillance continue GitHub
            if github_status:
                print("✅ Surveillance GitHub intégrée")
            
            print("🎯 Cycle initial terminé - surveillance continue activée")
            
        except Exception as e:
            print(f"❌ Erreur cycle initial: {e}")
            self._log_orchestrator_event('initial_cycle_error', 'ERROR', f'Erreur: {e}')
    
    def _monitor_github_workflows(self) -> bool:
        """Surveille les workflows GitHub et génère des alertes"""
        print("🔍 Surveillance GitHub Workflows...")
        
        try:
            import subprocess
            
            # Tentative vérification workflows avec GitHub CLI
            try:
                result = subprocess.run(
                    ['gh', 'workflow', 'list'], 
                    cwd=self.base_path,
                    capture_output=True, 
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    workflows_info = result.stdout
                    
                    # Vérification runs récents
                    runs_result = subprocess.run(
                        ['gh', 'run', 'list', '--limit', '5'],
                        cwd=self.base_path,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    # Analyse échecs récents
                    failed_runs = []
                    if runs_result.returncode == 0:
                        lines = runs_result.stdout.strip().split('
')
                        for line in lines[1:]:  # Skip header
                            if 'failure' in line.lower() or 'failed' in line.lower():
                                failed_runs.append(line.strip())
                    
                    # Génération alerte si échecs
                    if failed_runs:
                        alert_message = f"⚠️ ALERTES GITHUB WORKFLOWS DÉTECTÉES:
"
                        for failed in failed_runs:
                            alert_message += f"  • {failed}
"
                        
                        print(alert_message)
                        
                        # Log alerte
                        self._log_orchestrator_event(
                            'github_workflow_failures', 
                            'WARNING',
                            f'{len(failed_runs)} workflows en échec détectés'
                        )
                        
                        # Sauvegarde rapport détaillé
                        self._save_github_monitoring_report(workflows_info, runs_result.stdout, failed_runs)
                    else:
                        print("  ✅ Tous workflows GitHub opérationnels")
                        self._log_orchestrator_event('github_workflows_healthy', 'INFO', 'Workflows opérationnels')
                    
                    return True
                    
                else:
                    print("  ⚠️ GitHub CLI non configuré - surveillance manuelle recommandée")
                    self._log_orchestrator_event('github_cli_unavailable', 'WARNING', 'GitHub CLI non configuré')
                    return False
                    
            except FileNotFoundError:
                print("  ⚠️ GitHub CLI non installé - Installation: 'sudo apt install gh'")
                self._log_orchestrator_event('github_cli_missing', 'WARNING', 'GitHub CLI non installé')
                return False
                
            except subprocess.TimeoutExpired:
                print("  ⚠️ Timeout surveillance GitHub - vérification manuelle requise")
                self._log_orchestrator_event('github_timeout', 'WARNING', 'Timeout surveillance workflows')
                return False
                
        except Exception as e:
            print(f"  ❌ Erreur surveillance GitHub: {e}")
            self._log_orchestrator_event('github_monitoring_error', 'ERROR', f'Erreur: {e}')
            return False
    
    def _save_github_monitoring_report(self, workflows_info: str, runs_info: str, failed_runs: List[str]):
        """Sauvegarde rapport détaillé surveillance GitHub"""
        try:
            from datetime import datetime
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'workflows_status': workflows_info,
                'recent_runs': runs_info,
                'failed_runs': failed_runs,
                'total_failures': len(failed_runs),
                'monitoring_status': 'active',
                'recommendations': [
                    'Vérifier logs des workflows en échec',
                    'Corriger erreurs de configuration',
                    'Redéclencher workflows si nécessaire',
                    'Monitorer tendances échecs'
                ]
            }
            
            # Sauvegarde JSON
            report_path = os.path.join(self.base_path, f'github_monitoring_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
                
            print(f"  📊 Rapport GitHub sauvé: {report_path}")
            
        except Exception as e:
            print(f"  ❌ Erreur sauvegarde rapport GitHub: {e}")
        
    def _execute_research_agent(self) -> bool:
        """Exécute l'agent de recherche théorique"""
        try:
            print(f"🔬 Lancement Agent Recherche Théorique - {datetime.now()}")
            
            # Marquer agent comme running
            self.agents['theoretical_research']['status'] = 'running'
            self.agents['theoretical_research']['last_run'] = datetime.now()
            
            # Exécution agent
            script_path = os.path.join(self.agents_path, self.agents['theoretical_research']['script'])
            
            # Note: En production réelle, utiliser subprocess.run pour isolation
            # Ici, import direct pour démonstration
            import sys
            sys.path.append(self.agents_path)
            
            try:
                from theoretical_research_agent import TheoreticalResearchAgent
                
                # Exécution asynchrone
                async def run_research():
                    agent = TheoreticalResearchAgent()
                    await agent.autonomous_research_cycle()
                    
                # Exécute dans event loop
                asyncio.run(run_research())
                
                # Mise à jour métriques
                self.improvement_metrics['research_cycles_completed'] += 1
                self.improvement_metrics['knowledge_updates'] += 1
                
                self.agents['theoretical_research']['status'] = 'completed'
                
                self._log_orchestrator_event('research_agent_completed', 'SUCCESS', 
                                            'Agent recherche théorique terminé avec succès')
                
                print("✅ Agent Recherche Théorique terminé")
                return True
                
            except Exception as e:
                print(f"❌ Erreur exécution agent recherche: {e}")
                self.agents['theoretical_research']['status'] = 'error'
                
                self._log_orchestrator_event('research_agent_error', 'ERROR', f'Erreur: {e}')
                return False
                
        except Exception as e:
            print(f"❌ Erreur critique agent recherche: {e}")
            return False
            
    def _execute_critic_agent(self) -> bool:
        """Exécute l'agent critique adverse"""
        try:
            print(f"🔥 Lancement Agent Critique Adverse - {datetime.now()}")
            
            # Marquer agent comme running
            self.agents['adversarial_critic']['status'] = 'running'
            self.agents['adversarial_critic']['last_run'] = datetime.now()
            
            # Exécution agent
            script_path = os.path.join(self.agents_path, self.agents['adversarial_critic']['script'])
            
            try:
                import sys
                sys.path.append(self.agents_path)
                
                from adversarial_critic_agent import AdversarialCriticAgent
                
                agent = AdversarialCriticAgent()
                agent.autonomous_criticism_cycle()
                
                # Mise à jour métriques
                self.improvement_metrics['criticism_cycles_completed'] += 1
                self.improvement_metrics['issues_identified'] += len(agent.critical_findings)
                
                self.agents['adversarial_critic']['status'] = 'completed'
                
                self._log_orchestrator_event('critic_agent_completed', 'SUCCESS',
                                           f'Agent critique terminé - {len(agent.critical_findings)} critiques')
                
                print(f"✅ Agent Critique Adverse terminé - {len(agent.critical_findings)} critiques identifiées")
                return True
                
            except Exception as e:
                print(f"❌ Erreur exécution agent critique: {e}")
                self.agents['adversarial_critic']['status'] = 'error'
                
                self._log_orchestrator_event('critic_agent_error', 'ERROR', f'Erreur: {e}')
                return False
                
        except Exception as e:
            print(f"❌ Erreur critique agent critique: {e}")
            return False
            
    def _cross_analysis_research_criticism(self):
        """Analyse croisée entre recherche et critique"""
        print("🔄 Analyse croisée recherche/critique...")
        
        try:
            # Recherche derniers rapports
            research_reports = self._find_latest_reports('theoretical_research_report_')
            critic_reports = self._find_latest_reports('adversarial_criticism_report_')
            
            if not research_reports or not critic_reports:
                print("⚠️ Rapports insuffisants pour analyse croisée")
                return
                
            # Chargement derniers rapports
            latest_research = self._load_latest_report(research_reports)
            latest_critic = self._load_latest_report(critic_reports)
            
            # Analyse croisée
            cross_analysis = {
                'timestamp': datetime.now().isoformat(),
                'research_session': latest_research.get('session_id', 'unknown'),
                'critic_session': latest_critic.get('session_id', 'unknown'),
                'theoretical_gaps_vs_criticisms': self._analyze_gaps_vs_criticisms(latest_research, latest_critic),
                'validation_opportunities': self._find_validation_opportunities(latest_research, latest_critic),
                'contradiction_resolution': self._resolve_contradictions(latest_research, latest_critic),
                'improvement_priorities': self._prioritize_improvements(latest_research, latest_critic)
            }
            
            # Sauvegarde analyse croisée
            cross_analysis_path = f"{self.base_path}/cross_analysis_{self.session_id}.json"
            with open(cross_analysis_path, 'w', encoding='utf-8') as f:
                json.dump(cross_analysis, f, indent=2, ensure_ascii=False)
                
            print(f"✅ Analyse croisée sauvegardée: {cross_analysis_path}")
            
            self._log_orchestrator_event('cross_analysis_completed', 'SUCCESS',
                                       'Analyse croisée recherche/critique terminée')
            
        except Exception as e:
            print(f"❌ Erreur analyse croisée: {e}")
            self._log_orchestrator_event('cross_analysis_error', 'ERROR', f'Erreur: {e}')
            
    def _find_latest_reports(self, prefix: str) -> List[str]:
        """Trouve les derniers rapports d'un type"""
        reports = []
        for file in os.listdir(self.base_path):
            if file.startswith(prefix) and file.endswith('.json'):
                reports.append(os.path.join(self.base_path, file))
        return sorted(reports, key=os.path.getmtime, reverse=True)
        
    def _load_latest_report(self, report_files: List[str]) -> Dict:
        """Charge le dernier rapport d'une liste"""
        if not report_files:
            return {}
            
        try:
            with open(report_files[0], 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Erreur chargement rapport {report_files[0]}: {e}")
            return {}
            
    def _analyze_gaps_vs_criticisms(self, research_data: Dict, critic_data: Dict) -> List[Dict]:
        """Analyse gaps théoriques vs critiques identifiées"""
        correlations = []
        
        research_gaps = research_data.get('theoretical_gaps', [])
        critic_findings = critic_data.get('critical_findings', [])
        
        for gap in research_gaps:
            gap_type = gap.get('gap_type', '')
            
            # Recherche critiques correspondantes
            related_criticisms = []
            for finding in critic_findings:
                if any(keyword in finding.get('issue', '').lower() 
                      for keyword in gap_type.lower().split('_')):
                    related_criticisms.append(finding.get('issue', ''))
                    
            if related_criticisms:
                correlations.append({
                    'theoretical_gap': gap_type,
                    'gap_severity': gap.get('severity', 'UNKNOWN'),
                    'related_criticisms': related_criticisms,
                    'correlation_strength': 'HIGH' if len(related_criticisms) > 2 else 'MEDIUM',
                    'action_priority': 'URGENT' if gap.get('severity') == 'HIGH' else 'MEDIUM'
                })
                
        return correlations
        
    def _find_validation_opportunities(self, research_data: Dict, critic_data: Dict) -> List[Dict]:
        """Trouve opportunités validation entre recherche et défenses"""
        opportunities = []
        
        validations = research_data.get('validation_opportunities', [])
        defensive_responses = critic_data.get('defensive_responses', [])
        
        for validation in validations:
            # Recherche défenses qui pourraient être renforcées par cette validation
            for defense in defensive_responses:
                if validation.get('validation_type', '') in defense.get('defense_arguments', []):
                    opportunities.append({
                        'validation_paper': validation.get('paper_title', ''),
                        'defense_topic': defense.get('original_critique', ''),
                        'reinforcement_potential': 'HIGH' if validation.get('strength') == 'STRONG' else 'MEDIUM',
                        'action': 'Citer ce paper pour renforcer défense'
                    })
                    
        return opportunities
        
    def _resolve_contradictions(self, research_data: Dict, critic_data: Dict) -> List[Dict]:
        """Résout contradictions entre recherche positive et critiques"""
        resolutions = []
        
        key_findings = research_data.get('key_findings', [])
        contradictions = critic_data.get('critical_findings', [])
        
        for finding in key_findings:
            finding_topic = finding.get('title', '').lower()
            
            # Recherche critiques contradictoires
            conflicting_criticisms = []
            for criticism in contradictions:
                if any(keyword in criticism.get('issue', '').lower() 
                      for keyword in finding_topic.split()[:3]):  # Premiers mots titre
                    conflicting_criticisms.append(criticism)
                    
            if conflicting_criticisms:
                resolutions.append({
                    'positive_finding': finding.get('title', ''),
                    'conflicting_criticisms': [c.get('issue', '') for c in conflicting_criticisms],
                    'resolution_strategy': 'Approfondir recherche pour réconcilier perspectives',
                    'confidence_gap': 'HIGH' if len(conflicting_criticisms) > 1 else 'MEDIUM'
                })
                
        return resolutions
        
    def _prioritize_improvements(self, research_data: Dict, critic_data: Dict) -> List[Dict]:
        """Priorise améliorations basées sur recherche + critique"""
        priorities = []
        
        # Gaps théoriques haute priorité
        for gap in research_data.get('theoretical_gaps', []):
            if gap.get('severity') == 'HIGH':
                priorities.append({
                    'type': 'theoretical_gap',
                    'description': gap.get('description', ''),
                    'priority_score': 10,
                    'source': 'research_agent'
                })
                
        # Critiques critiques
        for finding in critic_data.get('critical_findings', []):
            if finding.get('severity') == 'CRITICAL':
                priorities.append({
                    'type': 'critical_issue',
                    'description': finding.get('issue', ''),
                    'priority_score': 9,
                    'source': 'critic_agent'
                })
                
        # Tri par score priorité
        priorities.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return priorities[:10]  # Top 10
        
    def _generate_daily_report(self):
        """Génère rapport quotidien état système"""
        print(f"📊 Génération rapport quotidien - {datetime.now()}")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'orchestrator_session': self.session_id,
            'agents_status': self.agents.copy(),
            'improvement_metrics': self.improvement_metrics.copy(),
            'recent_activity': self._get_recent_activity(),
            'next_scheduled_actions': self._get_next_scheduled_actions(),
            'system_health': self._assess_system_health(),
            'recommendations': self._generate_daily_recommendations()
        }
        
        # Sauvegarde
        daily_report_path = f"{self.base_path}/daily_improvement_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(daily_report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Rapport quotidien sauvegardé: {daily_report_path}")
        
        # Rapport console
        self._print_daily_summary(report)
        
    def _get_recent_activity(self) -> List[Dict]:
        """Récupère activité récente (24h)"""
        recent_threshold = datetime.now() - timedelta(hours=24)
        
        recent_activity = []
        for event in self.orchestrator_log:
            event_time = datetime.fromisoformat(event.get('timestamp', ''))
            if event_time >= recent_threshold:
                recent_activity.append(event)
                
        return recent_activity
        
    def _get_next_scheduled_actions(self) -> List[Dict]:
        """Récupère prochaines actions programmées"""
        next_actions = []
        
        # Calcul prochaines exécutions
        now = datetime.now()
        
        # Prochaine recherche (dimanche)
        days_until_sunday = (6 - now.weekday()) % 7
        if days_until_sunday == 0:  # Aujourd'hui dimanche
            days_until_sunday = 7
            
        next_research = now + timedelta(days=days_until_sunday)
        next_research = next_research.replace(hour=2, minute=0, second=0, microsecond=0)
        
        next_actions.append({
            'action': 'Agent Recherche Théorique',
            'scheduled_time': next_research.isoformat(),
            'frequency': 'weekly'
        })
        
        # Prochaine critique (demain)
        next_critic = (now + timedelta(days=1)).replace(hour=1, minute=0, second=0, microsecond=0)
        
        next_actions.append({
            'action': 'Agent Critique Adverse',
            'scheduled_time': next_critic.isoformat(),
            'frequency': 'daily'
        })
        
        return next_actions
        
    def _assess_system_health(self) -> Dict:
        """Évalue santé du système d'amélioration continue"""
        health = {
            'overall_status': 'UNKNOWN',
            'agents_operational': 0,
            'recent_errors': 0,
            'improvement_trend': 'STABLE',
            'issues': []
        }
        
        # Statut agents
        for agent_name, agent_data in self.agents.items():
            if agent_data.get('status') in ['completed', 'idle']:
                health['agents_operational'] += 1
            elif agent_data.get('status') == 'error':
                health['issues'].append(f"Agent {agent_name} en erreur")
                
        # Erreurs récentes
        recent_threshold = datetime.now() - timedelta(hours=24)
        for event in self.orchestrator_log:
            if (event.get('level') == 'ERROR' and 
                datetime.fromisoformat(event.get('timestamp', '')) >= recent_threshold):
                health['recent_errors'] += 1
                
        # Statut global
        if health['agents_operational'] == len(self.agents) and health['recent_errors'] == 0:
            health['overall_status'] = 'HEALTHY'
        elif health['recent_errors'] > 3:
            health['overall_status'] = 'CRITICAL'
        else:
            health['overall_status'] = 'WARNING'
            
        return health
        
    def _generate_daily_recommendations(self) -> List[str]:
        """Génère recommandations quotidiennes"""
        recommendations = []
        
        # Basé sur métriques
        if self.improvement_metrics['issues_identified'] > self.improvement_metrics['issues_resolved']:
            recommendations.append("Prioriser résolution des issues identifiées par agent critique")
            
        if self.improvement_metrics['research_cycles_completed'] == 0:
            recommendations.append("Lancer cycle recherche théorique pour mise à jour connaissances")
            
        if self.improvement_metrics['theoretical_gaps_closed'] == 0:
            recommendations.append("Adresser gaps théoriques identifiés")
            
        # Recommandations par défaut
        if not recommendations:
            recommendations.append("Système fonctionnel - Continuer monitoring automatique")
            
        return recommendations
        
    def _print_daily_summary(self, report: Dict):
        """Affiche résumé quotidien en console"""
        print("\n" + "="*60)
        print("📊 RÉSUMÉ QUOTIDIEN AMÉLIORATION CONTINUE")
        print("="*60)
        
        # Statut agents
        print("\n🤖 STATUT AGENTS:")
        for agent, data in report['agents_status'].items():
            status_emoji = {"idle": "💤", "running": "🏃", "completed": "✅", "error": "❌"}
            emoji = status_emoji.get(data.get('status', 'unknown'), "❓")
            print(f"  {emoji} {agent}: {data.get('status', 'unknown')}")
            
        # Métriques
        print("\n📈 MÉTRIQUES:")
        metrics = report['improvement_metrics']
        print(f"  🔬 Cycles recherche: {metrics['research_cycles_completed']}")
        print(f"  🔥 Cycles critique: {metrics['criticism_cycles_completed']}")
        print(f"  🐛 Issues identifiées: {metrics['issues_identified']}")
        print(f"  ✅ Issues résolues: {metrics['issues_resolved']}")
        
        # Santé système
        print(f"\n🏥 SANTÉ SYSTÈME: {report['system_health']['overall_status']}")
        
        # Recommandations
        print("\n💡 RECOMMANDATIONS:")
        for rec in report['recommendations']:
            print(f"  • {rec}")
            
        print("\n" + "="*60)
        
    def _continuous_monitoring(self):
        """Monitoring continu du système avec surveillance GitHub"""
        while self.is_running:
            try:
                # Vérification agents
                self._check_agents_health()
                
                # Surveillance GitHub workflows (toutes les 15 minutes)
                if datetime.now().minute % 15 == 0:
                    self._monitor_github_workflows()
                
                # Exécution tâches programmées
                schedule.run_pending()
                
                # Pause
                time.sleep(60)  # Vérification chaque minute
                
            except Exception as e:
                print(f"⚠️ Erreur monitoring: {e}")
                self._log_orchestrator_event('monitoring_error', 'ERROR', f'Erreur: {e}')
                time.sleep(300)  # Pause plus longue en cas d'erreur
                
    def _check_agents_health(self):
        """Vérifie santé des agents"""
        for agent_name, agent_data in self.agents.items():
            # Vérification timeout
            if agent_data.get('status') == 'running':
                if agent_data.get('last_run'):
                    last_run = agent_data['last_run']
                    if isinstance(last_run, str):
                        last_run = datetime.fromisoformat(last_run)
                        
                    # Timeout après 2h
                    if datetime.now() - last_run > timedelta(hours=2):
                        print(f"⚠️ Agent {agent_name} en timeout - Reset status")
                        agent_data['status'] = 'error'
                        self._log_orchestrator_event('agent_timeout', 'WARNING', 
                                                   f'Agent {agent_name} timeout')
                        
    def _main_orchestration_loop(self):
        """Loop principal d'orchestration"""
        print("\n🔄 LOOP PRINCIPAL ORCHESTRATEUR DÉMARRÉ")
        print("   Appuyez Ctrl+C pour arrêter")
        
        try:
            while self.is_running:
                time.sleep(10)  # Loop principal léger
                
        except KeyboardInterrupt:
            print("\n🛑 Interruption détectée")
            
    def stop_autonomous_operation(self):
        """Arrête opération autonome"""
        print("\n🛑 ARRÊT ORCHESTRATEUR AMÉLIORATION CONTINUE")
        
        self.is_running = False
        
        # Rapport final
        final_report = {
            'session_id': self.session_id,
            'stop_timestamp': datetime.now().isoformat(),
            'total_runtime': self._calculate_runtime(),
            'final_metrics': self.improvement_metrics.copy(),
            'agents_final_status': self.agents.copy(),
            'total_events': len(self.orchestrator_log)
        }
        
        final_path = f"{self.base_path}/orchestrator_final_report_{self.session_id}.json"
        with open(final_path, 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False)
            
        print(f"📊 Rapport final sauvegardé: {final_path}")
        print("✅ Orchestrateur arrêté proprement")
        
    def _calculate_runtime(self) -> str:
        """Calcule temps d'exécution total"""
        if self.orchestrator_log:
            start_time = datetime.fromisoformat(self.orchestrator_log[0]['timestamp'])
            end_time = datetime.now()
            runtime = end_time - start_time
            return f"{runtime.total_seconds():.0f} seconds"
        return "Unknown"
        
    def _log_orchestrator_event(self, event_type: str, level: str, message: str):
        """Log événement orchestrateur"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'level': level,
            'message': message,
            'session_id': self.session_id
        }
        
        self.orchestrator_log.append(event)
        
        # Log console si important
        if level in ['ERROR', 'WARNING']:
            level_emoji = {'ERROR': '❌', 'WARNING': '⚠️', 'INFO': 'ℹ️'}
            emoji = level_emoji.get(level, 'ℹ️')
            print(f"{emoji} [{level}] {message}")
            
    def _generate_comprehensive_report(self):
        """Génère rapport compréhensif initial"""
        print("📊 Génération rapport compréhensif...")
        
        comprehensive_report = {
            'orchestrator_session': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'initialization_summary': {
                'agents_configured': len(self.agents),
                'scheduling_active': True,
                'monitoring_active': True,
                'initial_cycle_completed': True
            },
            'agents_capabilities': {
                'theoretical_research': {
                    'description': 'Recherche bibliographique automatisée',
                    'apis_used': ['arxiv', 'semantic_scholar', 'openalex'],
                    'update_frequency': 'weekly',
                    'knowledge_domains': ['panini_grammar', 'melcuk_theory', 'semantic_compression']
                },
                'adversarial_critic': {
                    'description': 'Critique constructive multi-dimensionnelle',
                    'analysis_categories': ['theoretical', 'technical', 'scientific', 'commercial'],
                    'criticism_frequency': 'daily',
                    'improvement_focus': 'continuous_quality_enhancement'
                }
            },
            'improvement_framework': {
                'research_to_validation_pipeline': 'Recherche → Validation → Application',
                'criticism_to_improvement_cycle': 'Critique → Défense → Amélioration → Re-critique',
                'cross_validation': 'Recherche vs Critique pour cohérence',
                'autonomous_operation': '100% externalisé et programmé'
            },
            'success_metrics': {
                'knowledge_currency': 'Mise à jour régulière connaissances théoriques',
                'quality_improvement': 'Réduction continue issues identifiées',
                'credibility_enhancement': 'Validation externe et peer review',
                'innovation_validation': 'Confirmation originalité et valeur ajoutée'
            }
        }
        
        # Sauvegarde
        comprehensive_path = f"{self.base_path}/comprehensive_ci_report_{self.session_id}.json"
        with open(comprehensive_path, 'w', encoding='utf-8') as f:
            json.dump(comprehensive_report, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Rapport compréhensif sauvegardé: {comprehensive_path}")

def main():
    """Fonction principale"""
    orchestrator = ContinuousImprovementOrchestrator()
    
    print("🤖 ORCHESTRATEUR AMÉLIORATION CONTINUE PANINI")
    print("Objectif: Recherche théorique + Critique adverse autonomes")
    print("Mode: 100% externalisé et programmé")
    print("=" * 60)
    
    try:
        orchestrator.start_autonomous_operation()
    except Exception as e:
        print(f"❌ Erreur critique orchestrateur: {e}")
    finally:
        orchestrator.stop_autonomous_operation()

if __name__ == "__main__":
    main()
