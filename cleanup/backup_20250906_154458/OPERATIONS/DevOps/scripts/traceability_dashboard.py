#!/usr/bin/env python3
"""
Serveur web pour visualisation traçabilité en temps réel
"""

from flask import Flask, render_template, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)

class TraceabilityDashboard:
    def __init__(self):
        self.load_data()
        
    def load_data(self):
        try:
            with open('demo_semantic_store.json', 'r', encoding='utf-8') as f:
                self.store = json.load(f)
                print(f"📊 Store chargé: {len(self.store.get('semantic_atoms', []))} atomes")
        except FileNotFoundError:
            print("⚠️  demo_semantic_store.json non trouvé")
            self.store = {"semantic_atoms": []}
            
        try:
            with open('consensus_analysis.json', 'r', encoding='utf-8') as f:
                self.analysis = json.load(f)
                print(f"🧠 Analyse chargée: {len(self.analysis.get('semantic_patterns', {}))} patterns")
        except FileNotFoundError:
            print("⚠️  consensus_analysis.json non trouvé")
            self.analysis = {"semantic_patterns": {}}
    
    def get_provenance_graph(self):
        """Génère graphe de provenance pour vis.js"""
        nodes = []
        edges = []
        
        atoms = self.store.get('semantic_atoms', [])
        
        for atom in atoms:
            # Noeud concept
            nodes.append({
                'id': atom['id'],
                'label': atom['concept'][:20] + "..." if len(atom['concept']) > 20 else atom['concept'],
                'group': 'concept',
                'title': f"Concept: {atom['concept']}\nDéfinition: {atom['definition'][:200]}...\nSource: {atom['provenance']['source_url']}"
            })
            
            # Noeud agent (groupé)
            agent_id = atom['provenance']['source_agent']
            if not any(n['id'] == agent_id for n in nodes):
                nodes.append({
                    'id': agent_id,
                    'label': 'Agent Copilot',
                    'group': 'agent',
                    'title': f"Agent: {agent_id}\nType: Machine\nVersion: 1.0.0"
                })
            
            # Edge agent → concept
            edges.append({
                'from': agent_id,
                'to': atom['id'],
                'label': f"{atom['provenance']['extraction_confidence']:.2f}",
                'title': f"Méthode: {atom['provenance']['method']}\nConfiance: {atom['provenance']['extraction_confidence']}\nTimestamp: {atom['provenance']['timestamp']}"
            })
            
        return {'nodes': nodes, 'edges': edges}
    
    def get_timeline_data(self):
        """Timeline des extractions"""
        timeline = []
        atoms = self.store.get('semantic_atoms', [])
        
        for atom in atoms:
            try:
                # Parsing ISO timestamp
                timestamp = atom['provenance']['timestamp']
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                
                timeline.append({
                    'date': dt.strftime('%H:%M:%S'),
                    'concept': atom['concept'],
                    'agent': atom['provenance']['source_agent'],
                    'confidence': atom['provenance']['extraction_confidence']
                })
            except Exception as e:
                print(f"Erreur parsing timestamp: {e}")
                
        return sorted(timeline, key=lambda x: x['date'])
    
    def get_pattern_stats(self):
        """Statistiques patterns pour graphiques"""
        patterns = self.analysis.get('semantic_patterns', {})
        
        # Data pour chart.js
        labels = list(patterns.keys())
        data = [len(concepts) for concepts in patterns.values()]
        
        return {
            'labels': labels,
            'datasets': [{
                'label': 'Nombre de concepts',
                'data': data,
                'backgroundColor': [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
                ][:len(labels)]
            }]
        }

dashboard = TraceabilityDashboard()

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>PaniniFS - Démo Traçabilité</title>
    <script src="https://cdn.jsdelivr.net/npm/vis-network@latest/dist/vis-network.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .header { text-align: center; margin-bottom: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; }
        .container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 1400px; margin: 0 auto; }
        .panel { background: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
        .full-width { grid-column: 1 / -1; }
        #provenance-graph { height: 400px; border: 1px solid #ddd; border-radius: 5px; }
        .metric { background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%); color: white; padding: 15px; margin: 10px 0; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }
        .metric-value { font-size: 1.5em; font-weight: bold; }
        .timeline-item { background: #e3f2fd; padding: 10px; margin: 5px 0; border-left: 4px solid #2196f3; border-radius: 4px; }
        .pattern-item { background: #f3e5f5; padding: 10px; margin: 5px 0; border-left: 4px solid #9c27b0; border-radius: 4px; }
        .refresh-btn { background: #4caf50; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 10px 0; }
        .refresh-btn:hover { background: #45a049; }
        .status-indicator { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 10px; }
        .status-active { background-color: #4caf50; }
        .status-warning { background-color: #ff9800; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 PaniniFS - Démo Traçabilité Temps Réel</h1>
        <p>Système d'attribution et consensus sémantique avec provenance complète</p>
    </div>
    
    <div class="container">
        <div class="panel">
            <h2>📊 Métriques Globales <span class="status-indicator status-active"></span></h2>
            <button class="refresh-btn" onclick="refreshData()">🔄 Actualiser</button>
            <div id="metrics"></div>
        </div>
        
        <div class="panel">
            <h2>📈 Distribution Patterns</h2>
            <canvas id="pattern-chart" width="400" height="300"></canvas>
        </div>
        
        <div class="panel full-width">
            <h2>🕸️ Graphe de Provenance - Agent → Concepts</h2>
            <div id="provenance-graph"></div>
        </div>
        
        <div class="panel">
            <h2>⏰ Timeline Extractions</h2>
            <div id="timeline"></div>
        </div>
        
        <div class="panel">
            <h2>🧠 Patterns Sémantiques Détectés</h2>
            <div id="patterns"></div>
        </div>
    </div>

    <script>
        let network = null;
        let patternChart = null;
        
        function loadProvenanceGraph() {
            fetch('/api/provenance')
                .then(r => r.json())
                .then(data => {
                    const container = document.getElementById('provenance-graph');
                    const options = {
                        groups: {
                            concept: {
                                color: {background: '#97C2FC', border: '#2B7CE9'},
                                shape: 'dot',
                                size: 20
                            },
                            agent: {
                                color: {background: '#FFAB00', border: '#FF8F00'},
                                shape: 'star',
                                size: 30
                            }
                        },
                        physics: {
                            stabilization: {iterations: 100},
                            barnesHut: {gravitationalConstant: -2000}
                        },
                        interaction: {hover: true, tooltipDelay: 200}
                    };
                    
                    if (network) network.destroy();
                    network = new vis.Network(container, data, options);
                })
                .catch(err => console.error('Erreur provenance:', err));
        }
        
        function loadMetrics() {
            fetch('/api/metrics')
                .then(r => r.json())
                .then(data => {
                    const container = document.getElementById('metrics');
                    container.innerHTML = `
                        <div class="metric">
                            <span>🎯 Concepts Tracés</span>
                            <span class="metric-value">${data.total_concepts}</span>
                        </div>
                        <div class="metric">
                            <span>🤖 Agents Actifs</span>
                            <span class="metric-value">${data.total_agents}</span>
                        </div>
                        <div class="metric">
                            <span>🔗 Liens Provenance</span>
                            <span class="metric-value">${data.total_links}</span>
                        </div>
                        <div class="metric">
                            <span>⏰ Dernière MAJ</span>
                            <span class="metric-value">${data.last_update}</span>
                        </div>
                    `;
                })
                .catch(err => console.error('Erreur métriques:', err));
        }
        
        function loadPatternChart() {
            fetch('/api/pattern-stats')
                .then(r => r.json())
                .then(data => {
                    const ctx = document.getElementById('pattern-chart').getContext('2d');
                    
                    if (patternChart) patternChart.destroy();
                    
                    patternChart = new Chart(ctx, {
                        type: 'doughnut',
                        data: data,
                        options: {
                            responsive: true,
                            plugins: {
                                legend: {
                                    position: 'bottom'
                                },
                                title: {
                                    display: true,
                                    text: 'Répartition des Patterns Sémantiques'
                                }
                            }
                        }
                    });
                })
                .catch(err => console.error('Erreur pattern chart:', err));
        }
        
        function loadTimeline() {
            fetch('/api/timeline')
                .then(r => r.json())
                .then(data => {
                    const container = document.getElementById('timeline');
                    let html = '';
                    data.forEach(item => {
                        html += `
                            <div class="timeline-item">
                                <strong>${item.date}</strong> - ${item.concept}
                                <br><small>Agent: ${item.agent} | Confiance: ${item.confidence}</small>
                            </div>
                        `;
                    });
                    container.innerHTML = html || '<p>Aucune donnée temporelle</p>';
                })
                .catch(err => console.error('Erreur timeline:', err));
        }
        
        function loadPatterns() {
            fetch('/api/patterns')
                .then(r => r.json())
                .then(data => {
                    const container = document.getElementById('patterns');
                    let html = '';
                    for (const [pattern, concepts] of Object.entries(data)) {
                        html += `
                            <div class="pattern-item">
                                <strong>${pattern.replace('_', ' ')}</strong>
                                <br><small>${concepts.join(', ')}</small>
                            </div>
                        `;
                    }
                    container.innerHTML = html || '<p>Aucun pattern détecté</p>';
                })
                .catch(err => console.error('Erreur patterns:', err));
        }
        
        function refreshData() {
            console.log('🔄 Actualisation des données...');
            loadMetrics();
            loadProvenanceGraph();
            loadPatternChart();
            loadTimeline();
            loadPatterns();
        }
        
        // Chargement initial
        document.addEventListener('DOMContentLoaded', function() {
            refreshData();
            
            // Auto-refresh toutes les 30 secondes
            setInterval(refreshData, 30000);
        });
    </script>
</body>
</html>
    '''

@app.route('/api/provenance')
def api_provenance():
    dashboard.load_data()
    return jsonify(dashboard.get_provenance_graph())

@app.route('/api/metrics')
def api_metrics():
    dashboard.load_data()
    atoms = dashboard.store.get('semantic_atoms', [])
    agents = set(a['provenance']['source_agent'] for a in atoms)
    
    return jsonify({
        'total_concepts': len(atoms),
        'total_agents': len(agents),
        'total_links': len(atoms),
        'last_update': datetime.now().strftime('%H:%M:%S')
    })

@app.route('/api/patterns')
def api_patterns():
    dashboard.load_data()
    return jsonify(dashboard.analysis.get('semantic_patterns', {}))

@app.route('/api/pattern-stats')
def api_pattern_stats():
    dashboard.load_data()
    return jsonify(dashboard.get_pattern_stats())

@app.route('/api/timeline')
def api_timeline():
    dashboard.load_data()
    return jsonify(dashboard.get_timeline_data())

def main():
    print("🌐 DASHBOARD TRAÇABILITÉ PANINI FS")
    print("==================================")
    
    # Vérification fichiers
    required_files = ['demo_semantic_store.json', 'consensus_analysis.json']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"⚠️  Fichiers manquants: {', '.join(missing_files)}")
        print("💡 Lancez d'abord:")
        if 'demo_semantic_store.json' in missing_files:
            print("   python collect_with_attribution.py")
        if 'consensus_analysis.json' in missing_files:
            print("   python consensus_analyzer.py")
        print()
    
    dashboard.load_data()
    
    print(f"🚀 Dashboard configuré:")
    print(f"   • {len(dashboard.store.get('semantic_atoms', []))} atomes sémantiques")
    print(f"   • {len(dashboard.analysis.get('semantic_patterns', {}))} patterns détectés")
    print()
    print("🌐 Serveur démarré sur: http://localhost:5000")
    print("👉 Ouvrir dans votre navigateur pour voir la visualisation")
    print("🔄 Auto-actualisation toutes les 30 secondes")
    print("📊 Graphique interactif de provenance + métriques temps réel")
    print()
    print("👈 Ctrl+C pour arrêter le serveur")
    
    app.run(debug=False, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
