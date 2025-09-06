#!/usr/bin/env python3
"""
Script d'analyse des préférences de développement
Analyse le dossier ~/Copilotage pour extraire les préférences et patterns de développement
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

# Utiliser tomllib si disponible (Python 3.11+), sinon parser TOML manuellement
try:
    import tomllib
    TOML_AVAILABLE = True
except ImportError:
    TOML_AVAILABLE = False

@dataclass
class ProjectPreferences:
    """Structure pour stocker les préférences d'un projet"""
    name: str
    languages: List[str]
    frameworks: List[str]
    build_tools: List[str]
    test_frameworks: List[str]
    architecture_patterns: List[str]
    coding_style: Dict[str, Any]
    dependencies: List[str]
    documentation_style: str

class PreferencesAnalyzer:
    def __init__(self, copilotage_path: str = "~/Copilotage"):
        # Utiliser le répertoire Copilotage dans le projet actuel si ~/Copilotage n'existe pas
        copilotage_expanded = Path(copilotage_path).expanduser()
        if not copilotage_expanded.exists():
            # Essayer le répertoire Copilotage du projet
            project_copilotage = Path(__file__).parent.parent
            if project_copilotage.name == "Copilotage":
                copilotage_expanded = project_copilotage
            else:
                # Fallback sur le répertoire du script
                copilotage_expanded = Path(__file__).parent.parent / "Copilotage"
        
        self.copilotage_path = copilotage_expanded
        self.preferences = {}
        self.global_patterns = {
            'languages': {},
            'frameworks': {},
            'architecture_patterns': {},
            'coding_conventions': {}
        }
    
    def analyze_markdown_files(self):
        """Analyse les fichiers markdown pour extraire les préférences"""
        md_files = list(self.copilotage_path.rglob("*.md"))
        
        for md_file in md_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                project_name = md_file.stem
                preferences = self._extract_preferences_from_md(content, project_name)
                
                if preferences:
                    self.preferences[project_name] = preferences
                    
            except Exception as e:
                print(f"Erreur lors de l'analyse de {md_file}: {e}")
    
    def _extract_preferences_from_md(self, content: str, project_name: str) -> ProjectPreferences:
        """Extrait les préférences d'un fichier markdown"""
        
        # Détection des langages
        languages = []
        lang_patterns = {
            'rust': r'(?i)\b(rust|cargo|\.rs)\b',
            'python': r'(?i)\b(python|pip|\.py|django|flask)\b',
            'javascript': r'(?i)\b(javascript|npm|node|\.js|react|vue)\b',
            'typescript': r'(?i)\b(typescript|\.ts|angular)\b',
            'c++': r'(?i)\b(c\+\+|cpp|\.cpp|\.hpp)\b',
            'c#': r'(?i)\b(c#|\.cs|\.net|dotnet)\b',
            'java': r'(?i)\b(java|\.java|maven|gradle)\b',
            'go': r'(?i)\b(golang|go|\.go)\b'
        }
        
        for lang, pattern in lang_patterns.items():
            if re.search(pattern, content):
                languages.append(lang)
        
        # Détection des frameworks
        frameworks = []
        framework_patterns = {
            'tokio': r'(?i)\btokio\b',
            'actix': r'(?i)\bactix\b',
            'axum': r'(?i)\baxum\b',
            'django': r'(?i)\bdjango\b',
            'flask': r'(?i)\bflask\b',
            'react': r'(?i)\breact\b',
            'vue': r'(?i)\bvue\b',
            'angular': r'(?i)\bangular\b',
            'express': r'(?i)\bexpress\b'
        }
        
        for framework, pattern in framework_patterns.items():
            if re.search(pattern, content):
                frameworks.append(framework)
        
        # Détection des outils de build
        build_tools = []
        build_patterns = {
            'cargo': r'(?i)\bcargo\b',
            'npm': r'(?i)\bnpm\b',
            'yarn': r'(?i)\byarn\b',
            'webpack': r'(?i)\bwebpack\b',
            'vite': r'(?i)\bvite\b',
            'cmake': r'(?i)\bcmake\b',
            'make': r'(?i)\bmake\b',
            'msbuild': r'(?i)\bmsbuild\b'
        }
        
        for tool, pattern in build_patterns.items():
            if re.search(pattern, content):
                build_tools.append(tool)
        
        # Détection des patterns d'architecture
        arch_patterns = []
        arch_pattern_map = {
            'microservices': r'(?i)\b(microservices?|micro-services?)\b',
            'monolith': r'(?i)\bmonolith\b',
            'mvc': r'(?i)\bmvc\b',
            'mvvm': r'(?i)\bmvvm\b',
            'clean_architecture': r'(?i)\b(clean architecture|hexagonal)\b',
            'domain_driven': r'(?i)\b(ddd|domain.driven)\b',
            'event_sourcing': r'(?i)\bevent.sourcing\b',
            'cqrs': r'(?i)\bcqrs\b'
        }
        
        for pattern_name, regex in arch_pattern_map.items():
            if re.search(regex, content):
                arch_patterns.append(pattern_name)
        
        # Détection du style de documentation
        doc_style = "markdown"  # Par défaut
        if re.search(r'(?i)\bsphinx\b', content):
            doc_style = "sphinx"
        elif re.search(r'(?i)\bdoxygen\b', content):
            doc_style = "doxygen"
        elif re.search(r'(?i)\bjsdoc\b', content):
            doc_style = "jsdoc"
        
        return ProjectPreferences(
            name=project_name,
            languages=languages,
            frameworks=frameworks,
            build_tools=build_tools,
            test_frameworks=[],  # À enrichir
            architecture_patterns=arch_patterns,
            coding_style={},  # À enrichir
            dependencies=[],  # À enrichir
            documentation_style=doc_style
        )
    
    def analyze_config_files(self):
        """Analyse les fichiers de configuration pour extraire plus d'informations"""
        config_files = [
            "*.toml", "*.json", "*.yaml", "*.yml", 
            "*.ini", "*.conf", "Cargo.toml", "package.json",
            "requirements.txt", "Pipfile", "pyproject.toml"
        ]
        
        for pattern in config_files:
            for config_file in self.copilotage_path.rglob(pattern):
                try:
                    self._analyze_config_file(config_file)
                except Exception as e:
                    print(f"Erreur lors de l'analyse de {config_file}: {e}")
    
    def _analyze_config_file(self, config_file: Path):
        """Analyse un fichier de configuration spécifique"""
        if config_file.name == "Cargo.toml":
            self._analyze_cargo_toml(config_file)
        elif config_file.name == "package.json":
            self._analyze_package_json(config_file)
        # Ajouter d'autres types de fichiers selon les besoins
    
    def _analyze_cargo_toml(self, cargo_file: Path):
        """Analyse un fichier Cargo.toml"""
        try:
            if TOML_AVAILABLE:
                with open(cargo_file, 'rb') as f:
                    cargo_data = tomllib.load(f)  # type: ignore
            else:
                # Parser TOML basique pour les cas simples
                cargo_data = self._parse_simple_toml(cargo_file)
            
            project_name = cargo_data.get('package', {}).get('name', cargo_file.parent.name)
            
            if project_name in self.preferences:
                # Enrichir les dépendances
                deps = list(cargo_data.get('dependencies', {}).keys())
                self.preferences[project_name].dependencies.extend(deps)
                
                # Analyser les features pour détecter les patterns
                dev_deps = list(cargo_data.get('dev-dependencies', {}).keys())
                if 'tokio-test' in dev_deps or 'tokio' in deps:
                    if 'async' not in self.preferences[project_name].architecture_patterns:
                        self.preferences[project_name].architecture_patterns.append('async')
                        
        except Exception as e:
            print(f"Erreur lors de l'analyse de {cargo_file}: {e}")
    
    def _parse_simple_toml(self, toml_file: Path) -> Dict[str, Any]:
        """Parser TOML basique pour les cas simples"""
        result = {'package': {}, 'dependencies': {}, 'dev-dependencies': {}}
        current_section = None
        
        try:
            with open(toml_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    # Sections
                    if line.startswith('[') and line.endswith(']'):
                        current_section = line[1:-1]
                        if current_section not in result:
                            result[current_section] = {}
                        continue
                    
                    # Clé-valeur
                    if '=' in line and current_section:
                        key, value = line.split('=', 1)
                        key = key.strip().strip('"')
                        value = value.strip().strip('"').strip("'")
                        
                        if current_section in result:
                            result[current_section][key] = value
        except Exception as e:
            print(f"Erreur lors du parsing de {toml_file}: {e}")
        
        return result
    
    def _analyze_package_json(self, package_file: Path):
        """Analyse un fichier package.json"""
        try:
            with open(package_file, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
            
            project_name = package_data.get('name', package_file.parent.name)
            
            if project_name in self.preferences:
                # Enrichir les dépendances
                deps = list(package_data.get('dependencies', {}).keys())
                dev_deps = list(package_data.get('devDependencies', {}).keys())
                
                self.preferences[project_name].dependencies.extend(deps + dev_deps)
                
        except Exception as e:
            print(f"Erreur lors de l'analyse de {package_file}: {e}")
    
    def compute_global_patterns(self):
        """Calcule les patterns globaux à partir de tous les projets"""
        for project, prefs in self.preferences.items():
            # Compter les langages
            for lang in prefs.languages:
                self.global_patterns['languages'][lang] = self.global_patterns['languages'].get(lang, 0) + 1
            
            # Compter les frameworks
            for framework in prefs.frameworks:
                self.global_patterns['frameworks'][framework] = self.global_patterns['frameworks'].get(framework, 0) + 1
            
            # Compter les patterns d'architecture
            for pattern in prefs.architecture_patterns:
                self.global_patterns['architecture_patterns'][pattern] = self.global_patterns['architecture_patterns'].get(pattern, 0) + 1
    
    def generate_report(self) -> Dict[str, Any]:
        """Génère un rapport complet des préférences"""
        return {
            'projects': {name: asdict(prefs) for name, prefs in self.preferences.items()},
            'global_patterns': self.global_patterns,
            'summary': {
                'total_projects': len(self.preferences),
                'most_used_language': max(self.global_patterns['languages'].items(), key=lambda x: x[1])[0] if self.global_patterns['languages'] else None,
                'most_used_framework': max(self.global_patterns['frameworks'].items(), key=lambda x: x[1])[0] if self.global_patterns['frameworks'] else None,
                'preferred_architecture': max(self.global_patterns['architecture_patterns'].items(), key=lambda x: x[1])[0] if self.global_patterns['architecture_patterns'] else None
            }
        }
    
    def save_report(self, output_file: str = "preferences_report.json"):
        """Sauvegarde le rapport dans un fichier"""
        report = self.generate_report()
        
        # Utiliser le répertoire scripts pour sauvegarder
        scripts_dir = Path(__file__).parent
        output_path = scripts_dir / output_file
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"Rapport sauvegardé dans {output_path}")
        return output_path

def main():
    """Fonction principale"""
    analyzer = PreferencesAnalyzer()
    
    print("Analyse des préférences de développement...")
    print(f"Analyse du dossier: {analyzer.copilotage_path}")
    
    # Analyser les fichiers
    analyzer.analyze_markdown_files()
    analyzer.analyze_config_files()
    analyzer.compute_global_patterns()
    
    # Générer et sauvegarder le rapport
    report_path = analyzer.save_report()
    
    # Afficher un résumé
    report = analyzer.generate_report()
    summary = report['summary']
    
    print("\n=== RÉSUMÉ DES PRÉFÉRENCES ===")
    print(f"Nombre de projets analysés: {summary['total_projects']}")
    print(f"Langage le plus utilisé: {summary['most_used_language']}")
    print(f"Framework le plus utilisé: {summary['most_used_framework']}")
    print(f"Architecture préférée: {summary['preferred_architecture']}")
    
    print(f"\nRapport détaillé disponible dans: {report_path}")

if __name__ == "__main__":
    main()
