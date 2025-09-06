/**
 * 📱 PANINI ECOSYSTEM - SERVICE FCM KOTLIN
 * Service Firebase Cloud Messaging pour notifications monitoring
 */

package com.panini.monitoring

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import org.json.JSONObject

class PaniniFirebaseMessagingService : FirebaseMessagingService() {

    companion object {
        private const val CHANNEL_ID = "panini_monitoring_channel"
        private const val NOTIFICATION_ID = 1001
    }

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
    }

    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        super.onMessageReceived(remoteMessage)
        
        // Log pour debug
        android.util.Log.d("PaniniFirebase", "Message reçu de: ${remoteMessage.from}")
        
        // Traite les notifications selon le type
        remoteMessage.data.isNotEmpty().let {
            val dataType = remoteMessage.data["type"]
            
            when (dataType) {
                "domain_status" -> handleDomainStatusNotification(remoteMessage)
                "agent_activity" -> handleAgentActivityNotification(remoteMessage)
                "deployment_complete" -> handleDeploymentNotification(remoteMessage)
                else -> handleGenericNotification(remoteMessage)
            }
        }
        
        // Notification standard si présente
        remoteMessage.notification?.let {
            showNotification(
                title = it.title ?: "PaniniFS",
                body = it.body ?: "Nouvelle notification",
                data = remoteMessage.data
            )
        }
    }

    override fun onNewToken(token: String) {
        super.onNewToken(token)
        android.util.Log.d("PaniniFirebase", "Token FCM: $token")
        
        // Envoie le token au serveur pour enregistrement
        sendTokenToServer(token)
        
        // S'abonne aux topics de monitoring
        subscribeToTopics(token)
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "Monitoring PaniniFS",
                NotificationManager.IMPORTANCE_DEFAULT
            ).apply {
                description = "Notifications de monitoring de l'écosystème PaniniFS"
                enableLights(true)
                lightColor = android.graphics.Color.parseColor("#3498db")
                enableVibration(true)
                vibrationPattern = longArrayOf(100, 200, 100, 200)
            }
            
            val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }

    private fun handleDomainStatusNotification(message: RemoteMessage) {
        val domain = message.data["domain"] ?: "Domaine inconnu"
        val status = message.data["status"] ?: "unknown"
        val details = message.data["details"]?.let { JSONObject(it) }
        
        val emoji = when (status) {
            "online" -> "✅"
            "ssl_error" -> "⚠️"
            "offline" -> "❌"
            "deploying" -> "🚀"
            else -> "📊"
        }
        
        val title = "$emoji $domain"
        val body = when (status) {
            "online" -> {
                val responseTime = details?.optString("response_time", "N/A")
                "Opérationnel - ${responseTime}ms"
            }
            "ssl_error" -> "Certificat SSL en attente"
            "offline" -> "Inaccessible - Vérification requise"
            "deploying" -> "Déploiement en cours..."
            else -> "Statut: $status"
        }
        
        showNotification(title, body, message.data, createDomainIntent(domain))
    }

    // ... (Autres méthodes de gestion des notifications)
}

// ========================================
// 1. build.gradle (Module: app)
// ========================================

android {
    compileSdk 34
    
    defaultConfig {
        applicationId "com.panini.ecosystem"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.9.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    
    // Firebase
    implementation platform('com.google.firebase:firebase-bom:32.2.3')
    implementation 'com.google.firebase:firebase-messaging'
    implementation 'com.google.firebase:firebase-analytics'
    
    // Notifications
    implementation 'androidx.work:work-runtime:2.8.1'
}

// ========================================
// 2. MainActivity.java
// ========================================

package com.panini.ecosystem;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import com.google.firebase.messaging.FirebaseMessaging;
import android.Manifest;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "PaniniEcosystem";
    private static final String CHANNEL_ID = "panini_notifications";
    private static final int PERMISSION_REQUEST_CODE = 1001;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        // Demander permissions notifications (Android 13+)
        requestNotificationPermission();
        
        // Créer canal de notification
        createNotificationChannel();
        
        // Configuration FCM
        setupFirebaseMessaging();
    }
    
    private void requestNotificationPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) 
                != PackageManager.PERMISSION_GRANTED) {
                
                ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.POST_NOTIFICATIONS},
                    PERMISSION_REQUEST_CODE);
            }
        }
    }
    
    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            CharSequence name = "Panini Ecosystem";
            String description = "Notifications de l'écosystème Panini";
            int importance = NotificationManager.IMPORTANCE_HIGH;
            
            NotificationChannel channel = new NotificationChannel(CHANNEL_ID, name, importance);
            channel.setDescription(description);
            channel.enableVibration(true);
            channel.enableLights(true);
            
            NotificationManager notificationManager = getSystemService(NotificationManager.class);
            notificationManager.createNotificationChannel(channel);
        }
    }
    
    private void setupFirebaseMessaging() {
        // Récupérer le token FCM
        FirebaseMessaging.getInstance().getToken()
            .addOnCompleteListener(task -> {
                if (!task.isSuccessful()) {
                    Log.w(TAG, "Echec récupération token FCM", task.getException());
                    return;
                }
                
                String token = task.getResult();
                Log.d(TAG, "Token FCM: " + token);
                
                // TODO: Envoyer le token au serveur Python
                // sendTokenToServer(token);
            });
            
        // S'abonner aux topics
        FirebaseMessaging.getInstance().subscribeToTopic("panini_domains")
            .addOnCompleteListener(task -> {
                String msg = "Abonnement domaines: " + (task.isSuccessful() ? "OK" : "Echec");
                Log.d(TAG, msg);
            });
            
        FirebaseMessaging.getInstance().subscribeToTopic("panini_agents")
            .addOnCompleteListener(task -> {
                String msg = "Abonnement agents: " + (task.isSuccessful() ? "OK" : "Echec");
                Log.d(TAG, msg);
            });
            
        FirebaseMessaging.getInstance().subscribeToTopic("panini_critical")
            .addOnCompleteListener(task -> {
                String msg = "Abonnement critique: " + (task.isSuccessful() ? "OK" : "Echec");
                Log.d(TAG, msg);
            });
    }
}

// ========================================
// 3. PaniniFirebaseMessagingService.java
// ========================================

package com.panini.ecosystem;

import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.util.Log;
import androidx.core.app.NotificationCompat;
import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;

public class PaniniFirebaseMessagingService extends FirebaseMessagingService {
    private static final String TAG = "PaniniFirebase";
    private static final String CHANNEL_ID = "panini_notifications";
    
    @Override
    public void onMessageReceived(RemoteMessage remoteMessage) {
        Log.d(TAG, "Message reçu de: " + remoteMessage.getFrom());
        
        // Vérifier si le message contient une notification
        if (remoteMessage.getNotification() != null) {
            String title = remoteMessage.getNotification().getTitle();
            String body = remoteMessage.getNotification().getBody();
            
            Log.d(TAG, "Titre: " + title);
            Log.d(TAG, "Corps: " + body);
            
            // Données personnalisées
            String notificationType = remoteMessage.getData().get("type");
            
            // Créer notification locale
            showNotification(title, body, notificationType);
        }
    }
    
    @Override
    public void onNewToken(String token) {
        Log.d(TAG, "Nouveau token FCM: " + token);
        
        // TODO: Envoyer le nouveau token au serveur
        // sendTokenToServer(token);
    }
    
    private void showNotification(String title, String body, String type) {
        Intent intent = new Intent(this, MainActivity.class);
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        
        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0, intent,
            PendingIntent.FLAG_ONE_SHOT | PendingIntent.FLAG_IMMUTABLE);
        
        // Icône selon le type
        int iconRes = R.drawable.ic_panini;
        if ("domain_critical".equals(type)) {
            iconRes = R.drawable.ic_error;
        } else if ("domain_success".equals(type)) {
            iconRes = R.drawable.ic_success;
        }
        
        NotificationCompat.Builder notificationBuilder =
            new NotificationCompat.Builder(this, CHANNEL_ID)
                .setSmallIcon(iconRes)
                .setContentTitle(title)
                .setContentText(body)
                .setAutoCancel(true)
                .setPriority(NotificationCompat.PRIORITY_HIGH)
                .setDefaults(NotificationCompat.DEFAULT_ALL)
                .setContentIntent(pendingIntent);
        
        NotificationManager notificationManager =
            (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
            
        notificationManager.notify(0, notificationBuilder.build());
    }
}

// ========================================
// 4. AndroidManifest.xml (ajouts)
// ========================================

<application>
    <!-- Service FCM -->
    <service
        android:name=".PaniniFirebaseMessagingService"
        android:exported="false">
        <intent-filter>
            <action android:name="com.google.firebase.MESSAGING_EVENT" />
        </intent-filter>
    </service>
    
    <!-- Permissions -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.WAKE_LOCK" />
    <uses-permission android:name="android.permission.VIBRATE" />
    
    <!-- Android 13+ -->
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
</application>

// ========================================
// 5. Ressources à ajouter
// ========================================

// res/drawable/ic_panini.xml
// res/drawable/ic_success.xml  
// res/drawable/ic_error.xml

// res/layout/activity_main.xml
// Interface simple avec statut de connexion

// ========================================
// 6. Configuration gradle projet
// ========================================

// build.gradle (Project)
classpath 'com.google.gms:google-services:4.3.15'

// build.gradle (Module)
apply plugin: 'com.google.gms.google-services'

/*
🎯 DÉPLOIEMENT RAPIDE:

1. Créer projet dans Android Studio
2. Copier ce code dans les fichiers appropriés  
3. Ajouter google-services.json dans app/
4. Compiler et installer sur ton Android
5. Récupérer le token FCM dans les logs
6. Modifier notification_system.py avec tes clés
7. Lancer monitoring avec notifications !

📱 Une fois déployé, tu recevras des notifications pour:
   ✅ Domaines qui deviennent opérationnels
   ⚠️ Changements de statut  
   🚨 Problèmes critiques
   🤖 Activité des agents

🔄 Monitoring automatique toutes les 15 minutes !
*/
