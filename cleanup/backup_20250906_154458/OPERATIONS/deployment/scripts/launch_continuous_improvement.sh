#!/bin/bash
"""
🚀 LANCEUR AMÉLIORATION CONTINUE AVEC SURVEILLANCE GITHUB
=========================================================

Script de lancement pour système d'amélioration continue autonome:
- Agent Recherche Théorique (mise à jour connaissances 30 ans linguistique)
- Agent Critique Adverse (amélioration continue tous projets)
- Surveillance GitHub Workflows (alertes automatiques)
- Orchestrateur coordination (100% externalisé)

Optimisé pour environnement camping avec fonctionnement autonome.

Usage:
  ./launch_continuous_improvement.sh [mode]
  
Modes:
  - monitor   : Monitoring continu avec surveillance GitHub (défaut)
  - test      : Test 5 minutes
  - github    : Surveillance GitHub uniquement
  - research  : Agent recherche théorique uniquement
  - critic    : Agent critique adverse uniquement
"""

Usage:
./launch_continuous_improvement.sh [mode]

Modes:
- demo: Exécution démonstration immédiate
- autonomous: Démarrage mode autonome continu
- research: Agent recherche théorique seulement
- critic: Agent critique adverse seulement
- stop: Arrêt de tous les agents

Fonctionnement 100% autonome et externalisé.
"""

set -e  # Arrêt sur erreur

# Configuration
BASE_DIR="/home/stephane/GitHub/PaniniFS-1"
AGENTS_DIR="$BASE_DIR/Copilotage/agents"
VENV_DIR="$BASE_DIR/venv_ci"
LOG_DIR="$BASE_DIR/logs"
PID_FILE="$BASE_DIR/ci_orchestrator.pid"

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Fonctions utilitaires
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

# Banner
print_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║  🤖 SYSTÈME AMÉLIORATION CONTINUE AUTONOME PANINI            ║"
    echo "║                                                              ║"
    echo "║  🔬 Agent Recherche Théorique (Linguistique 30 ans)         ║"
    echo "║  🔥 Agent Critique Adverse (Amélioration Continue)           ║"
    echo "║  🤖 Orchestrateur (100% Externalisé)                        ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Vérification prérequis
check_prerequisites() {
    log_step "Vérification prérequis..."
    
    # Python 3.8+
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 requis mais non installé"
        exit 1
    fi
    
    python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    if [ "$(echo "$python_version >= 3.8" | bc -l)" -eq 0 ]; then
        log_error "Python 3.8+ requis (détecté: $python_version)"
        exit 1
    fi
    
    # Git
    if ! command -v git &> /dev/null; then
        log_error "Git requis mais non installé"
        exit 1
    fi
    
    # Répertoire projet
    if [ ! -d "$BASE_DIR" ]; then
        log_error "Répertoire projet non trouvé: $BASE_DIR"
        exit 1
    fi
    
    log_success "Prérequis validés"
}

# Setup environnement virtuel
setup_virtual_environment() {
    log_step "Configuration environnement virtuel..."
    
    # Création venv si inexistant
    if [ ! -d "$VENV_DIR" ]; then
        log_info "Création environnement virtuel: $VENV_DIR"
        python3 -m venv "$VENV_DIR"
    fi
    
    # Activation
    source "$VENV_DIR/bin/activate"
    
    # Mise à jour pip
    pip install --upgrade pip > /dev/null 2>&1
    
    # Installation dépendances
    log_info "Installation dépendances..."
    pip install -q aiohttp requests beautifulsoup4 schedule asyncio python-dateutil
    
    # Dépendances optionnelles pour recherche académique
    pip install -q xml2dict feedparser scholarly arxiv
    
    log_success "Environnement virtuel configuré"
}

# Création répertoires
setup_directories() {
    log_step "Configuration répertoires..."
    
    # Répertoires nécessaires
    mkdir -p "$LOG_DIR"
    mkdir -p "$AGENTS_DIR"
    
    # Fichiers log
    touch "$LOG_DIR/orchestrator.log"
    touch "$LOG_DIR/research_agent.log"
    touch "$LOG_DIR/critic_agent.log"
    
    log_success "Répertoires configurés"
}

# Vérification agents
check_agents() {
    log_step "Vérification agents..."
    
    required_agents=(
        "theoretical_research_agent.py"
        "adversarial_critic_agent.py"
        "continuous_improvement_orchestrator.py"
        "orchestrator_with_github.py"
    )
    
    # Vérifier scripts surveillance
    github_script="$BASE_DIR/Copilotage/scripts/github_workflow_monitor.py"
    if [ ! -f "$github_script" ]; then
        log_error "Script surveillance GitHub manquant: $github_script"
        exit 1
    fi
    
    for agent in "${required_agents[@]}"; do
        if [ ! -f "$AGENTS_DIR/$agent" ]; then
            log_error "Agent manquant: $agent"
            exit 1
        fi
    done
    
    log_success "Tous les agents présents"
}

# Arrêt processus existants
stop_existing_processes() {
    log_step "Arrêt processus existants..."
    
    # Vérification PID file
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            log_info "Arrêt orchestrateur existant (PID: $PID)"
            kill "$PID"
            sleep 2
            
            # Force kill si nécessaire
            if ps -p "$PID" > /dev/null 2>&1; then
                log_warning "Force kill orchestrateur"
                kill -9 "$PID"
            fi
        fi
        rm -f "$PID_FILE"
    fi
    
    # Arrêt autres processus agents
    pkill -f "theoretical_research_agent.py" 2>/dev/null || true
    pkill -f "adversarial_critic_agent.py" 2>/dev/null || true
    pkill -f "continuous_improvement_orchestrator.py" 2>/dev/null || true
    
    log_success "Processus existants arrêtés"
}

# Mode démonstration
run_demo_mode() {
    log_step "🎯 MODE DÉMONSTRATION"
    
    source "$VENV_DIR/bin/activate"
    cd "$BASE_DIR"
    
    echo -e "${CYAN}Exécution cycle démonstration complet...${NC}"
    
    # Agent recherche théorique
    log_info "1️⃣ Agent Recherche Théorique..."
    python3 "$AGENTS_DIR/theoretical_research_agent.py" 2>&1 | tee "$LOG_DIR/demo_research.log"
    
    echo ""
    
    # Agent critique adverse  
    log_info "2️⃣ Agent Critique Adverse..."
    python3 "$AGENTS_DIR/adversarial_critic_agent.py" 2>&1 | tee "$LOG_DIR/demo_critic.log"
    
    echo ""
    
    # Orchestrateur analyse croisée
    log_info "3️⃣ Orchestrateur (analyse croisée)..."
    python3 -c "
from $AGENTS_DIR.continuous_improvement_orchestrator import ContinuousImprovementOrchestrator
orchestrator = ContinuousImprovementOrchestrator()
orchestrator._cross_analysis_research_criticism()
orchestrator._generate_comprehensive_report()
print('✅ Démonstration terminée - Voir rapports générés')
" 2>&1 | tee "$LOG_DIR/demo_orchestrator.log"
    
    log_success "🎉 Démonstration terminée!"
    log_info "Consultez les rapports générés dans $BASE_DIR"
}

# Mode autonome
run_autonomous_mode() {
    log_step "🤖 MODE AUTONOME CONTINU"
    
    source "$VENV_DIR/bin/activate"
    cd "$BASE_DIR"
    
    # Lancement orchestrateur avec surveillance GitHub
    log_info "Démarrage orchestrateur avec surveillance GitHub..."
    
    nohup python3 "$AGENTS_DIR/orchestrator_with_github.py" \
        > "$LOG_DIR/orchestrator.log" 2>&1 &
    
    ORCHESTRATOR_PID=$!
    echo $ORCHESTRATOR_PID > "$PID_FILE"
    
    log_success "Orchestrateur + GitHub surveillance démarré (PID: $ORCHESTRATOR_PID)"
    log_info "Log: tail -f $LOG_DIR/orchestrator.log"
    
    # Configuration systemd pour persistance (optionnel)
    create_systemd_service
    
    echo -e "${GREEN}"
    echo "🎉 SYSTÈME AMÉLIORATION CONTINUE AUTONOME DÉMARRÉ!"
    echo ""
    echo "📊 Monitoring:"
    echo "   tail -f $LOG_DIR/orchestrator.log"
    echo ""
    echo "🛑 Arrêt:"
    echo "   $0 stop"
    echo ""
    echo "📈 Rapports générés quotidiennement dans:"
    echo "   $BASE_DIR/"
    echo -e "${NC}"
}

# Agent recherche seulement
run_research_only() {
    log_step "🔬 AGENT RECHERCHE THÉORIQUE SEULEMENT"
    
    source "$VENV_DIR/bin/activate"
    cd "$BASE_DIR"
    
    python3 "$AGENTS_DIR/theoretical_research_agent.py" 2>&1 | tee "$LOG_DIR/research_solo.log"
    
    log_success "Agent recherche théorique terminé"
}

# Agent critique seulement
run_critic_only() {
    log_step "🔥 AGENT CRITIQUE ADVERSE SEULEMENT"
    
    source "$VENV_DIR/bin/activate"
    cd "$BASE_DIR"
    
    python3 "$AGENTS_DIR/adversarial_critic_agent.py" 2>&1 | tee "$LOG_DIR/critic_solo.log"
    
    log_success "Agent critique adverse terminé"
}

# Création service systemd (optionnel)
create_systemd_service() {
    if command -v systemctl &> /dev/null && [ "$EUID" -eq 0 ]; then
        log_info "Création service systemd..."
        
        cat > /etc/systemd/system/panini-ci.service << EOF
[Unit]
Description=PaniniFS Continuous Improvement System
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$BASE_DIR
Environment=PATH=$VENV_DIR/bin
ExecStart=$VENV_DIR/bin/python $AGENTS_DIR/continuous_improvement_orchestrator.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
        
        systemctl daemon-reload
        systemctl enable panini-ci.service
        systemctl start panini-ci.service
        
        log_success "Service systemd créé et démarré"
        log_info "Commandes: systemctl [start|stop|status] panini-ci"
    fi
}

# Affichage status
show_status() {
    log_step "📊 STATUS SYSTÈME"
    
    echo -e "${CYAN}Processus actifs:${NC}"
    ps aux | grep -E "(theoretical_research|adversarial_critic|continuous_improvement)" | grep -v grep || echo "Aucun processus actif"
    
    echo ""
    echo -e "${CYAN}Fichiers PID:${NC}"
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "Orchestrateur actif (PID: $PID)"
        else
            echo "PID file obsolète"
            rm -f "$PID_FILE"
        fi
    else
        echo "Aucun PID file"
    fi
    
    echo ""
    echo -e "${CYAN}Logs récents:${NC}"
    if [ -f "$LOG_DIR/orchestrator.log" ]; then
        echo "Dernières lignes orchestrator.log:"
        tail -5 "$LOG_DIR/orchestrator.log" 2>/dev/null || echo "Log vide"
    fi
    
    echo ""
    echo -e "${CYAN}Rapports disponibles:${NC}"
    ls -la "$BASE_DIR"/*report*.json 2>/dev/null | head -5 || echo "Aucun rapport"
}

# Mode aide
show_help() {
    echo -e "${CYAN}🚀 LANCEUR AMÉLIORATION CONTINUE AUTONOME${NC}"
    echo ""
    echo "Usage: $0 [mode]"
    echo ""
    echo "Modes disponibles:"
    echo "  demo        - Exécution démonstration immédiate (tous agents)"
    echo "  autonomous  - Démarrage mode autonome continu (arrière-plan)"
    echo "  research    - Agent recherche théorique seulement"
    echo "  critic      - Agent critique adverse seulement"
    echo "  status      - Affichage status système"
    echo "  stop        - Arrêt de tous les agents"
    echo "  help        - Affiche cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 demo              # Test complet immédiat"
    echo "  $0 autonomous        # Démarrage système autonome"
    echo "  $0 status            # Vérification status"
    echo "  $0 stop              # Arrêt système"
    echo ""
    echo "Configuration:"
    echo "  Base dir: $BASE_DIR"
    echo "  Agents dir: $AGENTS_DIR"  
    echo "  Logs dir: $LOG_DIR"
    echo "  Venv: $VENV_DIR"
}

# Fonction principale
main() {
    print_banner
    
    MODE=${1:-"help"}
    
    case $MODE in
        "demo")
            check_prerequisites
            setup_virtual_environment
            setup_directories
            check_agents
            stop_existing_processes
            run_demo_mode
            ;;
        "autonomous")
            check_prerequisites
            setup_virtual_environment
            setup_directories
            check_agents
            stop_existing_processes
            run_autonomous_mode
            ;;
        "research")
            check_prerequisites
            setup_virtual_environment
            setup_directories
            check_agents
            run_research_only
            ;;
        "critic")
            check_prerequisites
            setup_virtual_environment
            setup_directories
            check_agents
            run_critic_only
            ;;
        "status")
            show_status
            ;;
        "stop")
            stop_existing_processes
            log_success "Tous les agents arrêtés"
            ;;
        "github")
            check_prerequisites
            setup_virtual_environment
            setup_directories
            log_step "🔍 SURVEILLANCE GITHUB UNIQUEMENT"
            source "$VENV_DIR/bin/activate"
            cd "$BASE_DIR"
            python3 Copilotage/scripts/github_workflow_monitor.py
            ;;
        "test")
            check_prerequisites
            setup_virtual_environment
            setup_directories
            check_agents
            log_step "🧪 MODE TEST 5 MINUTES"
            source "$VENV_DIR/bin/activate"
            cd "$BASE_DIR"
            timeout 300 python3 "$AGENTS_DIR/orchestrator_with_github.py" || true
            log_success "Test terminé"
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Exécution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
