#!/usr/bin/env python3
"""
👁️ MONITORING GITHUB AUTONOME
"""
import requests
import time
import json
from datetime import datetime

class GitHubAutonomousMonitor:
    def __init__(self):
        self.repos = [
            'stephanedenis/PaniniFS',
            'stephanedenis/Panini-DevOps'
        ]
        
    def monitor_continuous(self):
        """Monitoring continu GitHub"""
        while True:
            try:
                for repo in self.repos:
                    self.check_workflows(repo)
                    self.check_issues(repo)
                
                time.sleep(300)  # Check toutes les 5 min
                
            except Exception as e:
                print(f"⚠️ Erreur monitoring: {e}")
                time.sleep(600)
                
    def check_workflows(self, repo):
        """Vérifie workflows GitHub"""
        url = f"https://api.github.com/repos/{repo}/actions/runs"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            failed_runs = [run for run in data['workflow_runs'] 
                          if run['conclusion'] == 'failure']
            
            if failed_runs:
                print(f"🚨 {len(failed_runs)} workflows failed pour {repo}")
                
    def check_issues(self, repo):
        """Vérifie issues GitHub"""
        url = f"https://api.github.com/repos/{repo}/issues"
        response = requests.get(url)
        
        if response.status_code == 200:
            issues = response.json()
            open_issues = [i for i in issues if i['state'] == 'open']
            
            if len(open_issues) > 5:
                print(f"⚠️ {len(open_issues)} issues ouvertes pour {repo}")

if __name__ == "__main__":
    monitor = GitHubAutonomousMonitor()
    monitor.monitor_continuous()
