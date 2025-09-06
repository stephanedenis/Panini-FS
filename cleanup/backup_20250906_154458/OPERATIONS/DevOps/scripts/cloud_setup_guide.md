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

