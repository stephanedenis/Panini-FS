#!/usr/bin/env python3
"""
🔔 SYSTÈME NOTIFICATIONS FIREBASE FCM
Notifications Android autonomes pour monitoring PaniniFS
"""

import json
import requests
import time
from datetime import datetime
from typing import Dict, List, Optional
import logging

class FirebaseNotificationService:
    def __init__(self, server_key: str = None, project_id: str = None):
        """
        Initialise le service FCM
        
        Args:
            server_key: Clé serveur Firebase (ou via config)
            project_id: ID projet Firebase (ou via config)
        """
        # Configuration logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.server_key = server_key or self._load_config().get('server_key')
        self.project_id = project_id or self._load_config().get('project_id')
        self.fcm_url = "https://fcm.googleapis.com/fcm/send"
        
    def _load_config(self) -> Dict:
        """Charge la configuration Firebase depuis fichier"""
        try:
            with open('firebase_config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning("firebase_config.json non trouvé - utilise variables env")
            return {}
    
    def send_notification(self, 
                         title: str, 
                         body: str, 
                         topic: str = "panini_monitoring",
                         data: Dict = None,
                         priority: str = "high") -> bool:
        """
        Envoie une notification FCM
        
        Args:
            title: Titre de la notification
            body: Corps du message
            topic: Topic FCM (default: panini_monitoring)
            data: Données additionnelles
            priority: Priorité (high/normal)
            
        Returns:
            bool: Succès de l'envoi
        """
        if not self.server_key:
            self.logger.error("Clé serveur Firebase manquante")
            return False
            
        headers = {
            'Authorization': f'key={self.server_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'to': f'/topics/{topic}',
            'priority': priority,
            'notification': {
                'title': title,
                'body': body,
                'icon': 'ic_notification_panini',
                'color': '#3498db',
                'sound': 'default',
                'tag': 'panini_domain_status'
            },
            'data': data or {}
        }
        
        try:
            response = requests.post(self.fcm_url, 
                                   headers=headers, 
                                   json=payload, 
                                   timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success', 0) > 0:
                    self.logger.info(f"✅ Notification envoyée: {title}")
                    return True
                else:
                    self.logger.error(f"❌ Échec FCM: {result}")
                    return False
            else:
                self.logger.error(f"❌ Erreur HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Exception envoi FCM: {e}")
            return False
    
    def notify_domain_status(self, domain: str, status: str, details: Dict = None):
        """Notification spécialisée pour statut domaine"""
        
        emoji_map = {
            'online': '✅',
            'ssl_error': '⚠️',
            'offline': '❌',
            'deploying': '🚀'
        }
        
        emoji = emoji_map.get(status, '📊')
        
        title = f"{emoji} {domain.upper()}"
        
        if status == 'online':
            body = f"Domaine opérationnel - {details.get('response_time', 'N/A')}ms"
        elif status == 'ssl_error':
            body = f"Certificat SSL en attente - Code {details.get('http_code', 'N/A')}"
        elif status == 'offline':
            body = f"Domaine inaccessible - Vérification requise"
        elif status == 'deploying':
            body = f"Déploiement en cours - {details.get('phase', 'Phase inconnue')}"
        else:
            body = f"Statut: {status}"
            
        data = {
            'domain': domain,
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'details': json.dumps(details or {})
        }
        
        return self.send_notification(title, body, data=data)
    
    def notify_agent_activity(self, agent_name: str, action: str, status: str):
        """Notification pour activité des agents"""
        title = f"🤖 Agent {agent_name}"
        body = f"{action} - {status}"
        
        data = {
            'type': 'agent_activity',
            'agent': agent_name,
            'action': action,
            'status': status,
            'timestamp': datetime.now().isoformat()
        }
        
        return self.send_notification(title, body, topic="panini_agents", data=data)
    
    def notify_deployment_complete(self, domains: List[str], success_count: int):
        """Notification de fin de déploiement"""
        total = len(domains)
        emoji = "🎉" if success_count == total else "⚠️"
        
        title = f"{emoji} Déploiement Terminé"
        body = f"{success_count}/{total} domaines opérationnels"
        
        data = {
            'type': 'deployment_complete',
            'domains': domains,
            'success_count': success_count,
            'total_count': total,
            'timestamp': datetime.now().isoformat()
        }
        
        return self.send_notification(title, body, 
                                    topic="panini_deployments", 
                                    data=data, 
                                    priority="high")

class NotificationManager:
    """Gestionnaire principal des notifications"""
    
    def __init__(self):
        self.fcm = FirebaseNotificationService()
        self.last_notifications = {}  # Évite le spam
        
    def should_notify(self, key: str, interval_minutes: int = 5) -> bool:
        """Vérifie si on doit notifier (évite le spam)"""
        now = datetime.now()
        last_time = self.last_notifications.get(key)
        
        if not last_time:
            self.last_notifications[key] = now
            return True
            
        diff = (now - last_time).total_seconds() / 60
        if diff >= interval_minutes:
            self.last_notifications[key] = now
            return True
            
        return False
    
    def process_domain_monitoring_report(self, report: Dict):
        """Traite un rapport de monitoring et envoie notifications appropriées"""
        
        summary = report.get('summary', {})
        domains = report.get('domains', [])
        
        # Notification globale si changement significatif
        total = summary.get('total', 0)
        online = summary.get('online', 0)
        
        status_key = f"global_status_{online}_{total}"
        if self.should_notify(status_key, interval_minutes=15):
            if online == total:
                self.fcm.notify_deployment_complete([d['domain'] for d in domains], online)
            elif online == 0:
                self.fcm.send_notification("🚨 Alerte Système", 
                                         "Aucun domaine accessible", 
                                         priority="high")
        
        # Notifications par domaine pour changements d'état
        for domain_data in domains:
            domain = domain_data['domain']
            status = domain_data['status']
            
            domain_key = f"{domain}_{status}"
            if self.should_notify(domain_key, interval_minutes=10):
                self.fcm.notify_domain_status(domain, status, domain_data)

# Configuration par défaut
def create_firebase_config_template():
    """Crée un template de configuration Firebase"""
    config = {
        "server_key": "VOTRE_SERVER_KEY_FIREBASE",
        "project_id": "panini-ecosystem",
        "topics": {
            "monitoring": "panini_monitoring",
            "agents": "panini_agents", 
            "deployments": "panini_deployments"
        },
        "notification_settings": {
            "domain_check_interval": 5,
            "agent_activity_interval": 10,
            "deployment_interval": 15
        }
    }
    
    with open('firebase_config_template.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("📝 Template de configuration créé: firebase_config_template.json")
    print("👆 Renommer en firebase_config.json et remplir les valeurs")

if __name__ == "__main__":
    # Test du système de notifications
    
    print("🔔 SYSTÈME NOTIFICATIONS FIREBASE FCM")
    print("=" * 50)
    
    # Crée le template de configuration
    create_firebase_config_template()
    
    # Test avec configuration fictive
    notif_manager = NotificationManager()
    
    # Simulation d'un rapport de monitoring
    test_report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total': 5,
            'online': 3,
            'ssl_errors': 2,
            'offline': 0
        },
        'domains': [
            {
                'domain': 'paninifs.com',
                'status': 'online',
                'response_time': 0.145,
                'http_code': 200
            },
            {
                'domain': 'o-tomate.com', 
                'status': 'ssl_error',
                'http_code': 404
            }
        ]
    }
    
    print("📊 Test avec rapport de monitoring fictif...")
    notif_manager.process_domain_monitoring_report(test_report)
    
    print("\n✅ Configuration FCM prête!")
    print("📱 Prochaine étape: Configuration Android Studio")
