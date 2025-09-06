---
layout: default
title: "Gestion Domaines"
---

# 🌐 Gestion Domaines Écosystème PaniniFS

<div class="domains-overview">
    <h2>📋 État des Domaines</h2>
    
    <div class="domain-grid">
        <div class="domain-card primary">
            <h3>🎯 paninifs.com</h3>
            <div class="status-badge active">✅ ACTIF</div>
            <p><strong>Principal</strong> - Dashboard & Documentation</p>
            <div class="domain-stats">
                <span>🔗 GitHub Pages</span>
                <span>📊 Dashboard temps réel</span>
            </div>
            <a href="https://paninifs.com" class="domain-link">Visiter →</a>
        </div>

        <div class="domain-card community">
            <h3>🌍 paninifs.org</h3>
            <div class="status-badge planned">🚧 PLANIFIÉ</div>
            <p><strong>Communauté</strong> - Open Source & Contribution</p>
            <div class="domain-stats">
                <span>👥 Forum communauté</span>
                <span>📝 Guide contribution</span>
            </div>
            <a href="#" class="domain-link disabled">En construction</a>
        </div>

        <div class="domain-card publications">
            <h3>📚 stephanedenis.cc</h3>
            <div class="status-badge planned">🚧 PLANIFIÉ</div>
            <p><strong>Publications</strong> - Articles & Recherches</p>
            <div class="domain-stats">
                <span>📄 Papers scientifiques</span>
                <span>📖 Livres Leanpub</span>
            </div>
            <a href="#" class="domain-link disabled">En construction</a>
        </div>

        <div class="domain-card agents">
            <h3>🤖 o-tomate.com</h3>
            <div class="status-badge planned">🚧 PLANIFIÉ</div>
            <p><strong>Agents</strong> - Hub Autonome</p>
            <div class="domain-stats">
                <span>⚡ Status temps réel</span>
                <span>📊 Logs d'activité</span>
            </div>
            <a href="#" class="domain-link disabled">En construction</a>
        </div>

        <div class="domain-card lab">
            <h3>🔬 sdenis.net</h3>
            <div class="status-badge planned">🚧 PLANIFIÉ</div>
            <p><strong>Laboratoire</strong> - Expérimentations</p>
            <div class="domain-stats">
                <span>🧪 Prototypes</span>
                <span>🎮 Démonstrations</span>
            </div>
            <a href="#" class="domain-link disabled">En construction</a>
        </div>

        <div class="domain-card personal">
            <h3>👤 sdenis.com</h3>
            <div class="status-badge active">✅ UTILISÉ</div>
            <p><strong>Personnel</strong> - Profil LinkedIn</p>
            <div class="domain-stats">
                <span>💼 Profil professionnel</span>
                <span>🔗 Redirection LinkedIn</span>
            </div>
            <a href="https://sdenis.com" class="domain-link">Visiter →</a>
        </div>
    </div>
</div>

<div class="domains-roadmap">
    <h2>🗺️ Feuille de Route Domaines</h2>
    
    <div class="roadmap-timeline">
        <div class="roadmap-phase completed">
            <h3>Phase 1 - Fondations ✅</h3>
            <ul>
                <li>✅ Configuration paninifs.com</li>
                <li>✅ CNAME GitHub Pages</li>
                <li>✅ Dashboard opérationnel</li>
            </ul>
        </div>

        <div class="roadmap-phase current">
            <h3>Phase 2 - Expansion 🚧</h3>
            <ul>
                <li>🔄 Setup o-tomate.com (agents)</li>
                <li>⏳ Configuration stephanedenis.cc</li>
                <li>⏳ Déploiement automatisé</li>
            </ul>
        </div>

        <div class="roadmap-phase planned">
            <h3>Phase 3 - Écosystème 📋</h3>
            <ul>
                <li>📅 Site communauté paninifs.org</li>
                <li>📅 Laboratoire sdenis.net</li>
                <li>📅 API unifiée inter-domaines</li>
            </ul>
        </div>
    </div>
</div>

<div class="domains-actions">
    <h2>🚀 Actions Disponibles</h2>
    
    <div class="action-buttons">
        <button class="btn primary" onclick="deployDomain('o-tomate.com')">
            🤖 Déployer Hub Agents
        </button>
        <button class="btn secondary" onclick="deployDomain('stephanedenis.cc')">
            📚 Activer Publications
        </button>
        <button class="btn info" onclick="showDNSConfig()">
            🔧 Configuration DNS
        </button>
        <button class="btn success" onclick="updateDomains()">
            🔄 Synchroniser Tous
        </button>
    </div>
</div>

<style>
.domains-overview {
    margin: 20px 0;
}

.domain-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

.domain-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    background: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.domain-card.primary { border-left: 4px solid #3498db; }
.domain-card.community { border-left: 4px solid #2ecc71; }
.domain-card.publications { border-left: 4px solid #9b59b6; }
.domain-card.agents { border-left: 4px solid #e74c3c; }
.domain-card.lab { border-left: 4px solid #f39c12; }
.domain-card.personal { border-left: 4px solid #34495e; }

.status-badge {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
    margin: 5px 0;
}

.status-badge.active {
    background: #d5f4e6;
    color: #27ae60;
}

.status-badge.planned {
    background: #fef9e7;
    color: #f39c12;
}

.domain-stats {
    margin: 10px 0;
}

.domain-stats span {
    display: block;
    font-size: 14px;
    color: #666;
    margin: 2px 0;
}

.domain-link {
    display: inline-block;
    margin-top: 10px;
    padding: 8px 16px;
    background: #3498db;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-size: 14px;
}

.domain-link.disabled {
    background: #bdc3c7;
    cursor: not-allowed;
}

.roadmap-timeline {
    margin: 20px 0;
}

.roadmap-phase {
    margin: 20px 0;
    padding: 15px;
    border-radius: 8px;
}

.roadmap-phase.completed {
    background: #d5f4e6;
    border-left: 4px solid #27ae60;
}

.roadmap-phase.current {
    background: #fef9e7;
    border-left: 4px solid #f39c12;
}

.roadmap-phase.planned {
    background: #ebf3fd;
    border-left: 4px solid #3498db;
}

.action-buttons {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin: 20px 0;
}

.btn {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    text-decoration: none;
    display: inline-block;
}

.btn.primary { background: #3498db; color: white; }
.btn.secondary { background: #95a5a6; color: white; }
.btn.info { background: #17a2b8; color: white; }
.btn.success { background: #28a745; color: white; }

.btn:hover {
    opacity: 0.8;
}
</style>

<script>
function deployDomain(domain) {
    alert(`🚀 Déploiement de ${domain} en cours...`);
    // Ici on pourrait déclencher un workflow GitHub Actions
}

function showDNSConfig() {
    alert(`🔧 Configuration DNS:\n\nPour chaque domaine, ajouter:\nCNAME www.domain.com stephanedenis.github.io`);
}

function updateDomains() {
    alert(`🔄 Synchronisation des domaines lancée...`);
    location.reload();
}

// Auto-refresh des status
setInterval(() => {
    console.log('🔄 Vérification status domaines...');
}, 30000);
</script>
