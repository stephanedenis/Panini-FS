#!/usr/bin/env python3
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_github_workflow_monitor_smoke():
    from github_workflow_monitor import GitHubWorkflowMonitor
    mon = GitHubWorkflowMonitor()
    data = mon.check_all_repos_status()
    assert isinstance(data, dict)
    assert "user" in data and "repos" in data and "summary" in data
    assert isinstance(data["repos"], list)