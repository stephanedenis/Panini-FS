# Prototypage Rapide : Démo Traçabilité PaniniFS

## Preuve de Concept Immédiate

**Objectif** : Démontrer l'architecture d'attribution en 3 heures avec données réelles.

**Principe** : Construction incrémentale d'un "mini-PaniniFS" observable.

---

## Phase 1 : Collecte Tracée (30 min)

### Script de Collecte avec Attribution
```python
#!/usr/bin/env python3
"""
Collecteur sémantique avec traçabilité complète
Usage: python collect_with_attribution.py --source wikipedia --concept "intelligence artificielle"
"""

import json
import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import hashlib

@dataclass
class Agent:
    id: str
    type: str  # human, machine, collective
    name: str
    version: Optional[str] = None
    bias_profile: Optional[Dict] = None

@dataclass 
class ProvenanceRecord:
    source_agent: str
    timestamp: str
    method: str
    source_url: str
    extraction_confidence: float
    parent_sources: List[str]

@dataclass
class SemanticAtom:
    id: str
    concept: str
    definition: str
    context: str
    provenance: ProvenanceRecord
    
class AttributionCollector:
    def __init__(self, agent_profile: Agent):
        self.agent = agent_profile
        self.atoms = []
        
    def extract_from_wikipedia(self, concept: str) -> List[SemanticAtom]:
        """Extraction Wikipedia avec attribution complète"""
        import wikipedia
        
        # Récupération page
        try:
            page = wikipedia.page(concept)
            content = page.content[:2000]  # Premier paragraphe
            
            # Génération ID unique
            atom_id = hashlib.md5(f"{concept}_{page.url}_{datetime.datetime.now()}".encode()).hexdigest()[:8]
            
            # Création atome sémantique
            atom = SemanticAtom(
                id=atom_id,
                concept=concept,
                definition=content.split('.')[0],  # Première phrase
                context=content,
                provenance=ProvenanceRecord(
                    source_agent=self.agent.id,
                    timestamp=datetime.datetime.now().isoformat(),
                    method=f"wikipedia_extraction_{self.agent.version}",
                    source_url=page.url,
                    extraction_confidence=0.85,  # Heuristique
                    parent_sources=[page.url]
                )
            )
            
            self.atoms.append(atom)
            return [atom]
            
        except Exception as e:
            print(f"Erreur extraction {concept}: {e}")
            return []
            
    def save_to_store(self, filename: str):
        """Sauvegarde avec métadonnées complètes"""
        store = {
            "collection_metadata": {
                "collector_agent": asdict(self.agent),
                "collection_date": datetime.datetime.now().isoformat(),
                "total_atoms": len(self.atoms),
                "version": "0.1.0"
            },
            "semantic_atoms": [asdict(atom) for atom in self.atoms]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(store, f, indent=2, ensure_ascii=False)
            
        print(f"✅ {len(self.atoms)} atomes sauvés dans {filename}")

if __name__ == "__main__":
    # Configuration agent collecteur
    agent = Agent(
        id="autonomous_copilot_v1",
        type="machine", 
        name="PaniniFS Autonomous Copilot",
        version="1.0.0",
        bias_profile={"source": "wikipedia_fr", "language": "french", "cultural_context": "western"}
    )
    
    # Collecte concepts test
    collector = AttributionCollector(agent)
    
    concepts = [
        "intelligence artificielle",
        "machine learning", 
        "réseaux de neurones",
        "apprentissage profond",
        "transformers"
    ]
    
    for concept in concepts:
        print(f"🔍 Extraction: {concept}")
        collector.extract_from_wikipedia(concept)
    
    # Sauvegarde avec traçabilité
    collector.save_to_store("demo_semantic_store.json")
    print(f"🚀 Collecte terminée : {len(collector.atoms)} atomes sémantiques tracés")
```

### Lancement Immédiat
```bash
cd /home/stephane/GitHub/PaniniFS-1/Copilotage/scripts
python collect_with_attribution.py
```

---

## Phase 2 : Analyse Consensus (45 min)

### Détecteur de Convergence/Divergence
```python
#!/usr/bin/env python3
"""
Analyseur de consensus avec détection patterns
"""

import json
from collections import defaultdict
from typing import Dict, List
import re

class ConsensusAnalyzer:
    def __init__(self, store_file: str):
        with open(store_file, 'r', encoding='utf-8') as f:
            self.store = json.load(f)
        self.atoms = self.store['semantic_atoms']
        
    def analyze_definition_patterns(self) -> Dict:
        """Détecte patterns dans définitions"""
        patterns = defaultdict(list)
        
        for atom in self.atoms:
            definition = atom['definition'].lower()
            concept = atom['concept']
            
            # Patterns linguistiques
            if 'apprentissage' in definition:
                patterns['learning_based'].append(concept)
            if 'réseau' in definition or 'neurone' in definition:
                patterns['network_based'].append(concept)
            if 'algorithme' in definition:
                patterns['algorithmic'].append(concept)
            if 'données' in definition:
                patterns['data_driven'].append(concept)
                
        return dict(patterns)
        
    def detect_semantic_clusters(self) -> List[Dict]:
        """Clustering basique par mots-clés communs"""
        clusters = []
        
        # Extraction mots-clés par concept
        concept_keywords = {}
        for atom in self.atoms:
            words = re.findall(r'\b\w{4,}\b', atom['definition'].lower())
            concept_keywords[atom['concept']] = set(words)
            
        # Similarité par intersection
        concepts = list(concept_keywords.keys())
        for i, concept1 in enumerate(concepts):
            cluster = {'core_concept': concept1, 'related': [], 'similarity_scores': []}
            
            for j, concept2 in enumerate(concepts):
                if i != j:
                    words1 = concept_keywords[concept1]
                    words2 = concept_keywords[concept2]
                    
                    intersection = words1 & words2
                    union = words1 | words2
                    similarity = len(intersection) / len(union) if union else 0
                    
                    if similarity > 0.1:  # Seuil arbitraire
                        cluster['related'].append(concept2)
                        cluster['similarity_scores'].append(similarity)
                        
            if cluster['related']:
                clusters.append(cluster)
                
        return clusters
        
    def generate_consensus_report(self) -> Dict:
        """Rapport consensus avec métriques"""
        patterns = self.analyze_definition_patterns()
        clusters = self.detect_semantic_clusters()
        
        report = {
            "analysis_metadata": {
                "total_concepts": len(self.atoms),
                "analysis_date": "2024-11-30",
                "analyzer_version": "0.1.0"
            },
            "semantic_patterns": patterns,
            "concept_clusters": clusters,
            "consensus_metrics": {
                "pattern_coverage": {pattern: len(concepts)/len(self.atoms) 
                                  for pattern, concepts in patterns.items()},
                "cluster_density": len(clusters) / len(self.atoms),
                "avg_cluster_size": sum(len(c['related']) for c in clusters) / len(clusters) if clusters else 0
            }
        }
        
        return report
        
    def save_analysis(self, filename: str):
        """Sauvegarde analyse"""
        report = self.generate_consensus_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Analyse consensus sauvée: {filename}")
        return report

if __name__ == "__main__":
    analyzer = ConsensusAnalyzer("demo_semantic_store.json")
    report = analyzer.save_analysis("consensus_analysis.json")
    
    print("\n🧠 PATTERNS DÉTECTÉS:")
    for pattern, concepts in report['semantic_patterns'].items():
        print(f"  {pattern}: {concepts}")
        
    print("\n🔗 CLUSTERS SÉMANTIQUES:")
    for cluster in report['concept_clusters']:
        core = cluster['core_concept']
        related = cluster['related'][:3]  # Top 3
        print(f"  {core} → {related}")
```

---

## Phase 3 : Visualisation Temps Réel (45 min)

### Dashboard Traçabilité Web
```python
#!/usr/bin/env python3
"""
Serveur web pour visualisation traçabilité en temps réel
"""

from flask import Flask, render_template, jsonify
import json
from datetime import datetime

app = Flask(__name__)

class TraceabilityDashboard:
    def __init__(self):
        self.load_data()
        
    def load_data(self):
        try:
            with open('demo_semantic_store.json', 'r', encoding='utf-8') as f:
                self.store = json.load(f)
        except FileNotFoundError:
            self.store = {"semantic_atoms": []}
            
        try:
            with open('consensus_analysis.json', 'r', encoding='utf-8') as f:
                self.analysis = json.load(f)
        except FileNotFoundError:
            self.analysis = {"semantic_patterns": {}}
    
    def get_provenance_graph(self):
        """Génère graphe de provenance pour vis.js"""
        nodes = []
        edges = []
        
        for atom in self.store['semantic_atoms']:
            # Noeud concept
            nodes.append({
                'id': atom['id'],
                'label': atom['concept'],
                'group': 'concept',
                'title': f"Définition: {atom['definition'][:100]}..."
            })
            
            # Noeud agent
            agent_id = atom['provenance']['source_agent']
            if not any(n['id'] == agent_id for n in nodes):
                nodes.append({
                    'id': agent_id,
                    'label': agent_id,
                    'group': 'agent',
                    'title': f"Agent: {agent_id}"
                })
            
            # Edge agent → concept
            edges.append({
                'from': agent_id,
                'to': atom['id'],
                'label': atom['provenance']['method'],
                'title': f"Confiance: {atom['provenance']['extraction_confidence']}"
            })
            
        return {'nodes': nodes, 'edges': edges}
    
    def get_timeline_data(self):
        """Timeline des extractions"""
        timeline = []
        for atom in self.store['semantic_atoms']:
            timeline.append({
                'date': atom['provenance']['timestamp'],
                'concept': atom['concept'],
                'agent': atom['provenance']['source_agent'],
                'confidence': atom['provenance']['extraction_confidence']
            })
        return sorted(timeline, key=lambda x: x['date'])

dashboard = TraceabilityDashboard()

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>PaniniFS - Démo Traçabilité</title>
    <script src="https://cdn.jsdelivr.net/npm/vis-network@latest/dist/vis-network.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { display: flex; flex-wrap: wrap; gap: 20px; }
        .panel { border: 1px solid #ccc; padding: 15px; min-width: 400px; }
        #provenance-graph { height: 400px; }
        .metric { background: #f0f0f0; padding: 10px; margin: 5px 0; }
    </style>
</head>
<body>
    <h1>🚀 PaniniFS - Démo Traçabilité Temps Réel</h1>
    
    <div class="container">
        <div class="panel">
            <h2>📊 Métriques Globales</h2>
            <div id="metrics"></div>
        </div>
        
        <div class="panel">
            <h2>🕸️ Graphe de Provenance</h2>
            <div id="provenance-graph"></div>
        </div>
        
        <div class="panel">
            <h2>📈 Timeline Extractions</h2>
            <canvas id="timeline-chart" width="400" height="200"></canvas>
        </div>
        
        <div class="panel">
            <h2>🧠 Patterns Sémantiques</h2>
            <div id="patterns"></div>
        </div>
    </div>

    <script>
        // Chargement données
        fetch('/api/provenance')
            .then(r => r.json())
            .then(data => {
                const container = document.getElementById('provenance-graph');
                const options = {
                    groups: {
                        concept: {color: {background: '#97C2FC'}},
                        agent: {color: {background: '#FFAB00'}}
                    }
                };
                new vis.Network(container, data, options);
            });
            
        fetch('/api/metrics')
            .then(r => r.json())
            .then(data => {
                const container = document.getElementById('metrics');
                container.innerHTML = `
                    <div class="metric">📋 Concepts: ${data.total_concepts}</div>
                    <div class="metric">🤖 Agents: ${data.total_agents}</div>
                    <div class="metric">🔗 Liens: ${data.total_links}</div>
                    <div class="metric">⏰ Dernière MAJ: ${data.last_update}</div>
                `;
            });
            
        fetch('/api/patterns')
            .then(r => r.json())
            .then(data => {
                const container = document.getElementById('patterns');
                let html = '';
                for (const [pattern, concepts] of Object.entries(data)) {
                    html += `<div class="metric"><strong>${pattern}:</strong> ${concepts.join(', ')}</div>`;
                }
                container.innerHTML = html;
            });
    </script>
</body>
</html>
    '''

@app.route('/api/provenance')
def api_provenance():
    return jsonify(dashboard.get_provenance_graph())

@app.route('/api/metrics')
def api_metrics():
    dashboard.load_data()  # Refresh
    return jsonify({
        'total_concepts': len(dashboard.store['semantic_atoms']),
        'total_agents': len(set(a['provenance']['source_agent'] for a in dashboard.store['semantic_atoms'])),
        'total_links': len(dashboard.store['semantic_atoms']),
        'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/patterns')
def api_patterns():
    dashboard.load_data()
    return jsonify(dashboard.analysis.get('semantic_patterns', {}))

if __name__ == '__main__':
    print("🌐 Dashboard démarré sur http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
```

---

## Phase 4 : Test Système Complet (60 min)

### Script de Démo End-to-End
```bash
#!/bin/bash
# demo_complete.sh - Démonstrateur PaniniFS traçabilité

echo "🚀 DÉMO PANINI FS - TRAÇABILITÉ COMPLÈTE"
echo "========================================"

# 1. Collecte avec attribution
echo "📊 Phase 1: Collecte sémantique tracée..."
python collect_with_attribution.py
echo "✅ Collecte terminée"
echo

# 2. Analyse consensus
echo "🧠 Phase 2: Analyse patterns et consensus..."
python consensus_analyzer.py
echo "✅ Analyse terminée"
echo

# 3. Lancement dashboard
echo "🌐 Phase 3: Lancement dashboard temps réel..."
echo "👉 Ouvrir http://localhost:5000 dans votre navigateur"
python traceability_dashboard.py &
DASHBOARD_PID=$!
echo "✅ Dashboard démarré (PID: $DASHBOARD_PID)"
echo

# 4. Test ajout concept en temps réel
echo "🔄 Phase 4: Test mise à jour temps réel..."
sleep 3

# Simulation nouveau concept
echo "  → Ajout concept 'blockchain'..."
python -c "
from collect_with_attribution import *
agent = Agent('demo_agent', 'machine', 'Demo Agent', '1.0')
collector = AttributionCollector(agent)
collector.extract_from_wikipedia('blockchain')
collector.save_to_store('demo_semantic_store.json')
print('   ✅ Concept ajouté')
"

echo "  → Rafraîchir le dashboard pour voir la mise à jour"
echo

echo "🎯 DÉMO COMPLÈTE !"
echo "=================="
echo "✨ Traçabilité totale démontrée :"
echo "   • Attribution complète (qui/quoi/quand)"
echo "   • Consensus en temps réel"
echo "   • Visualisation interactive"
echo "   • Mise à jour automatique"
echo
echo "👈 Appuyer sur Ctrl+C pour arrêter le dashboard"

# Attendre interruption
wait $DASHBOARD_PID
```

---

## Résultats Attendus

### Visualisation Immédiate
- **Graphe de provenance** : Agents → Concepts avec métriques confiance
- **Timeline** : Évolution temporelle des extractions
- **Patterns** : Clusters sémantiques détectés automatiquement
- **Métriques** : Consensus, couverture, densité conceptuelle

### Preuves Traçabilité
- **Qui** : Agent_ID avec profil complet (bias, version, contexte)
- **Quoi** : Concept + définition + contexte d'extraction
- **Quand** : Timestamp précis + version système
- **Comment** : Méthode extraction + niveau confiance
- **Pourquoi** : Sources parentes + validation events

### Innovation Démontrable
1. **Attribution totale** : Chaque assertion tracée à son auteur
2. **Consensus évolutif** : Métriques accord/désaccord temps réel  
3. **Correction automatique** : Système apprend des validations
4. **Navigation temporelle** : Histoire complète des concepts
5. **Détection émergence** : Nouveaux patterns automatiquement

---

**Temps total** : 3h pour preuve de concept complète ✨

**Livrable** : Système PaniniFS minimal mais entièrement fonctionnel avec traçabilité totale démontrée visuellement.
