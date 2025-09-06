#!/usr/bin/env python3

# 🚀 Debug Ultra-Rapide PaniniFS
# Version minimale pour identifier l'erreur rapidement

import sys
import time
import os
from pathlib import Path

print("🚀 DEBUG ULTRA-RAPIDE PANINIFS")
print("=" * 40)

def test_basic_imports():
    """Test des imports de base"""
    print("📦 Test imports de base...")
    
    try:
        import torch
        print(f"✅ torch: {torch.__version__}")
        gpu_available = torch.cuda.is_available()
        print(f"   GPU: {'✅' if gpu_available else '❌'}")
    except ImportError as e:
        print(f"❌ torch: {e}")
    
    try:
        import numpy as np
        print(f"✅ numpy: {np.__version__}")
    except ImportError as e:
        print(f"❌ numpy: {e}")
    
    try:
        from sentence_transformers import SentenceTransformer
        print("✅ sentence-transformers disponible")
    except ImportError as e:
        print(f"⚠️ sentence-transformers: {e}")
        print("   Installation: pip install sentence-transformers")

def test_local_paths():
    """Test d'accès aux chemins locaux"""
    print("\n📁 Test chemins locaux...")
    
    paths_to_test = [
        '/home/stephane/GitHub/PaniniFS-1',
        '/home/stephane/GitHub/Pensine',
        '/home/stephane/GitHub',
        os.getcwd()
    ]
    
    for path_str in paths_to_test:
        path = Path(path_str)
        if path.exists():
            file_count = len(list(path.glob("*.py")))
            print(f"✅ {path_str}: {file_count} fichiers Python")
        else:
            print(f"❌ {path_str}: non trouvé")

def test_quick_processing():
    """Test rapide de processing"""
    print("\n⚡ Test processing rapide...")
    
    # Données de test minimales
    test_docs = [
        "Python programming test",
        "Rust systems programming", 
        "JavaScript web development"
    ]
    
    try:
        from sentence_transformers import SentenceTransformer
        
        print("🔄 Chargement modèle...")
        model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
        
        print("⚡ Création embeddings...")
        start = time.time()
        embeddings = model.encode(test_docs, show_progress_bar=False)
        duration = time.time() - start
        
        print(f"✅ Embeddings créés en {duration:.2f}s")
        print(f"   Forme: {embeddings.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur processing: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Test complet ultra-rapide"""
    
    start_total = time.time()
    
    # Tests séquentiels
    test_basic_imports()
    test_local_paths()
    processing_ok = test_quick_processing()
    
    total_time = time.time() - start_total
    
    print(f"\n📊 RÉSUMÉ DEBUG:")
    print(f"   ⏱️ Temps total: {total_time:.2f}s")
    print(f"   ⚡ Processing: {'✅ OK' if processing_ok else '❌ Erreur'}")
    
    if processing_ok:
        print(f"\n✅ DIAGNOSTIC: Environment OK!")
        print(f"   💡 L'erreur est probablement dans Colab")
        print(f"   🎯 Vérifiez: GPU activation, network, timeouts")
    else:
        print(f"\n❌ DIAGNOSTIC: Problème local détecté")
        print(f"   💡 Installez les dépendances manquantes")
        print(f"   🔧 pip install sentence-transformers torch")

if __name__ == "__main__":
    main()
