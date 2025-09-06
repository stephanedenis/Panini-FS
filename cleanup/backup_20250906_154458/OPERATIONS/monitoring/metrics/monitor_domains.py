#!/usr/bin/env python3
"""
🤖 MONITORING AUTONOME DOMAINES PANINI
Surveillance continue avec notifications FCM
"""

import requests
import time
import json
from datetime import datetime
import subprocess

# Import du système de notifications
try:
    from firebase_notifications import NotificationManager
    NOTIFICATIONS_ENABLED = True
except ImportError:
    NOTIFICATIONS_ENABLED = False
    print("⚠️ Module firebase_notifications non disponible - notifications désactivées")

class DomainMonitor:
    def __init__(self):
        self.domains = [
            'paninifs.com',
            'o-tomate.com', 
            'stephanedenis.cc',
            'sdenis.net',
            'paninifs.org'
        ]
        
        # Gestionnaire de notifications
        if NOTIFICATIONS_ENABLED:
            self.notif_manager = NotificationManager()
        
    def check_domain_status(self, domain):
        """Test autonome d'un domaine"""
        result = {
            'domain': domain,
            'timestamp': datetime.now().isoformat(),
            'status': 'unknown',
            'http_code': None,
            'response_time': None,
            'ssl_valid': False,
            'redirect_url': None
        }
        
        try:
            # Test HTTPS d'abord
            response = requests.get(f'https://{domain}', 
                                  timeout=10, 
                                  allow_redirects=True,
                                  verify=True)
            
            result['status'] = 'online'
            result['http_code'] = response.status_code
            result['response_time'] = response.elapsed.total_seconds()
            result['ssl_valid'] = True
            
            if response.history:
                result['redirect_url'] = response.url
                
        except requests.exceptions.SSLError:
            # Si SSL échoue, test HTTP
            try:
                response = requests.get(f'http://{domain}', 
                                      timeout=10, 
                                      allow_redirects=False)
                result['status'] = 'ssl_error'
                result['http_code'] = response.status_code
                result['response_time'] = response.elapsed.total_seconds()
                
            except Exception as e:
                result['status'] = 'offline'
                result['error'] = str(e)
                
        except Exception as e:
            result['status'] = 'offline'
            result['error'] = str(e)
            
        return result
    
    def check_github_pages_status(self):
        """Vérification du statut GitHub Pages via API"""
        try:
            # Vérifier le statut des GitHub Pages
            response = requests.get(
                'https://api.github.com/repos/stephanedenis/PaniniFS/pages',
                headers={'Accept': 'application/vnd.github.v3+json'}
            )
            
            if response.status_code == 200:
                pages_info = response.json()
                return {
                    'status': pages_info.get('status'),
                    'url': pages_info.get('html_url'),
                    'custom_domain': pages_info.get('cname'),
                    'source': pages_info.get('source', {})
                }
            else:
                return {'error': f'API error: {response.status_code}'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def run_monitoring_cycle(self):
        """Cycle de monitoring autonome avec notifications"""
        print("🤖 MONITORING AUTONOME - DÉMARRAGE")
        print("=" * 50)
        
        # Status GitHub Pages
        gh_status = self.check_github_pages_status()
        print(f"📊 GitHub Pages: {gh_status}")
        
        # Test chaque domaine
        results = []
        for domain in self.domains:
            print(f"\n🔍 Test: {domain}")
            status = self.check_domain_status(domain)
            results.append(status)
            
            if status['status'] == 'online':
                print(f"  ✅ {status['http_code']} - {status['response_time']:.2f}s")
            elif status['status'] == 'ssl_error':
                print(f"  ⚠️  HTTP OK but SSL error - Code: {status['http_code']}")
            else:
                print(f"  ❌ {status['status']}")
                if 'error' in status:
                    print(f"     Error: {status['error']}")
        
        # Sauvegarde des résultats
        report = {
            'timestamp': datetime.now().isoformat(),
            'github_pages': gh_status,
            'domains': results,
            'summary': {
                'total': len(results),
                'online': len([r for r in results if r['status'] == 'online']),
                'ssl_errors': len([r for r in results if r['status'] == 'ssl_error']),
                'offline': len([r for r in results if r['status'] == 'offline'])
            }
        }
        
        with open('domain_monitoring_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Envoi des notifications FCM
        if NOTIFICATIONS_ENABLED:
            self.notif_manager.process_domain_monitoring_report(report)
        
        print(f"\n📋 RÉSUMÉ:")
        print(f"   ✅ En ligne: {report['summary']['online']}/{report['summary']['total']}")
        print(f"   ⚠️  SSL Error: {report['summary']['ssl_errors']}")
        print(f"   ❌ Hors ligne: {report['summary']['offline']}")
        
        if NOTIFICATIONS_ENABLED:
            print(f"   📱 Notifications envoyées")
        
        return report

import requests
import time
import json
from datetime import datetime
import subprocess
from notification_system import PaniniNotificationSystem

class DomainMonitor:
    def __init__(self):
        self.domains = [
            'paninifs.com',
            'o-tomate.com', 
            'stephanedenis.cc',
            'sdenis.net',
            'paninifs.org'
        ]
        
        # Système de notifications
        self.notifier = PaniniNotificationSystem()
        self.last_status = None  # Pour détecter les changements
        
    def check_domain_status(self, domain):
        """Test autonome d'un domaine"""
        result = {
            'domain': domain,
            'timestamp': datetime.now().isoformat(),
            'status': 'unknown',
            'http_code': None,
            'response_time': None,
            'ssl_valid': False,
            'redirect_url': None
        }
        
        try:
            # Test HTTPS d'abord
            response = requests.get(f'https://{domain}', 
                                  timeout=10, 
                                  allow_redirects=True,
                                  verify=True)
            
            result['status'] = 'online'
            result['http_code'] = response.status_code
            result['response_time'] = response.elapsed.total_seconds()
            result['ssl_valid'] = True
            
            if response.history:
                result['redirect_url'] = response.url
                
        except requests.exceptions.SSLError:
            # Si SSL échoue, test HTTP
            try:
                response = requests.get(f'http://{domain}', 
                                      timeout=10, 
                                      allow_redirects=False)
                result['status'] = 'ssl_error'
                result['http_code'] = response.status_code
                result['response_time'] = response.elapsed.total_seconds()
                
            except Exception as e:
                result['status'] = 'offline'
                result['error'] = str(e)
                
        except Exception as e:
            result['status'] = 'offline'
            result['error'] = str(e)
            
        return result
    
    def check_github_pages_status(self):
        """Vérification du statut GitHub Pages via API"""
        try:
            # Vérifier le statut des GitHub Pages
            response = requests.get(
                'https://api.github.com/repos/stephanedenis/PaniniFS/pages',
                headers={'Accept': 'application/vnd.github.v3+json'}
            )
            
            if response.status_code == 200:
                pages_info = response.json()
                return {
                    'status': pages_info.get('status'),
                    'url': pages_info.get('html_url'),
                    'custom_domain': pages_info.get('cname'),
                    'source': pages_info.get('source', {})
                }
            else:
                return {'error': f'API error: {response.status_code}'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def run_monitoring_cycle(self):
        """Cycle de monitoring autonome"""
        print("🤖 MONITORING AUTONOME - DÉMARRAGE")
        print("=" * 50)
        
        # Status GitHub Pages
        gh_status = self.check_github_pages_status()
        print(f"📊 GitHub Pages: {gh_status}")
        
        # Test chaque domaine
        results = []
        for domain in self.domains:
            print(f"\n🔍 Test: {domain}")
            status = self.check_domain_status(domain)
            results.append(status)
            
            if status['status'] == 'online':
                print(f"  ✅ {status['http_code']} - {status['response_time']:.2f}s")
            elif status['status'] == 'ssl_error':
                print(f"  ⚠️  HTTP OK but SSL error - Code: {status['http_code']}")
            else:
                print(f"  ❌ {status['status']}")
                if 'error' in status:
                    print(f"     Error: {status['error']}")
        
        # Sauvegarde des résultats
        report = {
            'timestamp': datetime.now().isoformat(),
            'github_pages': gh_status,
            'domains': results,
            'summary': {
                'total': len(results),
                'online': len([r for r in results if r['status'] == 'online']),
                'ssl_errors': len([r for r in results if r['status'] == 'ssl_error']),
                'offline': len([r for r in results if r['status'] == 'offline'])
            }
        }
        
        with open('domain_monitoring_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # 🔔 NOTIFICATIONS AUTOMATIQUES
        self.check_and_notify(report)
        
        print(f"\n📋 RÉSUMÉ:")
        print(f"   ✅ En ligne: {report['summary']['online']}/{report['summary']['total']}")
        print(f"   ⚠️  SSL Error: {report['summary']['ssl_errors']}")
        print(f"   ❌ Hors ligne: {report['summary']['offline']}")
        
        return report
    
    def check_and_notify(self, current_report):
        """Vérifier changements et envoyer notifications"""
        try:
            # Charger le dernier rapport
            try:
                with open('last_domain_status.json', 'r') as f:
                    self.last_status = json.load(f)
            except FileNotFoundError:
                self.last_status = None
            
            # Détecter changements significatifs
            should_notify = False
            notification_type = "unknown"
            
            if self.last_status is None:
                # Premier run
                should_notify = True
                notification_type = "initial"
            else:
                old_online = self.last_status['summary']['online']
                new_online = current_report['summary']['online']
                
                if old_online != new_online:
                    should_notify = True
                    if new_online > old_online:
                        notification_type = "improvement"
                    else:
                        notification_type = "degradation"
                elif new_online == len(self.domains):
                    # Tous en ligne - notification périodique (toutes les 4h)
                    last_time = datetime.fromisoformat(self.last_status['timestamp'])
                    now = datetime.now()
                    if (now - last_time).total_seconds() > 14400:  # 4 heures
                        should_notify = True
                        notification_type = "periodic_success"
            
            # Envoyer notification si nécessaire
            if should_notify:
                print(f"🔔 Envoi notification ({notification_type})")
                self.notifier.notify_domain_status(current_report)
            
            # Sauvegarder le statut actuel
            with open('last_domain_status.json', 'w') as f:
                json.dump(current_report, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ Erreur notifications: {e}")
    
    def start_continuous_monitoring(self, interval_minutes=15):
        """Démarrage monitoring continu avec notifications"""
        print(f"🔄 MONITORING CONTINU - Interval: {interval_minutes} minutes")
        print("   Ctrl+C pour arrêter")
        
        try:
            while True:
                print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} - Cycle monitoring")
                self.run_monitoring_cycle()
                
                print(f"😴 Pause {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring arrêté par l'utilisateur")

if __name__ == "__main__":
    monitor = DomainMonitor()
    monitor.run_monitoring_cycle()
