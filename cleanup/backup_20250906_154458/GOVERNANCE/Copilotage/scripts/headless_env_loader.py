#!/usr/bin/env python3
"""
🔐 LOADER SECRETS ENVIRONNEMENT HEADLESS
======================================
Charge les secrets depuis l'environnement pour autonomie cloud.
"""

import os
import json
import base64
from typing import Optional, Dict, Any

class HeadlessEnvLoader:
    """Charge les secrets en mode headless"""
    
    @staticmethod
    def get_github_token() -> Optional[str]:
        """Récupère le token GitHub"""
        # GitHub Actions fournit automatiquement GITHUB_TOKEN
        return os.environ.get('GITHUB_TOKEN')
    
    @staticmethod
    def get_google_drive_credentials() -> Optional[Dict[str, Any]]:
        """Récupère les credentials Google Drive"""
        creds_env = os.environ.get('GOOGLE_DRIVE_CREDENTIALS')
        if creds_env:
            try:
                # Décode depuis base64 si nécessaire
                if creds_env.startswith('eyJ'):  # Base64 JSON
                    creds_json = base64.b64decode(creds_env).decode()
                else:
                    creds_json = creds_env
                
                return json.loads(creds_json)
            except Exception as e:
                print(f"⚠️ Erreur décodage Google credentials: {e}")
                return None
        return None
    
    @staticmethod
    def get_api_key(service: str) -> Optional[str]:
        """Récupère une clé API"""
        key_map = {
            'arxiv': 'ARXIV_API_KEY',
            'semantic_scholar': 'SEMANTIC_SCHOLAR_API_KEY'
        }
        
        env_var = key_map.get(service.lower())
        if env_var:
            return os.environ.get(env_var)
        return None
    
    @staticmethod
    def is_headless_mode() -> bool:
        """Détecte si en mode headless"""
        return (
            os.environ.get('GITHUB_ACTIONS') == 'true' or
            os.environ.get('COLAB_GPU') is not None or
            not os.environ.get('DISPLAY')
        )
    
    @staticmethod
    def get_fallback_config() -> Dict[str, Any]:
        """Configuration de fallback si secrets manquants"""
        return {
            'github_monitoring': {'enabled': True, 'uses_public_api': True},
            'google_drive_sync': {'enabled': False, 'reason': 'No credentials'},
            'research_apis': {'enabled': True, 'uses_public_endpoints': True},
            'criticism_analysis': {'enabled': True, 'local_only': True}
        }

# Test rapide
if __name__ == "__main__":
    loader = HeadlessEnvLoader()
    
    print("🔐 ÉTAT SECRETS HEADLESS")
    print("=" * 40)
    print(f"Mode headless: {loader.is_headless_mode()}")
    print(f"GitHub token: {'✅ Disponible' if loader.get_github_token() else '❌ Manquant'}")
    print(f"Google Drive: {'✅ Disponible' if loader.get_google_drive_credentials() else '❌ Manquant'}")
    print(f"ArXiv API: {'✅ Disponible' if loader.get_api_key('arxiv') else '❌ Manquant'}")
    
    if not all([loader.get_github_token(), loader.get_google_drive_credentials()]):
        print("\n⚠️ Mode dégradé activé")
        fallback = loader.get_fallback_config()
        for service, config in fallback.items():
            status = "✅" if config['enabled'] else "❌"
            print(f"  {status} {service}: {config}")
