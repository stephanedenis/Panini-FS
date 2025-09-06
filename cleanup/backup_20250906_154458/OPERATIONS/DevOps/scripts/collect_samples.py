#!/usr/bin/env python3
"""
Script de collecte d'échantillons de fichiers
Explore ~/GitHub/Pensine pour collecter des échantillons de différents types de fichiers
à utiliser comme données de test pour PaniniFS
"""

import os
import json
import hashlib
import mimetypes
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
import subprocess

@dataclass
class FileInfo:
    """Informations sur un fichier échantillon"""
    path: str
    relative_path: str
    size: int
    mime_type: str
    extension: str
    encoding: Optional[str]
    hash_md5: str
    hash_sha256: str
    git_info: Optional[Dict[str, Any]]
    semantic_info: Dict[str, Any]

@dataclass
class DirectoryInfo:
    """Informations sur un répertoire"""
    path: str
    relative_path: str
    file_count: int
    total_size: int
    subdirectory_count: int
    file_types: Dict[str, int]

class SampleCollector:
    def __init__(self, pensine_path: str = "~/GitHub/Pensine"):
        self.pensine_path = Path(pensine_path).expanduser()
        self.samples = []
        self.directories = []
        self.file_type_stats = defaultdict(int)
        self.size_stats = {
            'total_files': 0,
            'total_size': 0,
            'by_extension': defaultdict(lambda: {'count': 0, 'total_size': 0})
        }
        
        # Types de fichiers intéressants pour les tests
        self.interesting_types = {
            # Code source
            '.py', '.rs', '.js', '.ts', '.cpp', '.c', '.h', '.hpp', '.java', '.go', '.rb',
            '.php', '.cs', '.kt', '.swift', '.scala', '.clj', '.hs', '.ml', '.fs',
            
            # Configuration et données
            '.json', '.yaml', '.yml', '.toml', '.ini', '.conf', '.cfg', '.xml',
            '.csv', '.tsv', '.sql', '.db', '.sqlite',
            
            # Documentation
            '.md', '.rst', '.txt', '.adoc', '.tex', '.org',
            
            # Web
            '.html', '.css', '.scss', '.sass', '.less', '.vue', '.jsx', '.tsx',
            
            # Images et médias
            '.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico',
            '.mp3', '.wav', '.ogg', '.mp4', '.avi', '.mkv',
            
            # Archives et binaires
            '.zip', '.tar', '.gz', '.7z', '.rar', '.exe', '.dll', '.so', '.dylib',
            
            # Autres
            '.log', '.bak', '.tmp', '.lock', '.pid'
        }
    
    def collect_samples(self, max_files_per_type: int = 10, max_file_size: int = 10 * 1024 * 1024):
        """Collecte les échantillons de fichiers"""
        print(f"Collecte des échantillons dans: {self.pensine_path}")
        
        if not self.pensine_path.exists():
            print(f"Erreur: Le dossier {self.pensine_path} n'existe pas")
            return
        
        type_counts = defaultdict(int)
        
        for root, dirs, files in os.walk(self.pensine_path):
            root_path = Path(root)
            
            # Analyser le répertoire
            self._analyze_directory(root_path, dirs, files)
            
            # Analyser les fichiers
            for file in files:
                file_path = root_path / file
                
                # Ignorer les fichiers trop volumineux
                try:
                    if file_path.stat().st_size > max_file_size:
                        continue
                except (OSError, IOError):
                    continue
                
                # Obtenir l'extension
                extension = file_path.suffix.lower()
                
                # Limiter le nombre d'échantillons par type
                if type_counts[extension] >= max_files_per_type:
                    continue
                
                # Analyser le fichier si intéressant
                if extension in self.interesting_types or self._is_interesting_file(file_path):
                    file_info = self._analyze_file(file_path)
                    if file_info:
                        self.samples.append(file_info)
                        type_counts[extension] += 1
                        self.file_type_stats[extension] += 1
                        
                        # Mettre à jour les statistiques
                        self.size_stats['total_files'] += 1
                        self.size_stats['total_size'] += file_info.size
                        self.size_stats['by_extension'][extension]['count'] += 1
                        self.size_stats['by_extension'][extension]['total_size'] += file_info.size
    
    def _analyze_directory(self, dir_path: Path, subdirs: List[str], files: List[str]):
        """Analyse un répertoire"""
        try:
            total_size = 0
            file_types = defaultdict(int)
            
            for file in files:
                file_path = dir_path / file
                try:
                    size = file_path.stat().st_size
                    total_size += size
                    extension = file_path.suffix.lower()
                    file_types[extension] += 1
                except (OSError, IOError):
                    continue
            
            relative_path = str(dir_path.relative_to(self.pensine_path))
            
            dir_info = DirectoryInfo(
                path=str(dir_path),
                relative_path=relative_path,
                file_count=len(files),
                total_size=total_size,
                subdirectory_count=len(subdirs),
                file_types=dict(file_types)
            )
            
            self.directories.append(dir_info)
            
        except Exception as e:
            print(f"Erreur lors de l'analyse du répertoire {dir_path}: {e}")
    
    def _analyze_file(self, file_path: Path) -> Optional[FileInfo]:
        """Analyse un fichier spécifique"""
        try:
            # Informations de base
            stat = file_path.stat()
            size = stat.st_size
            extension = file_path.suffix.lower()
            relative_path = str(file_path.relative_to(self.pensine_path))
            
            # Type MIME
            mime_type, encoding = mimetypes.guess_type(str(file_path))
            if not mime_type:
                mime_type = 'application/octet-stream'
            
            # Hash du fichier
            md5_hash, sha256_hash = self._compute_hashes(file_path)
            
            # Informations Git
            git_info = self._get_git_info(file_path)
            
            # Informations sémantiques
            semantic_info = self._extract_semantic_info(file_path, mime_type)
            
            return FileInfo(
                path=str(file_path),
                relative_path=relative_path,
                size=size,
                mime_type=mime_type,
                extension=extension,
                encoding=encoding,
                hash_md5=md5_hash,
                hash_sha256=sha256_hash,
                git_info=git_info,
                semantic_info=semantic_info
            )
            
        except Exception as e:
            print(f"Erreur lors de l'analyse de {file_path}: {e}")
            return None
    
    def _compute_hashes(self, file_path: Path) -> tuple[str, str]:
        """Calcule les hash MD5 et SHA256 d'un fichier"""
        md5_hasher = hashlib.md5()
        sha256_hasher = hashlib.sha256()
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    md5_hasher.update(chunk)
                    sha256_hasher.update(chunk)
        except (OSError, IOError):
            return "error", "error"
        
        return md5_hasher.hexdigest(), sha256_hasher.hexdigest()
    
    def _get_git_info(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Récupère les informations Git pour un fichier"""
        try:
            # Trouver le repository Git le plus proche
            git_dir = file_path.parent
            while git_dir != git_dir.parent:
                if (git_dir / '.git').exists():
                    break
                git_dir = git_dir.parent
            else:
                return None
            
            # Obtenir les informations Git
            relative_to_git = file_path.relative_to(git_dir)
            
            # Dernière modification
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%H|%an|%ae|%ad|%s', '--', str(relative_to_git)],
                cwd=git_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout.strip():
                parts = result.stdout.strip().split('|', 4)
                if len(parts) >= 5:
                    return {
                        'repository': str(git_dir),
                        'last_commit_hash': parts[0],
                        'last_author_name': parts[1],
                        'last_author_email': parts[2],
                        'last_commit_date': parts[3],
                        'last_commit_message': parts[4],
                        'relative_path': str(relative_to_git)
                    }
            
            return None
            
        except Exception:
            return None
    
    def _extract_semantic_info(self, file_path: Path, mime_type: str) -> Dict[str, Any]:
        """Extrait des informations sémantiques d'un fichier"""
        info = {
            'is_text': mime_type.startswith('text/'),
            'is_code': False,
            'is_config': False,
            'is_documentation': False,
            'language': None,
            'line_count': 0,
            'word_count': 0,
            'char_count': 0
        }
        
        # Détection du type de fichier
        extension = file_path.suffix.lower()
        
        # Code source
        code_extensions = {
            '.py': 'python', '.rs': 'rust', '.js': 'javascript', '.ts': 'typescript',
            '.cpp': 'cpp', '.c': 'c', '.h': 'c', '.hpp': 'cpp',
            '.java': 'java', '.go': 'go', '.rb': 'ruby', '.php': 'php',
            '.cs': 'csharp', '.kt': 'kotlin', '.swift': 'swift',
            '.scala': 'scala', '.clj': 'clojure', '.hs': 'haskell'
        }
        
        if extension in code_extensions:
            info['is_code'] = True
            info['language'] = code_extensions[extension]
        
        # Configuration
        config_extensions = {'.json', '.yaml', '.yml', '.toml', '.ini', '.conf', '.cfg', '.xml'}
        if extension in config_extensions:
            info['is_config'] = True
        
        # Documentation
        doc_extensions = {'.md', '.rst', '.txt', '.adoc', '.tex', '.org'}
        if extension in doc_extensions:
            info['is_documentation'] = True
        
        # Analyser le contenu si c'est un fichier texte
        if info['is_text'] and file_path.stat().st_size < 1024 * 1024:  # Limite à 1MB
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    words = content.split()
                    
                    info['line_count'] = len(lines)
                    info['word_count'] = len(words)
                    info['char_count'] = len(content)
                    
                    # Détection de langue de programmation par contenu
                    if not info['language'] and info['is_code']:
                        info['language'] = self._detect_language_by_content(content)
                        
            except (UnicodeDecodeError, OSError):
                pass
        
        return info
    
    def _detect_language_by_content(self, content: str) -> Optional[str]:
        """Détecte le langage de programmation par le contenu"""
        content_lower = content.lower()
        
        # Patterns simples de détection
        if 'fn main()' in content or 'use std::' in content:
            return 'rust'
        elif 'def ' in content and 'import ' in content:
            return 'python'
        elif 'function ' in content and ('var ' in content or 'let ' in content):
            return 'javascript'
        elif 'public class ' in content and 'public static void main' in content:
            return 'java'
        elif '#include ' in content and ('int main(' in content or 'void main(' in content):
            return 'c'
        
        return None
    
    def _is_interesting_file(self, file_path: Path) -> bool:
        """Détermine si un fichier est intéressant à analyser"""
        # Fichiers spéciaux
        special_names = {
            'readme', 'license', 'changelog', 'dockerfile', 'makefile',
            'cargo.toml', 'package.json', 'requirements.txt', 'setup.py',
            '.gitignore', '.gitattributes', '.editorconfig'
        }
        
        name_lower = file_path.name.lower()
        return name_lower in special_names or file_path.stem.lower() in special_names
    
    def generate_test_scenarios(self) -> List[Dict[str, Any]]:
        """Génère des scénarios de test basés sur les échantillons"""
        scenarios = []
        
        # Scénario: Fichiers de différentes tailles
        size_categories = {
            'tiny': (0, 1024),           # < 1KB
            'small': (1024, 10240),      # 1-10KB
            'medium': (10240, 102400),   # 10-100KB
            'large': (102400, 1048576),  # 100KB-1MB
            'xlarge': (1048576, float('inf'))  # > 1MB
        }
        
        for category, (min_size, max_size) in size_categories.items():
            files = [f for f in self.samples if min_size <= f.size < max_size]
            if files:
                scenarios.append({
                    'name': f'test_files_{category}',
                    'description': f'Test avec des fichiers {category} ({min_size}-{max_size} bytes)',
                    'files': [f.relative_path for f in files[:5]],  # Max 5 exemples
                    'count': len(files)
                })
        
        # Scénario: Par type de fichier
        by_extension = defaultdict(list)
        for sample in self.samples:
            by_extension[sample.extension].append(sample)
        
        for ext, files in by_extension.items():
            if len(files) >= 2:  # Au moins 2 fichiers du même type
                scenarios.append({
                    'name': f'test_files{ext}',
                    'description': f'Test avec des fichiers {ext}',
                    'files': [f.relative_path for f in files[:3]],
                    'count': len(files)
                })
        
        # Scénario: Fichiers avec historique Git
        git_files = [f for f in self.samples if f.git_info]
        if git_files:
            scenarios.append({
                'name': 'test_files_with_git_history',
                'description': 'Test avec des fichiers ayant un historique Git',
                'files': [f.relative_path for f in git_files[:10]],
                'count': len(git_files)
            })
        
        return scenarios
    
    def generate_report(self) -> Dict[str, Any]:
        """Génère un rapport complet de la collecte"""
        scenarios = self.generate_test_scenarios()
        
        return {
            'collection_info': {
                'source_path': str(self.pensine_path),
                'total_files_analyzed': len(self.samples),
                'total_directories_analyzed': len(self.directories),
                'collection_date': str(Path().cwd())  # Placeholder
            },
            'statistics': {
                'file_types': dict(self.file_type_stats),
                'size_distribution': dict(self.size_stats['by_extension']),
                'total_size': self.size_stats['total_size'],
                'average_file_size': self.size_stats['total_size'] / max(1, self.size_stats['total_files'])
            },
            'samples': [asdict(sample) for sample in self.samples],
            'directories': [asdict(directory) for directory in self.directories],
            'test_scenarios': scenarios,
            'recommended_test_files': {
                'small_diverse_set': [f.relative_path for f in self.samples[:20]],
                'code_files_only': [f.relative_path for f in self.samples if f.semantic_info.get('is_code', False)][:10],
                'config_files_only': [f.relative_path for f in self.samples if f.semantic_info.get('is_config', False)][:5],
                'documentation_files': [f.relative_path for f in self.samples if f.semantic_info.get('is_documentation', False)][:5]
            }
        }
    
    def save_report(self, output_file: str = "sample_collection_report.json"):
        """Sauvegarde le rapport dans un fichier"""
        report = self.generate_report()
        
        scripts_dir = Path("/home/stephane/GitHub/PaniniFS-1/scripts/scripts")
        scripts_dir.mkdir(exist_ok=True)
        output_path = scripts_dir / output_file
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"Rapport de collecte sauvegardé dans {output_path}")
        return output_path

def main():
    """Fonction principale"""
    collector = SampleCollector()
    
    print("Collecte d'échantillons de fichiers pour tests...")
    print(f"Analyse du dossier: {collector.pensine_path}")
    
    if not collector.pensine_path.exists():
        print(f"Erreur: Le dossier {collector.pensine_path} n'existe pas")
        print("Création d'un rapport vide pour démonstration...")
        collector.save_report()
        return
    
    # Collecter les échantillons
    collector.collect_samples()
    
    # Générer et sauvegarder le rapport
    report_path = collector.save_report()
    
    # Afficher un résumé
    print(f"\n=== RÉSUMÉ DE LA COLLECTE ===")
    print(f"Fichiers analysés: {len(collector.samples)}")
    print(f"Répertoires analysés: {len(collector.directories)}")
    print(f"Types de fichiers trouvés: {len(collector.file_type_stats)}")
    
    # Top 5 des types de fichiers
    top_types = sorted(collector.file_type_stats.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f"\nTop 5 des types de fichiers:")
    for ext, count in top_types:
        print(f"  {ext or '(sans extension)'}: {count} fichiers")
    
    print(f"\nRapport détaillé disponible dans: {report_path}")

if __name__ == "__main__":
    main()
