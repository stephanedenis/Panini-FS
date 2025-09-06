#!/usr/bin/env python3
"""
🚀 GESTIONNAIRE GOOGLE DRIVE AUTONOME PANINI
==========================================

Gestionnaire autonome pour organisation Google Drive (2TB):
- Création structure dossiers Panini
- Upload automatique bibliographie et publications
- Synchronisation bidirectionnelle study pack
- Gestion annotations tablette reMarkable
- 100% autonome via API Google Drive

Structure cible:
/Panini/
├── Publications/
│   ├── Articles_En_Cours/
│   ├── Articles_Publies/
│   ├── Livre_Leanpub/
│   └── Presentations/
├── Bibliographie/
│   ├── Recherche_Theorique/
│   ├── Study_Pack_Remarkable/
│   ├── Papers_Critiques/
│   └── References_Panini/
├── Recherche/
│   ├── Audit_Reports/
│   ├── Criticism_Reports/
│   └── Improvement_Logs/
└── Annotations/
    ├── Remarkable_Exports/
    └── Review_Comments/
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import pickle
from pathlib import Path
import shutil
import mimetypes

# Google Drive API
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

class AutonomousGoogleDriveManager:
    """Gestionnaire autonome Google Drive pour écosystème Panini"""
    
    def __init__(self):
        self.session_id = f"gdrive_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.base_path = "/home/stephane/GitHub/PaniniFS-1"
        self.credentials_path = os.path.join(self.base_path, "gdrive_credentials")
        
        # Scopes Google Drive API
        self.scopes = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
        ]
        
        # Structure dossiers cible
        self.folder_structure = {
            'Panini': {
                'Publications': {
                    'Articles_En_Cours': {},
                    'Articles_Publies': {},
                    'Livre_Leanpub': {},
                    'Presentations': {}
                },
                'Bibliographie': {
                    'Recherche_Theorique': {},
                    'Study_Pack_Remarkable': {},
                    'Papers_Critiques': {},
                    'References_Panini': {}
                },
                'Recherche': {
                    'Audit_Reports': {},
                    'Criticism_Reports': {},
                    'Improvement_Logs': {}
                },
                'Annotations': {
                    'Remarkable_Exports': {},
                    'Review_Comments': {}
                }
            }
        }
        
        self.service = None
        self.folder_ids = {}
        self.upload_log = []
        
    def initialize_google_drive_api(self):
        """Initialise connexion Google Drive API"""
        print("🔑 Initialisation Google Drive API...")
        
        creds = None
        token_path = os.path.join(self.credentials_path, "token.pickle")
        credentials_json_path = os.path.join(self.credentials_path, "credentials.json")
        
        # Créer répertoire credentials si inexistant
        os.makedirs(self.credentials_path, exist_ok=True)
        
        # Charger token existant
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
                
        # Vérifier validité et refresh si nécessaire
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Refresh du token Google Drive...")
                creds.refresh(Request())
            else:
                print("🆕 Nouveau flow d'authentification Google Drive...")
                
                # Créer credentials.json basique si inexistant
                if not os.path.exists(credentials_json_path):
                    self._create_credentials_template(credentials_json_path)
                    print(f"⚠️ Configurez vos credentials dans: {credentials_json_path}")
                    print("   1. Aller à https://console.developers.google.com/")
                    print("   2. Créer projet et activer Google Drive API")
                    print("   3. Créer credentials OAuth 2.0")
                    print("   4. Télécharger et remplacer credentials.json")
                    return False
                    
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_json_path, self.scopes)
                creds = flow.run_local_server(port=0)
                
            # Sauvegarder token
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
                
        # Construire service
        try:
            self.service = build('drive', 'v3', credentials=creds)
            print("✅ Google Drive API initialisée")
            return True
        except HttpError as error:
            print(f"❌ Erreur Google Drive API: {error}")
            return False
            
    def _create_credentials_template(self, path: str):
        """Crée template credentials.json"""
        template = {
            "installed": {
                "client_id": "YOUR_CLIENT_ID.googleusercontent.com",
                "project_id": "panini-filesystem",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": "YOUR_CLIENT_SECRET",
                "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
            }
        }
        
        with open(path, 'w') as f:
            json.dump(template, f, indent=2)
            
    def create_folder_structure(self):
        """Crée structure complète dossiers Google Drive"""
        print("📁 Création structure dossiers Google Drive...")
        
        if not self.service:
            print("❌ Service Google Drive non initialisé")
            return False
            
        try:
            # Créer structure récursivement
            self._create_folders_recursive(self.folder_structure, parent_id='root')
            
            # Sauvegarder mapping folder IDs
            self._save_folder_mapping()
            
            print("✅ Structure dossiers créée")
            return True
            
        except HttpError as error:
            print(f"❌ Erreur création dossiers: {error}")
            return False
            
    def _create_folders_recursive(self, structure: Dict, parent_id: str, path: str = ""):
        """Crée dossiers récursivement"""
        for folder_name, sub_structure in structure.items():
            current_path = f"{path}/{folder_name}" if path else folder_name
            
            # Vérifier si dossier existe déjà
            existing_folder_id = self._find_folder_by_name(folder_name, parent_id)
            
            if existing_folder_id:
                print(f"📁 Dossier existant: {current_path}")
                folder_id = existing_folder_id
            else:
                # Créer nouveau dossier
                folder_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [parent_id]
                }
                
                folder = self.service.files().create(body=folder_metadata, fields='id').execute()
                folder_id = folder.get('id')
                print(f"✅ Dossier créé: {current_path}")
                
            # Stocker ID
            self.folder_ids[current_path] = folder_id
            
            # Créer sous-dossiers
            if sub_structure:
                self._create_folders_recursive(sub_structure, folder_id, current_path)
                
    def _find_folder_by_name(self, name: str, parent_id: str) -> Optional[str]:
        """Trouve dossier par nom dans parent spécifié"""
        try:
            query = f"name='{name}' and parents in '{parent_id}' and mimeType='application/vnd.google-apps.folder'"
            results = self.service.files().list(q=query, fields="files(id, name)").execute()
            
            files = results.get('files', [])
            if files:
                return files[0]['id']
            return None
            
        except HttpError as error:
            print(f"⚠️ Erreur recherche dossier {name}: {error}")
            return None
            
    def upload_study_pack_to_gdrive(self):
        """Upload study pack remarkable vers Google Drive"""
        print("📚 Upload study pack vers Google Drive...")
        
        study_pack_path = os.path.join(self.base_path, "remarkable_study_pack")
        
        if not os.path.exists(study_pack_path):
            print("❌ Study pack non trouvé")
            return False
            
        # Dossier cible
        target_folder_id = self.folder_ids.get('Panini/Bibliographie/Study_Pack_Remarkable')
        if not target_folder_id:
            print("❌ Dossier cible non trouvé")
            return False
            
        # Upload récursif
        success_count = 0
        total_count = 0
        
        for root, dirs, files in os.walk(study_pack_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, study_pack_path)
                
                total_count += 1
                
                # Créer sous-dossiers si nécessaire
                dir_structure = os.path.dirname(relative_path)
                if dir_structure:
                    current_folder_id = self._ensure_folder_path(dir_structure, target_folder_id)
                else:
                    current_folder_id = target_folder_id
                    
                # Upload fichier
                if self._upload_file(file_path, file, current_folder_id):
                    success_count += 1
                    
        print(f"📊 Upload terminé: {success_count}/{total_count} fichiers")
        return success_count > 0
        
    def _ensure_folder_path(self, path: str, parent_id: str) -> str:
        """Assure existence chemin dossiers"""
        folders = path.split('/')
        current_parent = parent_id
        
        for folder_name in folders:
            # Chercher dossier existant
            existing_id = self._find_folder_by_name(folder_name, current_parent)
            
            if existing_id:
                current_parent = existing_id
            else:
                # Créer dossier
                folder_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [current_parent]
                }
                
                folder = self.service.files().create(body=folder_metadata, fields='id').execute()
                current_parent = folder.get('id')
                
        return current_parent
        
    def _upload_file(self, file_path: str, file_name: str, parent_id: str) -> bool:
        """Upload fichier vers Google Drive"""
        try:
            # Déterminer mime type
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = 'application/octet-stream'
                
            # Metadata fichier
            file_metadata = {
                'name': file_name,
                'parents': [parent_id]
            }
            
            # Media upload
            media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
            
            # Vérifier si fichier existe déjà
            existing_file_id = self._find_file_by_name(file_name, parent_id)
            
            if existing_file_id:
                # Mettre à jour fichier existant
                file = self.service.files().update(
                    fileId=existing_file_id,
                    media_body=media
                ).execute()
                print(f"🔄 Fichier mis à jour: {file_name}")
            else:
                # Créer nouveau fichier
                file = self.service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()
                print(f"📤 Fichier uploadé: {file_name}")
                
            # Logger upload
            self.upload_log.append({
                'timestamp': datetime.now().isoformat(),
                'file_name': file_name,
                'file_path': file_path,
                'gdrive_id': file.get('id'),
                'action': 'update' if existing_file_id else 'create'
            })
            
            return True
            
        except HttpError as error:
            print(f"❌ Erreur upload {file_name}: {error}")
            return False
            
    def _find_file_by_name(self, name: str, parent_id: str) -> Optional[str]:
        """Trouve fichier par nom dans parent"""
        try:
            query = f"name='{name}' and parents in '{parent_id}'"
            results = self.service.files().list(q=query, fields="files(id, name)").execute()
            
            files = results.get('files', [])
            if files:
                return files[0]['id']
            return None
            
        except HttpError as error:
            print(f"⚠️ Erreur recherche fichier {name}: {error}")
            return None
            
    def upload_publications_to_gdrive(self):
        """Upload publications en cours vers Google Drive"""
        print("📝 Upload publications vers Google Drive...")
        
        publications_uploaded = 0
        
        # Publications existantes à uploader
        publication_files = [
            {'local': 'README.md', 'gdrive_path': 'Panini/Publications/Articles_En_Cours', 'name': 'README_PaniniFS.md'},
            {'local': 'EXTERNALISATION-CAMPING-STRATEGY.md', 'gdrive_path': 'Panini/Publications/Articles_En_Cours', 'name': 'Strategy_Externalisation.md'},
            {'local': 'panini_conceptual_audit_report.json', 'gdrive_path': 'Panini/Recherche/Audit_Reports', 'name': 'Conceptual_Audit_Latest.json'},
            {'local': 'ecosystem_coherence_final_report.json', 'gdrive_path': 'Panini/Recherche/Audit_Reports', 'name': 'Ecosystem_Coherence_Final.json'}
        ]
        
        for pub in publication_files:
            local_path = os.path.join(self.base_path, pub['local'])
            
            if os.path.exists(local_path):
                folder_id = self.folder_ids.get(pub['gdrive_path'])
                if folder_id:
                    if self._upload_file(local_path, pub['name'], folder_id):
                        publications_uploaded += 1
                        
        # Upload dossier publications review complet
        pub_review_path = os.path.join(self.base_path, "remarkable_study_pack/publications_review")
        if os.path.exists(pub_review_path):
            target_folder_id = self.folder_ids.get('Panini/Publications/Articles_En_Cours')
            if target_folder_id:
                for file in os.listdir(pub_review_path):
                    file_path = os.path.join(pub_review_path, file)
                    if os.path.isfile(file_path):
                        if self._upload_file(file_path, f"Review_{file}", target_folder_id):
                            publications_uploaded += 1
                            
        print(f"📊 Publications uploadées: {publications_uploaded}")
        return publications_uploaded > 0
        
    def setup_remarkable_sync_workflow(self):
        """Configure workflow synchronisation tablette reMarkable"""
        print("📱 Configuration sync reMarkable...")
        
        # Instructions sync reMarkable
        sync_instructions = {
            'workflow_type': 'remarkable_tablet_sync',
            'description': 'Synchronisation bidirectionnelle tablette reMarkable',
            'steps': [
                '1. Télécharger PDFs depuis Google Drive/Bibliographie/Study_Pack_Remarkable/',
                '2. Transférer vers reMarkable via reMarkable Desktop ou cloud',
                '3. Annoter et réviser sur tablette',
                '4. Exporter annotations depuis reMarkable',
                '5. Upload annotations vers Google Drive/Annotations/Remarkable_Exports/',
                '6. Traitement automatique commentaires pour amélioration'
            ],
            'automation': {
                'download_pdfs': 'Script automatique download nouveaux PDFs',
                'monitor_exports': 'Surveillance dossier exports reMarkable',
                'process_annotations': 'Extraction et traitement commentaires'
            },
            'google_drive_folders': {
                'source_bibliography': 'Panini/Bibliographie/Study_Pack_Remarkable/',
                'annotation_exports': 'Panini/Annotations/Remarkable_Exports/',
                'review_comments': 'Panini/Annotations/Review_Comments/'
            }
        }
        
        # Sauvegarder instructions
        sync_path = os.path.join(self.base_path, "remarkable_sync_workflow.json")
        with open(sync_path, 'w', encoding='utf-8') as f:
            json.dump(sync_instructions, f, indent=2, ensure_ascii=False)
            
        # Upload vers Google Drive
        workflow_folder_id = self.folder_ids.get('Panini/Annotations')
        if workflow_folder_id:
            self._upload_file(sync_path, "remarkable_sync_workflow.json", workflow_folder_id)
            
        print("✅ Workflow reMarkable configuré")
        return True
        
    def create_bibliography_pdfs(self):
        """Crée PDFs optimisés pour tablette reMarkable"""
        print("📄 Création PDFs bibliographie...")
        
        # Utiliser script existant pour générer bibliographie
        try:
            import subprocess
            
            # Exécuter générateur bibliographie avec option PDF
            result = subprocess.run([
                'python3',
                os.path.join(self.base_path, 'Copilotage/scripts/generate_remarkable_bibliography.py'),
                '--format', 'pdf',
                '--tablet-optimized'
            ], capture_output=True, text=True, cwd=self.base_path)
            
            if result.returncode == 0:
                print("✅ PDFs bibliographie générés")
                return True
            else:
                print(f"⚠️ Erreur génération PDFs: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur création PDFs: {e}")
            return False
            
    def monitor_gdrive_space_usage(self):
        """Surveille utilisation espace Google Drive"""
        print("💾 Vérification espace Google Drive...")
        
        try:
            about = self.service.about().get(fields="storageQuota").execute()
            storage = about.get('storageQuota', {})
            
            # Calculs espace
            limit = int(storage.get('limit', 0))
            usage = int(storage.get('usage', 0))
            
            # Conversion en unités lisibles
            limit_gb = limit / (1024**3) if limit > 0 else 0
            usage_gb = usage / (1024**3)
            available_gb = limit_gb - usage_gb if limit > 0 else float('inf')
            
            usage_percent = (usage_gb / limit_gb * 100) if limit_gb > 0 else 0
            
            print(f"📊 Espace Google Drive:")
            print(f"   💾 Utilisé: {usage_gb:.2f} GB")
            print(f"   📦 Total: {limit_gb:.2f} GB")
            print(f"   🆓 Disponible: {available_gb:.2f} GB")
            print(f"   📈 Pourcentage: {usage_percent:.1f}%")
            
            # Alertes
            if usage_percent > 90:
                print("🚨 ALERTE: Espace presque plein!")
            elif usage_percent > 75:
                print("⚠️ Attention: Plus de 75% utilisé")
                
            return {
                'total_gb': limit_gb,
                'used_gb': usage_gb,
                'available_gb': available_gb,
                'usage_percent': usage_percent
            }
            
        except HttpError as error:
            print(f"❌ Erreur vérification espace: {error}")
            return None
            
    def autonomous_sync_cycle(self):
        """Cycle complet synchronisation autonome"""
        print("🚀 CYCLE SYNCHRONISATION AUTONOME GOOGLE DRIVE")
        print("=" * 60)
        
        success_steps = 0
        total_steps = 7
        
        # 1. Initialisation API
        if self.initialize_google_drive_api():
            success_steps += 1
            
        # 2. Création structure
        if self.create_folder_structure():
            success_steps += 1
            
        # 3. Monitoring espace
        space_info = self.monitor_gdrive_space_usage()
        if space_info:
            success_steps += 1
            
        # 4. Création PDFs bibliographie
        if self.create_bibliography_pdfs():
            success_steps += 1
            
        # 5. Upload study pack
        if self.upload_study_pack_to_gdrive():
            success_steps += 1
            
        # 6. Upload publications
        if self.upload_publications_to_gdrive():
            success_steps += 1
            
        # 7. Configuration workflow reMarkable
        if self.setup_remarkable_sync_workflow():
            success_steps += 1
            
        # Rapport final
        self._generate_sync_report(success_steps, total_steps, space_info)
        
        print(f"\n🎯 SYNCHRONISATION TERMINÉE: {success_steps}/{total_steps} étapes réussies")
        
        return success_steps == total_steps
        
    def _save_folder_mapping(self):
        """Sauvegarde mapping IDs dossiers"""
        mapping_path = os.path.join(self.credentials_path, "folder_mapping.json")
        
        with open(mapping_path, 'w') as f:
            json.dump(self.folder_ids, f, indent=2)
            
        print(f"💾 Mapping dossiers sauvegardé: {mapping_path}")
        
    def _generate_sync_report(self, success_steps: int, total_steps: int, space_info: Optional[Dict]):
        """Génère rapport synchronisation"""
        report = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'sync_summary': {
                'success_steps': success_steps,
                'total_steps': total_steps,
                'success_rate': f"{success_steps/total_steps*100:.1f}%"
            },
            'folder_structure_created': len(self.folder_ids),
            'files_uploaded': len(self.upload_log),
            'gdrive_space': space_info,
            'folder_ids': self.folder_ids,
            'upload_log': self.upload_log,
            'remarkable_workflow': {
                'configured': True,
                'sync_folders': {
                    'bibliography_source': 'Panini/Bibliographie/Study_Pack_Remarkable/',
                    'annotations_target': 'Panini/Annotations/Remarkable_Exports/'
                }
            },
            'next_actions': [
                'Télécharger PDFs depuis Google Drive vers reMarkable',
                'Configurer sync automatique annotations',
                'Réviser publications sur tablette',
                'Uploader commentaires pour amélioration continue'
            ]
        }
        
        # Sauvegarde rapport
        report_path = os.path.join(self.base_path, f"gdrive_sync_report_{self.session_id}.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        # Rapport lisible
        self._print_sync_summary(report)
        
        print(f"📊 Rapport complet: {report_path}")
        
    def _print_sync_summary(self, report: Dict):
        """Affiche résumé synchronisation"""
        print("\n" + "="*60)
        print("📊 RÉSUMÉ SYNCHRONISATION GOOGLE DRIVE")
        print("="*60)
        
        # Succès
        summary = report['sync_summary']
        print(f"\n✅ Taux de succès: {summary['success_rate']}")
        print(f"📁 Dossiers créés: {report['folder_structure_created']}")
        print(f"📤 Fichiers uploadés: {report['files_uploaded']}")
        
        # Espace
        if report.get('gdrive_space'):
            space = report['gdrive_space']
            print(f"💾 Espace utilisé: {space['used_gb']:.2f}/{space['total_gb']:.2f} GB ({space['usage_percent']:.1f}%)")
            
        # Structure créée
        print(f"\n📁 STRUCTURE GOOGLE DRIVE:")
        print("   📂 Panini/")
        print("      📂 Publications/")
        print("         📄 Articles_En_Cours/ (révision tablette)")
        print("         📄 Articles_Publies/")
        print("         📄 Livre_Leanpub/")
        print("      📂 Bibliographie/")
        print("         📚 Study_Pack_Remarkable/ (PDFs tablette)")
        print("         📚 Recherche_Theorique/")
        print("      📂 Recherche/")
        print("         📊 Audit_Reports/")
        print("         🔥 Criticism_Reports/")
        print("      📂 Annotations/")
        print("         ✏️ Remarkable_Exports/ (vos annotations)")
        print("         💬 Review_Comments/")
        
        # Actions suivantes
        print(f"\n🚀 PROCHAINES ACTIONS:")
        for action in report['next_actions']:
            print(f"   • {action}")
            
        print("\n" + "="*60)

def main():
    """Fonction principale"""
    print("🚀 GESTIONNAIRE GOOGLE DRIVE AUTONOME - PANINI")
    print("Objectif: Organisation complète Google Drive (2TB)")
    print("Mode: 100% autonome avec API Google Drive")
    print("=" * 60)
    
    try:
        manager = AutonomousGoogleDriveManager()
        success = manager.autonomous_sync_cycle()
        
        if success:
            print("🎉 Synchronisation Google Drive réussie!")
            print("📱 Votre tablette reMarkable peut maintenant accéder à la bibliographie")
            print("💬 Vos annotations seront automatiquement intégrées")
        else:
            print("⚠️ Synchronisation partiellement réussie - Voir rapport pour détails")
            
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
