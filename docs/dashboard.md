# 🏕️ Dashboard Camping Strategy

!!! info "Mode Camping Actif"
    **Totoro:** Terminal minimal + VS Code + GitHub Copilot  
    **Cloud:** Colab Master + GitHub Actions + Vercel  
    **Monitoring:** Temps réel via JSON + MkDocs

## 📊 État Système en Temps Réel

<div id="system-status-loading">
    <p>⏳ Chargement de l'état du système...</p>
</div>

<div id="system-status" style="display: none;">
    <!-- Contenu dynamique injecté par JavaScript -->
</div>

## 🤖 Agents Autonomes

<div id="agents-status">
    <!-- Agents chargés dynamiquement -->
</div>

## 🌐 Domaines Multi-Sites

<div id="domains-status">
    <!-- Domaines chargés dynamiquement -->
</div>

## 🔧 Workflows GitHub

<div id="workflows-status">
    <!-- Workflows chargés dynamiquement -->
</div>

## 🔗 Liens Rapides

- [☁️ Colab Master Orchestrator](https://colab.research.google.com/github/stephanedenis/PaniniFS/blob/master/ECOSYSTEM/colab-notebooks/PaniniFS-Master-Orchestrator.ipynb)
- [🔧 GitHub Actions](https://github.com/stephanedenis/PaniniFS/actions)
- [📱 Repository GitHub](https://github.com/stephanedenis/PaniniFS)
- [⚙️ GitHub Pages Settings](https://github.com/stephanedenis/PaniniFS/settings/pages)

<script>
// Chargement dynamique de l'état système
async function loadSystemStatus() {
    try {
        const response = await fetch('./data/system_status.json');
        const data = await response.json();
        
        document.getElementById('system-status-loading').style.display = 'none';
        document.getElementById('system-status').style.display = 'block';
        
        // Injection du contenu dynamique
        renderSystemStatus(data);
        renderAgentsStatus(data.agents);
        renderDomainsStatus(data.domains);
        renderWorkflowsStatus(data.workflows);
        
    } catch (error) {
        console.error('Erreur chargement état système:', error);
        document.getElementById('system-status-loading').innerHTML = 
            '<p>❌ Erreur chargement données. Vérifiez la connexion.</p>';
    }
}

function renderSystemStatus(data) {
    const campingStatus = data.camping_strategy.active ? '🏕️ ACTIF' : '❌ INACTIF';
    const overallHealth = data.system_health.overall_status === 'healthy' ? '🟢 SAIN' : '🟡 ATTENTION';
    
    const html = `
        <div class="md-typeset">
            <div class="admonition success">
                <p class="admonition-title">État Général: ${overallHealth}</p>
                <ul>
                    <li><strong>Camping Strategy:</strong> ${campingStatus}</li>
                    <li><strong>Agents Opérationnels:</strong> ${data.system_health.agents_operational}/13+</li>
                    <li><strong>Dernière Mise à Jour:</strong> ${new Date(data.timestamp).toLocaleString('fr-FR')}</li>
                    <li><strong>Externalisation:</strong> ${data.system_health.externalization_complete ? '✅ Complète' : '🔄 En cours'}</li>
                </ul>
            </div>
        </div>
    `;
    
    document.getElementById('system-status').innerHTML = html;
}

function renderAgentsStatus(agents) {
    let html = '<div class="md-typeset">';
    
    Object.entries(agents.categories).forEach(([category, data]) => {
        const categoryIcons = {
            research: '📚',
            critique: '🔥', 
            orchestrators: '🎯',
            monitoring: '📡',
            devops: '🏗️'
        };
        
        html += `
            <details class="details">
                <summary><strong>${categoryIcons[category]} ${category.toUpperCase()} (${data.count})</strong></summary>
                <ul>
        `;
        
        data.agents.forEach(agent => {
            const statusIcon = agent.status === 'active' ? '🟢' : 
                             agent.status === 'backup' ? '🟡' : '⚪';
            const lastExec = agent.last_execution ? 
                `<br><small>Dernière exéc: ${new Date(agent.last_execution).toLocaleString('fr-FR')}</small>` : '';
            
            html += `
                <li>
                    ${statusIcon} <strong>${agent.name}</strong> (${agent.status})
                    <br><code>${agent.path}</code>
                    ${lastExec}
                    <br><small>Features: ${agent.features.join(', ')}</small>
                </li>
            `;
        });
        
        html += '</ul></details>';
    });
    
    html += '</div>';
    document.getElementById('agents-status').innerHTML = html;
}

function renderDomainsStatus(domains) {
    let html = `
        <div class="md-typeset">
            <p><strong>Total:</strong> ${domains.total} domaines configurés</p>
            <ul>
    `;
    
    domains.configured.forEach(domain => {
        const statusIcon = domain.status === 'online' ? '🟢' : '🔴';
        const sslIcon = domain.ssl === 'active' ? '🔒' : '🔓';
        
        html += `
            <li>
                ${statusIcon} <strong>${domain.domain}</strong> ${sslIcon}
                <br><small>CNAME: ${domain.cname}</small>
            </li>
        `;
    });
    
    html += '</ul></div>';
    document.getElementById('domains-status').innerHTML = html;
}

function renderWorkflowsStatus(workflows) {
    const status = workflows.github_actions.status === 'repaired' ? '✅ RÉPARÉS' : '🔄 EN COURS';
    const lastRun = new Date(workflows.github_actions.last_successful_run).toLocaleString('fr-FR');
    
    const html = `
        <div class="md-typeset">
            <div class="admonition tip">
                <p class="admonition-title">GitHub Actions: ${status}</p>
                <ul>
                    <li><strong>Dernière Exécution Réussie:</strong> ${lastRun}</li>
                    <li><strong>Corrections Récentes:</strong></li>
                    <ul>
                        ${workflows.github_actions.recent_fixes.map(fix => 
                            `<li>${fix.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</li>`
                        ).join('')}
                    </ul>
                </ul>
            </div>
        </div>
    `;
    
    document.getElementById('workflows-status').innerHTML = html;
}

// Auto-refresh toutes les 30 secondes
setInterval(loadSystemStatus, 30000);

// Chargement initial
document.addEventListener('DOMContentLoaded', loadSystemStatus);
</script>

<style>
.details summary {
    cursor: pointer;
    padding: 10px;
    background: rgba(0, 100, 200, 0.1);
    border-radius: 5px;
    margin: 5px 0;
}

.details[open] summary {
    margin-bottom: 10px;
}

.details ul {
    margin-left: 20px;
}

.details li {
    margin: 10px 0;
    padding: 8px;
    background: rgba(0, 0, 0, 0.05);
    border-radius: 3px;
}
</style>
