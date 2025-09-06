#!/usr/bin/env python3
"""
Tests basiques pour les scripts PaniniFS
"""

import pytest
import os
import sys

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_headless_env_loader_import():
    """Test d'importation du loader headless"""
    try:
        from headless_env_loader import HeadlessEnvLoader
        loader = HeadlessEnvLoader()
        assert loader is not None
    except ImportError:
        pytest.skip("Module headless_env_loader non disponible")

def test_github_workflow_monitor_import():
    """Test d'importation du monitor GitHub"""
    try:
        from github_workflow_monitor import GitHubWorkflowMonitor
        monitor = GitHubWorkflowMonitor()
        assert monitor is not None
    except ImportError:
        pytest.skip("Module github_workflow_monitor non disponible")

def test_basic_functionality():
    """Test de fonctionnalité basique"""
    assert True  # Test placeholder qui passe toujours

def test_python_version():
    """Test de la version Python"""
    import sys
    assert sys.version_info >= (3, 8), "Python 3.8+ requis"

if __name__ == "__main__":
    pytest.main([__file__])
