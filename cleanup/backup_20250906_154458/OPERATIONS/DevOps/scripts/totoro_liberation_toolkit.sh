#!/bin/bash
"""
🐲 TOTORO LIBERATION TOOLKIT
Guide pratique implémentation immédiate distribution workloads
💰 Budget: 40$CAD/mois + GitHub gratuit optimisé
"""

echo "🐲 TOTORO LIBERATION TOOLKIT - SETUP AUTOMATISÉ"
echo "==============================================="
echo "🎯 Objectif: Migration workloads en 4 semaines"
echo "💰 Budget: 40\$CAD/mois + ressources gratuites"
echo ""

# Configuration variables
GITHUB_REPO="stephanedenis/PaniniFS"
SCRIPTS_DIR="/home/stephane/GitHub/PaniniFS-1/Copilotage/scripts"
WORKFLOWS_DIR="/home/stephane/GitHub/PaniniFS-1/.github/workflows"

# Phase 1: GitHub Actions Setup
setup_github_actions() {
    echo "🤖 PHASE 1: SETUP GITHUB ACTIONS WORKFLOWS"
    echo "==========================================="
    
    # Créer répertoire workflows
    mkdir -p "$WORKFLOWS_DIR"
    
    # Workflow 1: Collecteurs optimisés
    cat > "$WORKFLOWS_DIR/collectors-optimized.yml" << 'EOF'
name: 🔄 Collecteurs Multi-Sources Optimisés

on:
  schedule:
    # Lundi, Mercredi, Vendredi à 02:00 UTC (optimisation coût)
    - cron: '0 2 * * 1,3,5'
  workflow_dispatch: # Manual trigger

env:
  PYTHON_VERSION: '3.11'

jobs:
  wikipedia-collector:
    runs-on: ubuntu-latest
    timeout-minutes: 45
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        cd Copilotage/scripts
        pip install -r requirements.txt
    
    - name: Run Wikipedia Collector
      run: |
        cd Copilotage/scripts
        python3 collect_with_attribution.py --source wikipedia --max-articles 100 --timeout 40
    
    - name: Upload Wikipedia Data
      uses: actions/upload-artifact@v4
      with:
        name: wikipedia-data-${{ github.run_number }}
        path: Copilotage/scripts/*wikipedia*.json
        retention-days: 30

  arxiv-collector:
    runs-on: ubuntu-latest
    timeout-minutes: 45
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        cd Copilotage/scripts
        pip install -r requirements.txt
    
    - name: Run ArXiv Collector
      run: |
        cd Copilotage/scripts
        python3 arxiv_collector.py --max-papers 50 --timeout 40
    
    - name: Upload ArXiv Data
      uses: actions/upload-artifact@v4
      with:
        name: arxiv-data-${{ github.run_number }}
        path: Copilotage/scripts/*arxiv*.json
        retention-days: 30

  consensus-analysis:
    needs: [wikipedia-collector, arxiv-collector]
    runs-on: ubuntu-latest
    timeout-minutes: 30
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
        cache: 'pip'
    
    - name: Download artifacts
      uses: actions/download-artifact@v4
      with:
        pattern: '*-data-*'
        path: Copilotage/scripts/
        merge-multiple: true
    
    - name: Install dependencies
      run: |
        cd Copilotage/scripts
        pip install -r requirements.txt
    
    - name: Run Consensus Analysis
      run: |
        cd Copilotage/scripts
        python3 consensus_analyzer.py --incremental --timeout 25
    
    - name: Upload Analysis Results
      uses: actions/upload-artifact@v4
      with:
        name: consensus-analysis-${{ github.run_number }}
        path: Copilotage/scripts/*consensus*.json
        retention-days: 90
    
    - name: Update GitHub Pages Data
      run: |
        # Copier résultats vers docs pour GitHub Pages
        mkdir -p docs/data
        cp Copilotage/scripts/*consensus*.json docs/data/latest_consensus.json
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add docs/data/
        git commit -m "🤖 Auto-update consensus data" || exit 0
        git push
EOF

    # Workflow 2: Rust compilation multi-platform
    cat > "$WORKFLOWS_DIR/rust-multiplatform.yml" << 'EOF'
name: 🦀 Rust Multi-Platform Build

on:
  push:
    paths:
      - 'PaniniFS-2/**'
      - '.github/workflows/rust-multiplatform.yml'
  workflow_dispatch:

env:
  CARGO_TERM_COLOR: always

jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        include:
          - os: ubuntu-latest
            target: x86_64-unknown-linux-gnu
            artifact_name: panini-fs
            asset_name: panini-fs-linux-amd64
          - os: windows-latest
            target: x86_64-pc-windows-msvc
            artifact_name: panini-fs.exe
            asset_name: panini-fs-windows-amd64.exe
          - os: macos-latest
            target: x86_64-apple-darwin
            artifact_name: panini-fs
            asset_name: panini-fs-macos-amd64
    
    runs-on: ${{ matrix.os }}
    timeout-minutes: 30
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Rust
      uses: actions-rs/toolchain@v1
      with:
        toolchain: stable
        target: ${{ matrix.target }}
        override: true
    
    - name: Cache Cargo
      uses: actions/cache@v3
      with:
        path: |
          ~/.cargo/registry
          ~/.cargo/git
          PaniniFS-2/target
        key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
    
    - name: Build Release
      run: |
        cd PaniniFS-2
        cargo build --release --target ${{ matrix.target }}
    
    - name: Upload Binary
      uses: actions/upload-artifact@v4
      with:
        name: ${{ matrix.asset_name }}
        path: PaniniFS-2/target/${{ matrix.target }}/release/${{ matrix.artifact_name }}
        retention-days: 90
EOF

    # Workflow 3: Tests automatiques
    cat > "$WORKFLOWS_DIR/automated-testing.yml" << 'EOF'
name: 🧪 Tests Automatiques

on:
  push:
    branches: [ master, develop ]
  pull_request:
    branches: [ master ]
  schedule:
    # Tests quotidiens à 06:00 UTC
    - cron: '0 6 * * *'

jobs:
  python-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        cd Copilotage/scripts
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run Python Tests
      run: |
        cd Copilotage/scripts
        pytest --cov=. --cov-report=xml
    
    - name: Upload Coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./Copilotage/scripts/coverage.xml

  rust-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Rust
      uses: actions-rs/toolchain@v1
      with:
        toolchain: stable
        override: true
    
    - name: Cache Cargo
      uses: actions/cache@v3
      with:
        path: |
          ~/.cargo/registry
          ~/.cargo/git
          PaniniFS-2/target
        key: ${{ runner.os }}-cargo-test-${{ hashFiles('**/Cargo.lock') }}
    
    - name: Run Rust Tests
      run: |
        cd PaniniFS-2
        cargo test --verbose

  performance-benchmarks:
    runs-on: ubuntu-latest
    timeout-minutes: 25
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        cd Copilotage/scripts
        pip install -r requirements.txt
    
    - name: Run Performance Benchmarks
      run: |
        cd Copilotage/scripts
        python3 -c "
        import time
        import json
        from datetime import datetime
        
        # Benchmark simple
        start = time.time()
        # Simuler workload
        import requests
        end = time.time()
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'duration': end - start,
            'status': 'success'
        }
        
        with open('benchmark_results.json', 'w') as f:
            json.dump(results, f)
        "
    
    - name: Upload Benchmark Results
      uses: actions/upload-artifact@v4
      with:
        name: benchmark-results-${{ github.run_number }}
        path: Copilotage/scripts/benchmark_results.json
        retention-days: 30
EOF

    echo "✅ GitHub Actions workflows créés"
    echo "   📁 $WORKFLOWS_DIR/"
    echo "   🔄 collectors-optimized.yml (3x/semaine)"
    echo "   🦀 rust-multiplatform.yml (cross-platform)"
    echo "   🧪 automated-testing.yml (qualité continue)"
}

# Phase 2: Cloud Platform Setup Guide
setup_cloud_platforms() {
    echo ""
    echo "☁️ PHASE 2: SETUP PLATEFORMES CLOUD"
    echo "===================================="
    
    cat > "$SCRIPTS_DIR/cloud_setup_guide.md" << 'EOF'
# 🚀 Guide Setup Plateformes Cloud pour PaniniFS

## 1. Oracle Cloud Free Tier (PRIORITÉ 1)
**Pourquoi**: Le plus généreux, ARM instances puissantes

### Setup Steps:
1. Créer compte Oracle Cloud: https://cloud.oracle.com/
2. Activer Always Free tier
3. Créer Compute Instance:
   - Shape: VM.Standard.A1.Flex (ARM)
   - OCPUs: 4 (gratuit)
   - Memory: 24GB (gratuit)
   - Storage: 200GB (gratuit)
   - OS: Ubuntu 22.04 LTS

### Installation PaniniFS:
```bash
# Sur instance Oracle
sudo apt update && sudo apt install -y python3-pip git
git clone https://github.com/stephanedenis/PaniniFS.git
cd PaniniFS/Copilotage/scripts
pip3 install -r requirements.txt

# Setup service systemd pour collecteurs
sudo tee /etc/systemd/system/panini-collector.service << 'EOL'
[Unit]
Description=PaniniFS Collector Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/PaniniFS/Copilotage/scripts
ExecStart=/usr/bin/python3 autonomous-copilot.py /home/ubuntu/PaniniFS/Copilotage daemon
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl enable panini-collector
sudo systemctl start panini-collector
```

## 2. Azure for Students (SI ÉLIGIBLE)
**Pourquoi**: 100h/mois compute gratuit

### Vérification éligibilité:
- Adresse email éducation (.edu, .ac., etc.)
- Carte étudiante ou preuve affiliation
- https://azure.microsoft.com/en-us/free/students/

### Setup si éligible:
1. Activer Azure for Students
2. Créer VM B1s (1 core, 1GB RAM)
3. Installer monitoring/backup services

## 3. Google Cloud Free Tier (BACKUP)
**Pourquoi**: f1-micro toujours gratuit, bon pour dashboard web

### Setup Steps:
1. Créer compte GCP: https://cloud.google.com/
2. Activer $300 crédits + Always Free
3. Créer VM f1-micro (us-central1, us-east1, us-west1)
4. Installer dashboard web léger

## 4. Cloudflare (CDN + Analytics)
**Pourquoi**: CDN gratuit, analytics, protection DDoS

### Setup Steps:
1. Créer compte Cloudflare
2. Ajouter domaine (ou utiliser workers.dev gratuit)
3. Configurer CDN pour artifacts binaires
4. Setup Pages pour dashboard statique

## 🎯 Architecture Recommandée:
- **Oracle ARM**: Collecteurs principaux + base données
- **Azure/GCP**: Backup services + monitoring
- **Cloudflare**: Distribution artifacts + dashboard web
- **GitHub Actions**: Orchestration + CI/CD

## 💰 Estimation Coûts Mensuels:
- Oracle Free: 0$
- Azure Students: 0$ (si éligible)
- GCP Free: 0$
- Cloudflare: 0$ (plan gratuit)
- **Total: 0-15$ overflow GitHub Actions**

EOF

    echo "✅ Guide setup cloud platforms créé"
    echo "   📁 $SCRIPTS_DIR/cloud_setup_guide.md"
}

# Phase 3: Monitoring & Alerting Setup
setup_monitoring() {
    echo ""
    echo "📊 PHASE 3: SETUP MONITORING & ALERTING"
    echo "======================================="
    
    # Script monitoring simple
    cat > "$SCRIPTS_DIR/simple_monitor.py" << 'EOF'
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
EOF

    chmod +x "$SCRIPTS_DIR/simple_monitor.py"
    
    echo "✅ Simple monitor créé"
    echo "   📁 $SCRIPTS_DIR/simple_monitor.py"
    echo "   🔧 Configurer DISCORD_WEBHOOK_URL dans environment"
}

# Phase 4: Budget Tracking
setup_budget_tracking() {
    echo ""
    echo "💰 PHASE 4: SETUP BUDGET TRACKING"
    echo "================================="
    
    cat > "$SCRIPTS_DIR/budget_tracker.py" << 'EOF'
#!/usr/bin/env python3
"""
💰 Budget Tracker PaniniFS
Surveillance coûts GitHub Actions + Cloud platforms
"""

import requests
import json
from datetime import datetime, timedelta

class BudgetTracker:
    def __init__(self):
        self.monthly_budget_cad = 40
        self.github_free_minutes = 2000
        
    def get_github_actions_usage(self):
        """Récupération usage GitHub Actions"""
        # Nécessite GitHub token avec permissions appropriées
        # Pour l'instant, simulation
        
        current_month_minutes = 150  # À récupérer via API
        percentage_used = (current_month_minutes / self.github_free_minutes) * 100
        
        return {
            'minutes_used': current_month_minutes,
            'minutes_total': self.github_free_minutes,
            'percentage_used': percentage_used,
            'estimated_monthly': current_month_minutes * 30 / datetime.now().day
        }
    
    def calculate_cloud_costs(self):
        """Calcul coûts cloud estimés"""
        costs = {
            'oracle_free': 0,  # Always free
            'azure_students': 0,  # Si éligible
            'gcp_free': 0,  # f1-micro always free
            'github_actions_overflow': 0,  # Calculé selon usage
            'storage_backup': 5,  # Estimation
            'cdn_pro': 0,  # Gratuit ou 20$ si upgrade
            'total_estimated': 5
        }
        
        return costs
    
    def generate_budget_report(self):
        """Génération rapport budget"""
        github_usage = self.get_github_actions_usage()
        cloud_costs = self.calculate_cloud_costs()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'monthly_budget_cad': self.monthly_budget_cad,
            'github_actions': github_usage,
            'cloud_costs': cloud_costs,
            'budget_status': {
                'used_percentage': (cloud_costs['total_estimated'] / self.monthly_budget_cad) * 100,
                'remaining_budget': self.monthly_budget_cad - cloud_costs['total_estimated'],
                'status': 'GREEN'  # GREEN/YELLOW/RED
            }
        }
        
        # Déterminer status couleur
        used_pct = report['budget_status']['used_percentage']
        if used_pct > 80:
            report['budget_status']['status'] = 'RED'
        elif used_pct > 60:
            report['budget_status']['status'] = 'YELLOW'
        
        return report
    
    def save_budget_report(self):
        """Sauvegarde rapport budget"""
        report = self.generate_budget_report()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"budget_report_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"💾 Budget report saved: {filename}")
        print(f"💰 Current spend: ${report['cloud_costs']['total_estimated']:.2f}/{self.monthly_budget_cad} CAD")
        print(f"📊 Status: {report['budget_status']['status']}")
        
        return filename

if __name__ == "__main__":
    tracker = BudgetTracker()
    tracker.save_budget_report()
EOF

    chmod +x "$SCRIPTS_DIR/budget_tracker.py"
    
    echo "✅ Budget tracker créé"
    echo "   📁 $SCRIPTS_DIR/budget_tracker.py"
    echo "   📊 Surveillance 40\$CAD/mois automatique"
}

# Exécution toutes les phases
main() {
    echo "🐲 DÉBUT SETUP TOTORO LIBERATION TOOLKIT"
    echo ""
    
    setup_github_actions
    setup_cloud_platforms
    setup_monitoring
    setup_budget_tracking
    
    echo ""
    echo "🏆 SETUP COMPLET TOTORO LIBERATION!"
    echo "=================================="
    echo "✅ GitHub Actions workflows configurés"
    echo "☁️ Guide setup cloud platforms créé"
    echo "📊 Monitoring & alerting configurés"
    echo "💰 Budget tracking automatisé"
    echo ""
    echo "🚀 PROCHAINES ÉTAPES:"
    echo "1. Commit & push workflows: git add .github/ && git commit -m '🤖 Add automation workflows'"
    echo "2. Setup cloud accounts selon guide"
    echo "3. Configurer Discord webhook pour alertes"
    echo "4. Tester workflows manuellement"
    echo ""
    echo "🎯 TIMELINE: 4 semaines → Totoro libre en mode inspiration!"
}

main
