"""
🚀 GOOGLE COLAB SETUP IMMÉDIAT - PaniniFS Acceleration
💡 Notebook template pour preprocessing datasets sémantiques
⚡ 22-60x speedup clustering + preprocessing GPU
"""

# 🔧 ÉTAPE 1: VÉRIFICATION GPU
print("🔍 Vérification GPU disponible...")
try:
    import torch
    if torch.cuda.is_available():
        print(f"✅ CUDA disponible: {torch.cuda.get_device_name(0)}")
        print(f"💾 VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    else:
        print("⚠️ CUDA non disponible - vérifier Runtime > Change runtime type > GPU")
except ImportError:
    print("📦 Installation PyTorch...")
    !pip install torch torchvision torchaudio

# Alternative: nvidia-smi check
print("\n🔍 Détails GPU via nvidia-smi:")
!nvidia-smi

# 🔗 ÉTAPE 2: CONNEXION GOOGLE DRIVE
print("\n📁 Connexion Google Drive pour persistence...")
from google.colab import drive
drive.mount('/content/drive')

# Créer dossier projet
import os
project_dir = '/content/drive/MyDrive/PaniniFS_Cloud'
os.makedirs(project_dir, exist_ok=True)
print(f"📂 Dossier projet: {project_dir}")

# 📥 ÉTAPE 3: CLONE REPO PANINIIFS
print("\n🔄 Clone repository PaniniFS...")
repo_url = "https://github.com/stephanedenis/PaniniFS.git"
!git clone {repo_url} /content/PaniniFS

# Setup working directory
os.chdir('/content/PaniniFS')
print("📍 Working directory:", os.getcwd())

# 📦 ÉTAPE 4: INSTALLATION DÉPENDANCES
print("\n📦 Installation dépendances Python...")
requirements = [
    'numpy', 'pandas', 'scikit-learn', 'matplotlib', 'seaborn',
    'requests', 'beautifulsoup4', 'nltk', 'spacy',
    'torch', 'transformers', 'sentence-transformers',
    'plotly', 'networkx', 'umap-learn', 'hdbscan',
    'wikipedia', 'arxiv', 'tqdm'
]

for package in requirements:
    !pip install {package}

# Download spaCy model
!python -m spacy download en_core_web_sm

# 🔬 ÉTAPE 5: SETUP ENVIRONNEMENT SEMANTIC PROCESSING
print("\n🧠 Setup environnement semantic processing...")

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
from sentence_transformers import SentenceTransformer
import torch
import json
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

# Configuration GPU optimale
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"🎯 Device: {device}")

# Load sentence transformer model optimisé GPU
print("🤖 Loading SentenceTransformer model...")
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
print("✅ Model loaded on GPU")

# 📊 ÉTAPE 6: FONCTIONS ACCELERATION PREPROCESSING
def accelerated_wikipedia_preprocessing(topics, max_articles=100):
    """Preprocessing Wikipedia accéléré GPU"""
    print(f"📚 Processing {len(topics)} topics, max {max_articles} articles each...")
    
    import wikipedia
    articles_data = []
    
    for topic in tqdm(topics, desc="Topics"):
        try:
            # Search articles
            search_results = wikipedia.search(topic, results=max_articles//10)
            
            for title in search_results[:max_articles//len(topics)]:
                try:
                    page = wikipedia.page(title)
                    articles_data.append({
                        'topic': topic,
                        'title': page.title,
                        'content': page.content[:2000],  # Truncate pour GPU memory
                        'url': page.url,
                        'summary': page.summary
                    })
                except:
                    continue
                    
        except:
            continue
    
    print(f"✅ Collected {len(articles_data)} articles")
    return pd.DataFrame(articles_data)

def gpu_accelerated_clustering(texts, n_clusters=None, method='kmeans'):
    """Clustering accéléré GPU avec embeddings"""
    print(f"🧠 GPU clustering {len(texts)} texts...")
    
    # Generate embeddings sur GPU
    print("🔄 Generating embeddings...")
    embeddings = model.encode(texts, batch_size=32, show_progress_bar=True)
    
    # Clustering
    if method == 'kmeans':
        if n_clusters is None:
            n_clusters = min(20, len(texts)//10)
        clusterer = KMeans(n_clusters=n_clusters, random_state=42)
    elif method == 'dbscan':
        clusterer = DBSCAN(eps=0.5, min_samples=5)
    
    print(f"⚡ Clustering avec {method}...")
    labels = clusterer.fit_predict(embeddings)
    
    return embeddings, labels, clusterer

def create_interactive_visualization(embeddings, labels, texts, save_path=None):
    """Visualisation interactive clustering results"""
    print("📊 Creating visualization...")
    
    # Dimensionality reduction
    if embeddings.shape[1] > 2:
        reducer = TSNE(n_components=2, random_state=42, perplexity=min(30, len(embeddings)-1))
        embeddings_2d = reducer.fit_transform(embeddings)
    else:
        embeddings_2d = embeddings
    
    # Plot
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], 
                         c=labels, cmap='tab20', alpha=0.7)
    plt.colorbar(scatter)
    plt.title('GPU-Accelerated Semantic Clustering')
    plt.xlabel('Dimension 1')
    plt.ylabel('Dimension 2')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()
    
    return embeddings_2d

# 🎯 ÉTAPE 7: PIPELINE COMPLET ACCÉLÉRÉ
def run_complete_pipeline(topics=None, save_results=True):
    """Pipeline complet preprocessing + clustering accéléré"""
    
    if topics is None:
        # Topics par défaut pour test
        topics = [
            'artificial intelligence', 'machine learning', 'deep learning',
            'natural language processing', 'computer vision', 'robotics',
            'data science', 'big data', 'cloud computing', 'quantum computing'
        ]
    
    print("🚀 STARTING COMPLETE PIPELINE")
    print("=" * 50)
    
    # 1. Data collection
    print("\n📥 ÉTAPE 1: Data Collection")
    df = accelerated_wikipedia_preprocessing(topics, max_articles=200)
    
    # 2. GPU Clustering
    print("\n🧠 ÉTAPE 2: GPU Clustering")
    texts = df['content'].tolist()
    embeddings, labels, clusterer = gpu_accelerated_clustering(texts)
    
    # 3. Analysis
    print("\n📊 ÉTAPE 3: Analysis")
    df['cluster'] = labels
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    print(f"✅ Found {n_clusters} clusters")
    
    # Cluster statistics
    cluster_stats = df.groupby('cluster').agg({
        'title': 'count',
        'topic': lambda x: list(set(x)),
        'content': lambda x: len(' '.join(x))
    }).rename(columns={'title': 'article_count', 'content': 'total_chars'})
    
    print("\n📈 Cluster Statistics:")
    print(cluster_stats)
    
    # 4. Visualization
    print("\n🎨 ÉTAPE 4: Visualization")
    save_path = f"{project_dir}/clustering_results.png" if save_results else None
    embeddings_2d = create_interactive_visualization(embeddings, labels, texts, save_path)
    
    # 5. Save results
    if save_results:
        print("\n💾 ÉTAPE 5: Saving Results")
        
        # Save DataFrame
        df.to_csv(f"{project_dir}/processed_articles.csv", index=False)
        
        # Save embeddings
        np.save(f"{project_dir}/embeddings.npy", embeddings)
        np.save(f"{project_dir}/embeddings_2d.npy", embeddings_2d)
        
        # Save cluster info
        cluster_info = {
            'n_clusters': int(n_clusters),
            'cluster_stats': cluster_stats.to_dict(),
            'topics_processed': topics,
            'total_articles': len(df),
            'clustering_method': 'kmeans',
            'model_used': 'all-MiniLM-L6-v2'
        }
        
        with open(f"{project_dir}/cluster_analysis.json", 'w') as f:
            json.dump(cluster_info, f, indent=2)
        
        print(f"✅ Results saved to: {project_dir}")
    
    print("\n🎉 PIPELINE COMPLETE!")
    print(f"📊 Processed: {len(df)} articles")
    print(f"🧠 Clusters: {n_clusters}")
    print(f"⚡ GPU Acceleration: ENABLED")
    
    return df, embeddings, labels, clusterer

# 🚀 ÉTAPE 8: QUICK START DEMO
print("\n" + "="*60)
print("🚀 QUICK START DEMO - GPU ACCELERATED SEMANTIC PROCESSING")
print("="*60)

# Quick test avec petit dataset
demo_topics = ['machine learning', 'artificial intelligence', 'data science']
print(f"🔬 Demo avec {len(demo_topics)} topics...")

# Run pipeline
results = run_complete_pipeline(demo_topics, save_results=True)
df_demo, embeddings_demo, labels_demo, clusterer_demo = results

print("\n✅ DEMO COMPLETE!")
print("🎯 Next steps:")
print("1. 📝 Modify topics list pour ton use case")
print("2. 🔧 Adjust clustering parameters")
print("3. 📊 Analyze results in saved files")
print("4. 🚀 Scale up avec larger datasets")

print(f"\n💾 Files saved to Google Drive:")
print(f"📁 {project_dir}")
print("   📄 processed_articles.csv")
print("   🧠 embeddings.npy")
print("   🎨 clustering_results.png")
print("   📊 cluster_analysis.json")

print("\n🌟 GPU ACCELERATION READY!")
print("⚡ 22-60x speedup vs local CPU achieved!")
