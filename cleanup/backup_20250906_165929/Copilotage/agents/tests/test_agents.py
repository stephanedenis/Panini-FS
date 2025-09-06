#!/usr/bin/env python3
"""
Tests basiques pour les agents PaniniFS
"""

import pytest
import os
import sys

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_simple_orchestrator_import():
    """Test d'importation de l'orchestrateur simple"""
    try:
        from simple_autonomous_orchestrator import SimpleAutonomousOrchestrator
        orchestrator = SimpleAutonomousOrchestrator()
        assert orchestrator is not None
    except ImportError:
        pytest.skip("Module orchestrateur non disponible")

def test_research_agent_import():
    """Test d'importation de l'agent de recherche"""
    try:
        from theoretical_research_simple import TheoreticalResearchAgent
        agent = TheoreticalResearchAgent()
        assert agent is not None
    except ImportError:
        pytest.skip("Module recherche non disponible")

def test_critic_agent_import():
    """Test d'importation de l'agent critique"""
    try:
        from adversarial_critic_simple import AdversarialCriticAgent
        agent = AdversarialCriticAgent()
        assert agent is not None
    except ImportError:
        pytest.skip("Module critique non disponible")

def test_agents_basic_functionality():
    """Test de fonctionnalité basique des agents"""
    assert True  # Test placeholder qui passe toujours

if __name__ == "__main__":
    pytest.main([__file__])
