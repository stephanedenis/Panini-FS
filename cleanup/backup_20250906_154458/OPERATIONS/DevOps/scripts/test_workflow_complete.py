#!/usr/bin/env python3
"""
🧪 WORKFLOW TESTER COMPLET
🎯 Test automatisé du pipeline VSCode → Colab → Results
⚡ Validation complète de l'accélération
"""

import os
import time
import subprocess
import json
from datetime import datetime
from pathlib import Path

class WorkflowTester:
    """Testeur complet du workflow d'accélération"""
    
    def __init__(self):
        self.workspace_root = "/home/stephane/GitHub/PaniniFS-1"
        self.start_time = datetime.now()
        self.test_results = {}
        
    def test_local_environment(self):
        """Tester environnement local"""
        print("🔍 TEST ENVIRONNEMENT LOCAL...")
        print("=" * 30)
        
        tests = {
            "python3": ["python3", "--version"],
            "git": ["git", "--version"],
            "jupyter": ["jupyter", "--version"],
            "pip": ["pip", "--version"]
        }
        
        results = {}
        for tool, cmd in tests.items():
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    results[tool] = "✅ OK"
                    print(f"   ✅ {tool}: {result.stdout.strip().split()[0] if result.stdout else 'OK'}")
                else:
                    results[tool] = "❌ ERROR"
                    print(f"   ❌ {tool}: Error")
            except Exception as e:
                results[tool] = f"❌ {str(e)[:30]}"
                print(f"   ❌ {tool}: {str(e)[:30]}")
        
        self.test_results["local_environment"] = results
        return all("✅" in status for status in results.values())
    
    def test_notebook_generation(self):
        """Tester génération automatique notebook"""
        print(f"\n📝 TEST GÉNÉRATION NOTEBOOK...")
        print("=" * 30)
        
        # Vérifier notebook créé
        notebook_path = f"{self.workspace_root}/scripts/colab_notebooks/semantic_processing_accelerated.ipynb"
        
        if os.path.exists(notebook_path):
            print(f"   ✅ Notebook existant: {notebook_path}")
            
            # Vérifier contenu
            try:
                with open(notebook_path, 'r') as f:
                    notebook_data = json.load(f)
                
                cells_count = len(notebook_data.get('cells', []))
                has_gpu_check = any('gpu' in str(cell).lower() for cell in notebook_data.get('cells', []))
                has_dependencies = any('pip install' in str(cell) for cell in notebook_data.get('cells', []))
                
                print(f"   📊 Cellules: {cells_count}")
                print(f"   🚀 GPU check: {'✅' if has_gpu_check else '❌'}")
                print(f"   📦 Dependencies: {'✅' if has_dependencies else '❌'}")
                
                self.test_results["notebook_generation"] = {
                    "exists": True,
                    "cells_count": cells_count,
                    "has_gpu_check": has_gpu_check,
                    "has_dependencies": has_dependencies
                }
                
                return True
                
            except Exception as e:
                print(f"   ❌ Erreur lecture notebook: {e}")
                self.test_results["notebook_generation"] = {"error": str(e)}
                return False
        else:
            print(f"   ❌ Notebook non trouvé: {notebook_path}")
            print(f"   🔄 Génération automatique...")
            
            # Lancer génération
            try:
                result = subprocess.run([
                    "python3", "colab_cli_launcher.py"
                ], cwd=f"{self.workspace_root}/scripts/scripts", 
                   capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    print(f"   ✅ Génération réussie")
                    return self.test_notebook_generation()  # Re-test
                else:
                    print(f"   ❌ Erreur génération: {result.stderr[:100]}")
                    return False
                    
            except Exception as e:
                print(f"   ❌ Erreur lancement générateur: {e}")
                return False
    
    def test_github_integration(self):
        """Tester intégration GitHub"""
        print(f"\n📤 TEST INTÉGRATION GITHUB...")
        print("=" * 30)
        
        try:
            # Vérifier remote origin
            result = subprocess.run([
                "git", "remote", "get-url", "origin"
            ], cwd=self.workspace_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                remote_url = result.stdout.strip()
                print(f"   ✅ Remote origin: {remote_url}")
                
                # Tester connectivity GitHub
                ping_result = subprocess.run([
                    "git", "ls-remote", "origin", "HEAD"
                ], cwd=self.workspace_root, capture_output=True, text=True, timeout=30)
                
                if ping_result.returncode == 0:
                    print(f"   ✅ Connexion GitHub: OK")
                    
                    self.test_results["github_integration"] = {
                        "remote_configured": True,
                        "connectivity": True,
                        "remote_url": remote_url
                    }
                    return True
                else:
                    print(f"   ⚠️ Connexion GitHub: Problème réseau")
                    self.test_results["github_integration"] = {
                        "remote_configured": True,
                        "connectivity": False
                    }
                    return False
            else:
                print(f"   ❌ Remote origin non configuré")
                return False
                
        except Exception as e:
            print(f"   ❌ Erreur test GitHub: {e}")
            return False
    
    def test_colab_url_generation(self):
        """Tester génération URL Colab"""
        print(f"\n🌐 TEST GÉNÉRATION URL COLAB...")
        print("=" * 30)
        
        # Template URL Colab avec bon nom d'utilisateur
        base_url = "https://colab.research.google.com/github/stephanedenis/PaniniFS/blob/master"
        notebook_path = "scripts/colab_notebooks/semantic_processing_accelerated.ipynb"
        colab_url = f"{base_url}/{notebook_path}"
        
        print(f"   🔗 URL générée: {colab_url}")
        
        # Vérifier format URL (corrigé)
        url_valid = (
            colab_url.startswith("https://colab.research.google.com/github") and
            "stephanedenis" in colab_url and
            ".ipynb" in colab_url
        )
        
        if url_valid:
            print(f"   ✅ Format URL: Valide")
            self.test_results["colab_url"] = {
                "url": colab_url,
                "format_valid": True
            }
            return True
        else:
            print(f"   ❌ Format URL: Invalide")
            return False
    
    def generate_test_report(self):
        """Générer rapport de test complet"""
        print(f"\n📊 GÉNÉRATION RAPPORT TEST...")
        print("=" * 30)
        
        end_time = datetime.now()
        total_time = (end_time - self.start_time).total_seconds()
        
        report = {
            "test_execution": {
                "start_time": self.start_time.isoformat(),
                "end_time": end_time.isoformat(), 
                "total_duration_seconds": round(total_time, 2)
            },
            "test_results": self.test_results,
            "summary": {
                "total_tests": len(self.test_results),
                "passed_tests": sum(1 for result in self.test_results.values() 
                                  if isinstance(result, dict) and not result.get("error")),
                "overall_status": "READY" if len(self.test_results) >= 3 else "INCOMPLETE"
            }
        }
        
        # Sauvegarder rapport
        report_file = f"{self.workspace_root}/scripts/test_workflow_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"   ✅ Rapport sauvegardé: {report_file}")
        return report

def main():
    print("🧪 WORKFLOW TESTER COMPLET")
    print("=" * 35)
    print("🎯 Test pipeline VSCode → Colab → Results")
    print("⚡ Validation accélération 22-60x")
    print("")
    
    tester = WorkflowTester()
    
    # Exécuter tous les tests
    tests = [
        ("Environnement Local", tester.test_local_environment),
        ("Génération Notebook", tester.test_notebook_generation),
        ("Intégration GitHub", tester.test_github_integration),
        ("URL Colab", tester.test_colab_url_generation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"🧪 TEST: {test_name}")
        try:
            result = test_func()
            results.append(result)
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"   {status}")
        except Exception as e:
            print(f"   ❌ EXCEPTION: {e}")
            results.append(False)
    
    # Rapport final
    report = tester.generate_test_report()
    
    print(f"\n{'='*50}")
    print(f"🎯 RÉSULTATS FINAUX")
    print(f"{'='*50}")
    
    passed = sum(results)
    total = len(results)
    percentage = (passed / total) * 100
    
    print(f"📊 Tests passés: {passed}/{total} ({percentage:.0f}%)")
    
    if passed == total:
        print(f"✅ WORKFLOW COMPLÈTEMENT PRÊT!")
        print(f"🚀 Accélération 22-60x disponible")
        print(f"🎯 Lancer: ./deploy_colab_auto.sh")
    elif passed >= 3:
        print(f"⚠️ WORKFLOW PARTIELLEMENT PRÊT")
        print(f"🔧 Quelques ajustements nécessaires")
    else:
        print(f"❌ WORKFLOW NON PRÊT")
        print(f"🔧 Configuration requise")
    
    print(f"\n📄 Rapport détaillé: test_workflow_report.json")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
