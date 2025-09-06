#!/usr/bin/env python3
"""
Copilote Autonome - Mode de fonctionnement asynchrone
Gère la communication bidirectionnelle pendant le travail
"""
import time
import json
import subprocess
from pathlib import Path

class AutonomousCopilot:
    def __init__(self, workspace_path):
        self.workspace = Path(workspace_path)
        self.status_file = self.workspace / "copilot-status.json"
        self.commands_queue = self.workspace / "copilot-commands.json"
        self.results_queue = self.workspace / "copilot-results.json"
        self.running_processes = {}
        
    def start_background_task(self, task_id, command, cwd=None):
        """Lance une tâche en arrière-plan avec suivi"""
        try:
            process = subprocess.Popen(
                command, shell=True, cwd=cwd,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True
            )
            self.running_processes[task_id] = {
                'process': process,
                'command': command,
                'start_time': time.time(),
                'status': 'running'
            }
            self.update_status()
            return True
        except Exception as e:
            self.log_error(task_id, str(e))
            return False
            
    def check_processes(self):
        """Vérifie l'état de tous les processus en cours"""
        completed = []
        for task_id, task_info in self.running_processes.items():
            process = task_info['process']
            if process.poll() is not None:  # Processus terminé
                stdout, stderr = process.communicate()
                completed.append({
                    'task_id': task_id,
                    'command': task_info['command'],
                    'return_code': process.returncode,
                    'stdout': stdout,
                    'stderr': stderr,
                    'duration': time.time() - task_info['start_time']
                })
                
        # Nettoyer les processus terminés
        for result in completed:
            del self.running_processes[result['task_id']]
            
        if completed:
            self.save_results(completed)
            
        self.update_status()
        return completed
        
    def update_status(self):
        """Met à jour le fichier de statut"""
        status = {
            'timestamp': time.time(),
            'running_tasks': len(self.running_processes),
            'tasks': {
                task_id: {
                    'command': info['command'][:50] + '...' if len(info['command']) > 50 else info['command'],
                    'duration': time.time() - info['start_time'],
                    'status': info['status']
                }
                for task_id, info in self.running_processes.items()
            }
        }
        
        with open(self.status_file, 'w') as f:
            json.dump(status, f, indent=2)
            
    def save_results(self, results):
        """Sauvegarde les résultats des tâches terminées"""
        existing_results = []
        if self.results_queue.exists():
            with open(self.results_queue, 'r') as f:
                existing_results = json.load(f)
                
        existing_results.extend(results)
        
        with open(self.results_queue, 'w') as f:
            json.dump(existing_results, f, indent=2)
            
    def log_error(self, task_id, error):
        """Log les erreurs"""
        error_log = {
            'timestamp': time.time(),
            'task_id': task_id,
            'error': error
        }
        
        error_file = self.workspace / "copilot-errors.json"
        existing_errors = []
        if error_file.exists():
            with open(error_file, 'r') as f:
                existing_errors = json.load(f)
                
        existing_errors.append(error_log)
        
        with open(error_file, 'w') as f:
            json.dump(existing_errors, f, indent=2)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: autonomous-copilot.py <workspace> <mode>")
        sys.exit(1)
        
    workspace = sys.argv[1]
    mode = sys.argv[2]
    
    copilot = AutonomousCopilot(workspace)
    
    if mode == "daemon":
        # Mode démon - surveillance continue
        while True:
            completed = copilot.check_processes()
            if completed:
                print(f"Tâches terminées: {len(completed)}")
            time.sleep(2)
    elif mode == "status":
        # Affichage du statut
        if copilot.status_file.exists():
            with open(copilot.status_file, 'r') as f:
                status = json.load(f)
                print(json.dumps(status, indent=2))
    elif mode == "results":
        # Affichage des résultats
        if copilot.results_queue.exists():
            with open(copilot.results_queue, 'r') as f:
                results = json.load(f)
                print(json.dumps(results, indent=2))
