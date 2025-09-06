#!/usr/bin/env python3
"""
🤖 COLAB AUTONOMOUS CONTROLLER
Contrôle direct de Google Colab via Playwright
- Connexion automatique
- Activation GPU 
- Exécution cellules
- Monitoring temps réel
- Récupération résultats
"""

import asyncio
import time
import json
import re
from pathlib import Path
from playwright.async_api import async_playwright
import subprocess

class ColabAutonomousController:
    def __init__(self, notebook_url, headless=False):
        self.notebook_url = notebook_url
        self.headless = headless
        self.page = None
        self.browser = None
        self.status = {
            'connected': False,
            'gpu_enabled': False,
            'cells_executed': 0,
            'current_cell': None,
            'outputs': []
        }
        
    async def start_browser(self):
        """Démarrage navigateur avec configuration optimale"""
        print("🚀 Démarrage navigateur autonome...")
        
        playwright = await async_playwright().start()
        
        # Configuration navigateur pour contourner détection
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        
        # Création contexte avec user agent réaliste
        context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        self.page = await context.new_page()
        
        # Injection script anti-détection
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
        
        print("✅ Navigateur autonome prêt")
        
    async def connect_to_colab(self):
        """Connexion automatique à Colab"""
        print(f"🌐 Connexion à Colab: {self.notebook_url}")
        
        try:
            await self.page.goto(self.notebook_url, wait_until='networkidle')
            await asyncio.sleep(3)
            
            # Vérification chargement
            title = await self.page.title()
            if 'colab' in title.lower():
                print("✅ Colab chargé avec succès")
                self.status['connected'] = True
                return True
            else:
                print(f"❌ Problème chargement Colab: {title}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur connexion Colab: {e}")
            return False
    
    async def enable_gpu(self):
        """Activation automatique GPU"""
        print("⚡ Activation GPU automatique...")
        
        try:
            # Clic menu Runtime
            await self.page.click('text=Runtime')
            await asyncio.sleep(1)
            
            # Clic Change runtime type
            await self.page.click('text=Change runtime type')
            await asyncio.sleep(2)
            
            # Sélection GPU
            gpu_selector = 'select[aria-label="Hardware accelerator"]'
            await self.page.select_option(gpu_selector, 'GPU')
            await asyncio.sleep(1)
            
            # Clic Save
            await self.page.click('button:has-text("Save")')
            await asyncio.sleep(3)
            
            print("✅ GPU activé - Runtime redémarrage...")
            self.status['gpu_enabled'] = True
            
            # Attendre reconnexion
            await asyncio.sleep(10)
            return True
            
        except Exception as e:
            print(f"❌ Erreur activation GPU: {e}")
            return False
    
    async def connect_runtime(self):
        """Connexion au runtime"""
        print("🔌 Connexion au runtime...")
        
        try:
            # Recherche bouton Connect
            connect_button = await self.page.query_selector('button:has-text("Connect")')
            if connect_button:
                await connect_button.click()
                print("🔄 Connexion en cours...")
                
                # Attendre connexion
                for _ in range(30):  # Max 30s
                    await asyncio.sleep(1)
                    connected_indicator = await self.page.query_selector('[title*="Connected"]')
                    if connected_indicator:
                        print("✅ Runtime connecté!")
                        return True
                        
                print("⚠️ Timeout connexion runtime")
                return False
            else:
                print("✅ Runtime déjà connecté")
                return True
                
        except Exception as e:
            print(f"❌ Erreur connexion runtime: {e}")
            return False
    
    async def execute_cell(self, cell_index=0, wait_completion=True):
        """Exécution cellule spécifique"""
        print(f"▶️ Exécution cellule {cell_index}...")
        
        try:
            # Sélection cellule
            cells = await self.page.query_selector_all('[data-colab-type="code"]')
            if cell_index >= len(cells):
                print(f"❌ Cellule {cell_index} inexistante (total: {len(cells)})")
                return False
            
            cell = cells[cell_index]
            await cell.click()
            await asyncio.sleep(0.5)
            
            # Exécution Shift+Enter
            await self.page.keyboard.press('Shift+Enter')
            
            self.status['current_cell'] = cell_index
            self.status['cells_executed'] += 1
            
            if wait_completion:
                return await self.wait_cell_completion(cell_index)
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur exécution cellule {cell_index}: {e}")
            return False
    
    async def wait_cell_completion(self, cell_index, timeout=300):
        """Attendre fin d'exécution cellule"""
        print(f"⏳ Attente fin exécution cellule {cell_index}...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Vérification spinner execution
                spinner = await self.page.query_selector(f'[data-cell-index="{cell_index}"] .cell-execution-indicator')
                if not spinner:
                    print(f"✅ Cellule {cell_index} terminée")
                    await self.capture_cell_output(cell_index)
                    return True
                    
                await asyncio.sleep(2)
                
            except Exception:
                await asyncio.sleep(2)
                continue
        
        print(f"⚠️ Timeout cellule {cell_index}")
        return False
    
    async def capture_cell_output(self, cell_index):
        """Capture sortie cellule"""
        try:
            output_selector = f'[data-cell-index="{cell_index}"] .output'
            output_elements = await self.page.query_selector_all(output_selector)
            
            outputs = []
            for element in output_elements:
                text = await element.text_content()
                if text and text.strip():
                    outputs.append(text.strip())
            
            if outputs:
                self.status['outputs'].append({
                    'cell_index': cell_index,
                    'outputs': outputs,
                    'timestamp': time.time()
                })
                print(f"📊 Sortie cellule {cell_index} capturée: {len(outputs)} éléments")
            
        except Exception as e:
            print(f"❌ Erreur capture sortie: {e}")
    
    async def monitor_execution(self):
        """Monitoring continu de l'exécution"""
        print("📊 Démarrage monitoring continu...")
        
        while True:
            try:
                # Vérification état général
                page_title = await self.page.title()
                
                # Détection erreurs
                error_elements = await self.page.query_selector_all('.error')
                if error_elements:
                    print("⚠️ Erreurs détectées dans le notebook")
                
                # Statistiques
                total_cells = len(await self.page.query_selector_all('[data-colab-type="code"]'))
                print(f"📈 État: {self.status['cells_executed']}/{total_cells} cellules exécutées")
                
                await asyncio.sleep(10)
                
            except Exception as e:
                print(f"❌ Erreur monitoring: {e}")
                await asyncio.sleep(10)
    
    async def execute_full_notebook(self):
        """Exécution complète du notebook"""
        print("🚀 Exécution complète du notebook...")
        
        try:
            # Menu Runtime > Run all
            await self.page.click('text=Runtime')
            await asyncio.sleep(1)
            await self.page.click('text=Run all')
            
            print("▶️ Exécution de toutes les cellules lancée...")
            
            # Monitoring de l'exécution
            start_time = time.time()
            while True:
                # Vérification si exécution terminée
                running_indicators = await self.page.query_selector_all('.cell-execution-indicator')
                
                if not running_indicators:
                    execution_time = time.time() - start_time
                    print(f"✅ Notebook entièrement exécuté en {execution_time:.1f}s")
                    return True
                
                await asyncio.sleep(5)
                
                # Timeout sécurité
                if time.time() - start_time > 1800:  # 30 minutes max
                    print("⚠️ Timeout exécution notebook")
                    return False
                
        except Exception as e:
            print(f"❌ Erreur exécution complète: {e}")
            return False
    
    async def save_status(self, filepath):
        """Sauvegarde état controller"""
        with open(filepath, 'w') as f:
            json.dump(self.status, f, indent=2)
        print(f"💾 État sauvé: {filepath}")
    
    async def close(self):
        """Fermeture propre"""
        if self.browser:
            await self.browser.close()
        print("🔚 Controller fermé")

async def main():
    """Fonction principale - lancement autonome"""
    print("🤖 COLAB AUTONOMOUS CONTROLLER - DÉMARRAGE")
    print("=" * 50)
    
    # Configuration
    notebook_url = "https://colab.research.google.com/github/stephanedenis/PaniniFS/blob/master/scripts/colab_notebooks/semantic_processing_accelerated.ipynb"
    
    controller = ColabAutonomousController(notebook_url, headless=False)
    
    try:
        # Séquence d'automatisation complète
        await controller.start_browser()
        
        if await controller.connect_to_colab():
            if await controller.enable_gpu():
                if await controller.connect_runtime():
                    # Démarrage monitoring en parallèle
                    monitor_task = asyncio.create_task(controller.monitor_execution())
                    
                    # Exécution notebook
                    await controller.execute_full_notebook()
                    
                    # Sauvegarde état final
                    await controller.save_status('/home/stephane/GitHub/PaniniFS-1/scripts/colab_execution_status.json')
                    
                    monitor_task.cancel()
                    
        print("🎉 PROCESSUS AUTONOME TERMINÉ")
        
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
    finally:
        await controller.close()

if __name__ == "__main__":
    asyncio.run(main())
