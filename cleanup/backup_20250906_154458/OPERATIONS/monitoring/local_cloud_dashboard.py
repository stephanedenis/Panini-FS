#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 DASHBOARD LOCAL HYBRIDE PANINIFS
Dashboard local avec intégration cloud via iframes et données temps réel
Surveille l'activité autonome locale + cloud
"""

import os
import json
import psutil
import subprocess
import time
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import urllib.parse
import socketserver

class LocalCloudDashboard:
    def __init__(self):
        self.local_port = 8080
        self.data_file = "/tmp/paninifs_local_dashboard.json"
        self.log_file = "/tmp/paninifs_dashboard.log"
        
    def collect_local_metrics(self):
        """Collecte métriques système local"""
        try:
            # Système
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Processus Python actifs
            python_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_percent']):
                try:
                    if proc.info['name'] and 'python' in proc.info['name'].lower():
                        python_processes.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'cmdline': ' '.join(proc.info['cmdline'][:3]) if proc.info['cmdline'] else '',
                            'cpu': round(proc.info['cpu_percent'] or 0, 1),
                            'memory': round(proc.info['memory_percent'] or 0, 1)
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Terminaux actifs
            terminals_count = len([p for p in psutil.process_iter(['name']) if 'bash' in p.info['name']])
            
            # GitHub CLI status
            gh_status = "Unknown"
            try:
                result = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True, timeout=5)
                gh_status = "Connected" if result.returncode == 0 else "Disconnected"
            except:
                gh_status = "Not Available"
            
            # Dernière activité Git
            git_activity = "Unknown"
            try:
                result = subprocess.run(['git', 'log', '--oneline', '-1'], 
                                      capture_output=True, text=True, cwd='/home/stephane/GitHub/PaniniFS-1', timeout=5)
                git_activity = result.stdout.strip()[:50] if result.stdout else "No commits"
            except:
                git_activity = "Error reading git"
            
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'system': {
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'memory_used_gb': round(memory.used / (1024**3), 1),
                    'memory_total_gb': round(memory.total / (1024**3), 1),
                    'disk_percent': disk.percent,
                    'disk_used_gb': round(disk.used / (1024**3), 1),
                    'disk_total_gb': round(disk.total / (1024**3), 1)
                },
                'processes': {
                    'python_count': len(python_processes),
                    'terminals_count': terminals_count,
                    'python_processes': python_processes[:10]  # Top 10
                },
                'git': {
                    'gh_status': gh_status,
                    'last_activity': git_activity
                }
            }
            
            return metrics
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def save_metrics(self, metrics):
        """Sauvegarde métriques en JSON"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(metrics, f, indent=2)
        except Exception as e:
            self.log(f"Error saving metrics: {e}")
    
    def log(self, message):
        """Log avec timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        try:
            with open(self.log_file, 'a') as f:
                f.write(log_entry)
        except:
            pass
        print(log_entry.strip())
    
    def generate_dashboard_html(self):
        """Génère HTML dashboard hybride"""
        html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 PaniniFS - Dashboard Local Hybride</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            transition: transform 0.2s;
        }}
        .metric-card:hover {{
            transform: translateY(-5px);
        }}
        .iframe-container {{
            border: 2px solid #dee2e6;
            border-radius: 8px;
            overflow: hidden;
            height: 400px;
        }}
        .status-online {{ color: #28a745; }}
        .status-offline {{ color: #dc3545; }}
        .process-row {{ font-size: 0.8em; }}
        .refresh-indicator {{
            animation: spin 1s linear infinite;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body class="bg-light">
    <div class="container-fluid py-3">
        <!-- Header -->
        <div class="row mb-3">
            <div class="col">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h2><i class="fas fa-tachometer-alt me-2"></i>Dashboard Local Hybride</h2>
                        <small class="text-muted">Surveillance autonome locale + cloud</small>
                    </div>
                    <div>
                        <button class="btn btn-primary btn-sm" onclick="refreshData()">
                            <i class="fas fa-sync-alt" id="refreshIcon"></i> Actualiser
                        </button>
                        <span class="badge bg-success ms-2" id="lastUpdate">Chargement...</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Métriques Système -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card metric-card text-center p-3">
                    <h6><i class="fas fa-microchip"></i> CPU</h6>
                    <h3 id="cpuUsage">--</h3>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card text-center p-3">
                    <h6><i class="fas fa-memory"></i> RAM</h6>
                    <h3 id="memoryUsage">--</h3>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card text-center p-3">
                    <h6><i class="fas fa-hdd"></i> Disque</h6>
                    <h3 id="diskUsage">--</h3>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card text-center p-3">
                    <h6><i class="fab fa-python"></i> Processus</h6>
                    <h3 id="pythonCount">--</h3>
                </div>
            </div>
        </div>

        <div class="row">
            <!-- Activité Locale -->
            <div class="col-lg-6">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-desktop me-2"></i>Activité Locale</h5>
                    </div>
                    <div class="card-body">
                        <!-- GitHub CLI Status -->
                        <div class="mb-3">
                            <strong>GitHub CLI:</strong> 
                            <span id="ghStatus" class="badge">--</span>
                        </div>
                        
                        <!-- Dernière activité Git -->
                        <div class="mb-3">
                            <strong>Dernier commit:</strong><br>
                            <small id="gitActivity" class="text-muted">--</small>
                        </div>
                        
                        <!-- Processus Python actifs -->
                        <h6>Processus Python Top 5:</h6>
                        <div class="table-responsive">
                            <table class="table table-sm">
                                <thead>
                                    <tr>
                                        <th>PID</th>
                                        <th>Commande</th>
                                        <th>CPU%</th>
                                        <th>RAM%</th>
                                    </tr>
                                </thead>
                                <tbody id="processTable">
                                    <tr><td colspan="4" class="text-center">Chargement...</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Dashboard Cloud Intégré -->
            <div class="col-lg-6">
                <div class="card">
                    <div class="card-header d-flex justify-content-between">
                        <h5><i class="fas fa-cloud me-2"></i>Dashboard Cloud</h5>
                        <a href="/home/stephane/GitHub/PaniniFS-1/DOCUMENTATION/public-site/docs/dashboard.html" 
                           target="_blank" class="btn btn-outline-primary btn-sm">
                            <i class="fas fa-external-link-alt"></i> Plein écran
                        </a>
                    </div>
                    <div class="card-body p-0">
                        <div class="iframe-container">
                            <iframe src="/home/stephane/GitHub/PaniniFS-1/DOCUMENTATION/public-site/docs/dashboard.html" 
                                    width="100%" height="100%" frameborder="0"
                                    title="Dashboard Cloud PaniniFS">
                            </iframe>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Monitoring Intégré -->
        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header d-flex justify-content-between">
                        <h5><i class="fas fa-chart-line me-2"></i>Monitoring Temps Réel</h5>
                        <div>
                            <a href="file:///home/stephane/GitHub/PaniniFS-1/DOCUMENTATION/public-site/_site/monitoring/index.html" 
                               target="_blank" class="btn btn-outline-success btn-sm me-2">
                                <i class="fas fa-chart-bar"></i> Monitoring Détaillé
                            </a>
                            <button class="btn btn-outline-warning btn-sm" onclick="openTerminal()">
                                <i class="fas fa-terminal"></i> Terminal
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-lg-8">
                                <div class="iframe-container" style="height: 300px;">
                                    <iframe src="file:///home/stephane/GitHub/PaniniFS-1/DOCUMENTATION/public-site/_site/monitoring/index.html"
                                            width="100%" height="100%" frameborder="0"
                                            title="Monitoring PaniniFS">
                                    </iframe>
                                </div>
                            </div>
                            <div class="col-lg-4">
                                <h6>Actions Rapides</h6>
                                <div class="d-grid gap-2">
                                    <button class="btn btn-outline-primary btn-sm" onclick="runMonitoring()">
                                        <i class="fas fa-play"></i> Lancer Monitoring
                                    </button>
                                    <button class="btn btn-outline-success btn-sm" onclick="checkCloudStatus()">
                                        <i class="fas fa-cloud-upload-alt"></i> Status Cloud
                                    </button>
                                    <button class="btn btn-outline-info btn-sm" onclick="viewLogs()">
                                        <i class="fas fa-file-alt"></i> Voir Logs
                                    </button>
                                    <button class="btn btn-outline-warning btn-sm" onclick="emergencyStop()">
                                        <i class="fas fa-stop"></i> Arrêt d'Urgence
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let refreshInterval;
        
        function refreshData() {{
            const icon = document.getElementById('refreshIcon');
            icon.classList.add('refresh-indicator');
            
            fetch('/metrics')
                .then(response => response.json())
                .then(data => {{
                    updateDashboard(data);
                    icon.classList.remove('refresh-indicator');
                }})
                .catch(error => {{
                    console.error('Error:', error);
                    icon.classList.remove('refresh-indicator');
                }});
        }}
        
        function updateDashboard(data) {{
            if (data.error) {{
                console.error('Data error:', data.error);
                return;
            }}
            
            // Mise à jour timestamp
            const updateTime = new Date(data.timestamp).toLocaleTimeString('fr-FR');
            document.getElementById('lastUpdate').textContent = updateTime;
            
            // Métriques système
            document.getElementById('cpuUsage').textContent = data.system.cpu_percent + '%';
            document.getElementById('memoryUsage').textContent = data.system.memory_percent + '%';
            document.getElementById('diskUsage').textContent = data.system.disk_percent + '%';
            document.getElementById('pythonCount').textContent = data.processes.python_count;
            
            // GitHub status
            const ghStatusElement = document.getElementById('ghStatus');
            ghStatusElement.textContent = data.git.gh_status;
            ghStatusElement.className = 'badge ' + (data.git.gh_status === 'Connected' ? 'bg-success' : 'bg-danger');
            
            // Git activity
            document.getElementById('gitActivity').textContent = data.git.last_activity;
            
            // Processus table
            const processTable = document.getElementById('processTable');
            if (data.processes.python_processes && data.processes.python_processes.length > 0) {{
                processTable.innerHTML = '';
                data.processes.python_processes.slice(0, 5).forEach(proc => {{
                    const row = `
                        <tr class="process-row">
                            <td>${{proc.pid}}</td>
                            <td><small>${{proc.cmdline}}</small></td>
                            <td>${{proc.cpu}}%</td>
                            <td>${{proc.memory}}%</td>
                        </tr>
                    `;
                    processTable.innerHTML += row;
                }});
            }} else {{
                processTable.innerHTML = '<tr><td colspan="4" class="text-center">Aucun processus Python actif</td></tr>';
            }}
        }}
        
        function openTerminal() {{
            // Essaye d'ouvrir terminal via VS Code
            if (window.vscode) {{
                window.vscode.postMessage({{command: 'terminal.open'}});
            }} else {{
                alert('Terminal disponible dans VS Code uniquement');
            }}
        }}
        
        function runMonitoring() {{
            fetch('/action/monitoring')
                .then(response => response.text())
                .then(result => alert('Monitoring lancé: ' + result))
                .catch(error => alert('Erreur: ' + error));
        }}
        
        function checkCloudStatus() {{
            fetch('/action/cloud-status')
                .then(response => response.text())
                .then(result => alert('Status Cloud: ' + result))
                .catch(error => alert('Erreur: ' + error));
        }}
        
        function viewLogs() {{
            window.open('/logs', '_blank');
        }}
        
        function emergencyStop() {{
            if (confirm('Êtes-vous sûr de vouloir arrêter tous les processus autonomes ?')) {{
                fetch('/action/emergency-stop')
                    .then(response => response.text())
                    .then(result => alert('Arrêt d\\'urgence: ' + result))
                    .catch(error => alert('Erreur: ' + error));
            }}
        }}
        
        // Auto-refresh toutes les 5 secondes
        refreshInterval = setInterval(refreshData, 5000);
        
        // Premier chargement
        refreshData();
    </script>
</body>
</html>"""
        return html_content
    
    def start_server(self):
        """Démarre serveur HTTP local"""
        class DashboardHandler(SimpleHTTPRequestHandler):
            def __init__(self, dashboard_instance, *args, **kwargs):
                self.dashboard = dashboard_instance
                super().__init__(*args, **kwargs)
            
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    html = self.dashboard.generate_dashboard_html()
                    self.wfile.write(html.encode())
                elif self.path == '/metrics':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    metrics = self.dashboard.collect_local_metrics()
                    self.wfile.write(json.dumps(metrics).encode())
                elif self.path == '/logs':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    try:
                        with open(self.dashboard.log_file, 'r') as f:
                            logs = f.read()
                        self.wfile.write(logs.encode())
                    except:
                        self.wfile.write(b"No logs available")
                elif self.path.startswith('/action/'):
                    action = self.path.split('/')[-1]
                    result = self.dashboard.handle_action(action)
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(result.encode())
                else:
                    super().do_GET()
        
        # Handler avec référence au dashboard
        handler = lambda *args, **kwargs: DashboardHandler(self, *args, **kwargs)
        
        with socketserver.TCPServer(("", self.local_port), handler) as httpd:
            self.log(f"Dashboard Local démarré sur http://localhost:{self.local_port}")
            print(f"\n🎯 Dashboard Local Hybride disponible sur:")
            print(f"   http://localhost:{self.local_port}")
            print(f"\n🔄 Actualisation automatique toutes les 5 secondes")
            print(f"📊 Données sauvées dans: {self.data_file}")
            print(f"📝 Logs disponibles: {self.log_file}")
            print(f"\n📱 Appuyez sur Ctrl+C pour arrêter")
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                self.log("Dashboard arrêté par l'utilisateur")
                print("\n👋 Dashboard arrêté")
    
    def handle_action(self, action):
        """Gère les actions dashboard"""
        try:
            if action == 'monitoring':
                subprocess.Popen(['python3', '/home/stephane/GitHub/PaniniFS-1/monitor_domains.py'], 
                               cwd='/home/stephane/GitHub/PaniniFS-1')
                return "Monitoring lancé"
            elif action == 'cloud-status':
                result = subprocess.run(['python3', '/home/stephane/GitHub/PaniniFS-1/OPERATIONS/monitoring/ultra_reliable_cloud_test.py'], 
                                      capture_output=True, text=True, timeout=30)
                return f"Cloud Status: {result.returncode == 0}"
            elif action == 'emergency-stop':
                # Arrête processus Python PaniniFS
                stopped = 0
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        if (proc.info['name'] and 'python' in proc.info['name'].lower() and
                            proc.info['cmdline'] and any('paninifs' in cmd.lower() for cmd in proc.info['cmdline'])):
                            proc.terminate()
                            stopped += 1
                    except:
                        continue
                return f"Arrêté {stopped} processus PaniniFS"
            else:
                return f"Action inconnue: {action}"
        except Exception as e:
            return f"Erreur: {str(e)}"
    
    def run_background_collector(self):
        """Collecte métriques en arrière-plan"""
        while True:
            try:
                metrics = self.collect_local_metrics()
                self.save_metrics(metrics)
                time.sleep(5)  # Toutes les 5 secondes
            except Exception as e:
                self.log(f"Erreur collecte: {e}")
                time.sleep(10)

if __name__ == "__main__":
    dashboard = LocalCloudDashboard()
    
    # Démarre collecteur en arrière-plan
    collector_thread = threading.Thread(target=dashboard.run_background_collector, daemon=True)
    collector_thread.start()
    
    # Démarre serveur principal
    dashboard.start_server()
