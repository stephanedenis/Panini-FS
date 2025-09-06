#!/usr/bin/env python3
"""
🔔 NOTIFICATION SYSTEM - PANINI ECOSYSTEM
Notifications FCM pour monitoring domaines
"""

import requests
import json
from datetime import datetime
import time

class PaniniNotificationSystem:
    def __init__(self):
        # Configuration FCM (à personnaliser)
        self.fcm_server_key = "YOUR_FCM_SERVER_KEY"  # Depuis Firebase Console
        self.device_token = "YOUR_DEVICE_TOKEN"      # Token de ton Android
        
        self.fcm_url = "https://fcm.googleapis.com/fcm/send"
        
        # Topics pour différents types de notifications
        self.topics = {
            'domains': '/topics/panini_domains',
            'agents': '/topics/panini_agents', 
            'critical': '/topics/panini_critical'
        }
        
    def send_fcm_notification(self, title, body, topic=None, device_token=None, data=None):
        """Envoi notification FCM"""
        
        headers = {
            'Authorization': f'key={self.fcm_server_key}',
            'Content-Type': 'application/json'
        }
        
        # Payload notification
        payload = {
            'notification': {
                'title': title,
                'body': body,
                'icon': 'ic_panini',
                'sound': 'default',
                'click_action': 'FLUTTER_NOTIFICATION_CLICK'
            }
        }
        
        # Ajouter données personnalisées
        if data:
            payload['data'] = data
            
        # Destination : topic ou device spécifique
        if topic:
            payload['to'] = topic
        elif device_token:
            payload['to'] = device_token
        else:
            payload['to'] = self.device_token
            
        try:
            response = requests.post(self.fcm_url, 
                                   headers=headers, 
                                   data=json.dumps(payload))
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Notification envoyée: {result.get('success', 0)} succès")
                return True
            else:
                print(f"❌ Erreur FCM: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur notification: {e}")
            return False
    
    def notify_domain_status(self, domain_report):
        """Notification pour statut domaines"""
        summary = domain_report['summary']
        total = summary['total']
        online = summary['online']
        
        if online == total:
            # Tous en ligne - notification success
            self.send_fcm_notification(
                title="🎉 Écosystème Panini - Opérationnel",
                body=f"Tous les domaines ({total}) sont en ligne !",
                topic=self.topics['domains'],
                data={
                    'type': 'domain_success',
                    'online_count': str(online),
                    'total_count': str(total),
                    'timestamp': domain_report['timestamp']
                }
            )
        elif online > 0:
            # Partiellement en ligne - notification warning
            self.send_fcm_notification(
                title="⚠️ Domaines Panini - Partiel",
                body=f"{online}/{total} domaines opérationnels",
                topic=self.topics['domains'],
                data={
                    'type': 'domain_partial',
                    'online_count': str(online),
                    'total_count': str(total)
                }
            )
        else:
            # Tous hors ligne - notification critique
            self.send_fcm_notification(
                title="🚨 Écosystème Panini - Critique",
                body="Aucun domaine accessible !",
                topic=self.topics['critical'],
                data={
                    'type': 'domain_critical',
                    'total_count': str(total)
                }
            )
    
    def notify_agent_activity(self, agent_report):
        """Notification pour activité agents"""
        active_agents = len([a for a in agent_report.get('agents', []) 
                           if a.get('status') == 'active'])
        
        self.send_fcm_notification(
            title="🤖 Agents Panini",
            body=f"{active_agents} agents actifs dans l'écosystème",
            topic=self.topics['agents'],
            data={
                'type': 'agent_status',
                'active_count': str(active_agents)
            }
        )
    
    def notify_deployment_complete(self, deployment_info):
        """Notification de déploiement terminé"""
        self.send_fcm_notification(
            title="🚀 Déploiement Panini - Terminé",
            body=f"Nouveau déploiement: {deployment_info.get('version', 'unknown')}",
            data={
                'type': 'deployment',
                'version': deployment_info.get('version'),
                'domains': deployment_info.get('domains', [])
            }
        )

# Configuration pour l'intégration
class NotificationConfig:
    """Guide de configuration FCM"""
    
    @staticmethod
    def print_setup_guide():
        print("""
🔧 CONFIGURATION FCM - GUIDE COMPLET
====================================

📱 1. CRÉATION PROJET FIREBASE:
   - Aller sur: https://console.firebase.google.com/
   - Créer projet "PaniniEcosystem" 
   - Ajouter app Android avec package: com.panini.ecosystem

📱 2. CONFIGURATION ANDROID STUDIO:
   - Télécharger google-services.json
   - Ajouter dans app/ de ton projet Android
   - Ajouter dans build.gradle (Module):
     implementation 'com.google.firebase:firebase-messaging:23.0.0'

🔑 3. RÉCUPÉRATION CLÉS:
   - Server Key: Firebase Console > Settings > Cloud Messaging
   - Device Token: Via code Android (voir ci-dessous)

📱 4. CODE ANDROID BASIQUE:
   
   // MainActivity.java
   FirebaseMessaging.getInstance().getToken()
       .addOnCompleteListener(new OnCompleteListener<String>() {
           @Override
           public void onComplete(@NonNull Task<String> task) {
               String token = task.getResult();
               Log.d("FCM", "Token: " + token);
               // Envoyer ce token au serveur Python
           }
       });

🎯 5. TOPICS SUBSCRIPTION:
   
   // S'abonner aux notifications domaines
   FirebaseMessaging.getInstance().subscribeToTopic("panini_domains");
   FirebaseMessaging.getInstance().subscribeToTopic("panini_agents");
   FirebaseMessaging.getInstance().subscribeToTopic("panini_critical");

📬 6. SERVICE NOTIFICATIONS:
   
   // MyFirebaseMessagingService.java
   public class MyFirebaseMessagingService extends FirebaseMessagingService {
       @Override
       public void onMessageReceived(RemoteMessage remoteMessage) {
           // Gérer les notifications reçues
           String title = remoteMessage.getNotification().getTitle();
           String body = remoteMessage.getNotification().getBody();
           
           // Créer notification locale
           showNotification(title, body);
       }
   }

🔧 7. CONFIGURATION PYTHON:
   - Modifier YOUR_FCM_SERVER_KEY dans monitor_domains.py
   - Modifier YOUR_DEVICE_TOKEN ou utiliser topics
        """)

if __name__ == "__main__":
    # Guide de configuration
    NotificationConfig.print_setup_guide()
    
    # Test du système (avec clés factices)
    notifier = PaniniNotificationSystem()
    
    # Simulation de notification de test
    print("\n🧪 TEST SIMULATION:")
    print("(Remplacer les clés pour test réel)")
    
    test_report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {'total': 5, 'online': 3, 'ssl_errors': 2, 'offline': 0}
    }
    
    print("Test notification domaines...")
    # notifier.notify_domain_status(test_report)  # Décommenter avec vraies clés
