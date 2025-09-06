#!/usr/bin/env python3
"""
🔍 Simple Monitor PaniniFS
Surveillance services + alertes Discord
"""

import requests
import json
import time
import os
from datetime import datetime

class SimpleMonitor:
    def __init__(self):
        # Configuration Discord webhook (à définir)
        self.discord_webhook = os.getenv('DISCORD_WEBHOOK_URL', '')
        self.services = {
            'github_actions': 'https://api.github.com/repos/stephanedenis/PaniniFS/actions/runs',
            'oracle_vm': 'http://YOUR_ORACLE_IP:8080/health',  # À configurer
            'consensus_data': 'https://paninifs.org/data/latest_consensus.json'
        }
    
    def check_service(self, name, url):
        """Vérification état service"""
        try:
            response = requests.get(url, timeout=10)
            return {
                'name': name,
                'status': 'UP' if response.status_code == 200 else 'DOWN',
                'response_time': response.elapsed.total_seconds(),
                'status_code': response.status_code
            }
        except Exception as e:
            return {
                'name': name,
                'status': 'ERROR',
                'error': str(e)
            }
    
    def send_discord_alert(self, message):
        """Envoi alerte Discord"""
        if not self.discord_webhook:
            print(f"📢 ALERT: {message}")
            return
        
        payload = {
            'content': f"🚨 **PaniniFS Alert** 🚨\n{message}",
            'username': 'PaniniFS Monitor'
        }
        
        try:
            requests.post(self.discord_webhook, json=payload)
        except Exception as e:
            print(f"❌ Failed to send Discord alert: {e}")
    
    def run_monitoring_cycle(self):
        """Cycle monitoring complet"""
        results = []
        
        for name, url in self.services.items():
            result = self.check_service(name, url)
            results.append(result)
            
            # Alerte si service down
            if result['status'] != 'UP':
                self.send_discord_alert(f"Service {name} is {result['status']}")
        
        # Sauvegarde résultats
        timestamp = datetime.now().isoformat()
        monitoring_data = {
            'timestamp': timestamp,
            'results': results
        }
        
        with open('monitoring_results.json', 'w') as f:
            json.dump(monitoring_data, f, indent=2)
        
        print(f"✅ Monitoring cycle completed at {timestamp}")
        return results

if __name__ == "__main__":
    monitor = SimpleMonitor()
    
    # Run monitoring loop
    while True:
        try:
            monitor.run_monitoring_cycle()
            time.sleep(300)  # Check every 5 minutes
        except KeyboardInterrupt:
            print("🛑 Monitoring stopped")
            break
        except Exception as e:
            print(f"❌ Monitoring error: {e}")
            time.sleep(60)  # Wait 1 minute on error
