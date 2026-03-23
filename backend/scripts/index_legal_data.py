import json
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# 1. Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, "..", "data", "legal_dataset.jsonl")
index_save_path = os.path.join(BASE_DIR, "..", "data", "legal_index.faiss")
metadata_save_path = os.path.join(BASE_DIR, "..", "data", "legal_metadata.json")

def index_data():
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}")
        return

    print("Loading dataset...")
    data = []
    with open(dataset_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    
    # Extract instructions for embedding (these are the user situations/questions)
    texts_to_embed = [item['instruction'] for item in data]
    print(f"Loaded {len(texts_to_embed)} examples.")
    
    print("Loading embedding model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("Generating embeddings (this may take a minute on CPU)...")
    embeddings = model.encode(texts_to_embed, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')
    
    # Initialize FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    
    print("Adding embeddings to FAISS index...")
    index.add(embeddings)
    
    # Save index
    print(f"Saving index to {index_save_path}...")
    faiss.write_index(index, index_save_path)
    
    # Save metadata (the actual answers)
    print(f"Saving metadata to {metadata_save_path}...")
    with open(metadata_save_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    
    print("Indexing complete!")

if __name__ == "__main__":
    index_data()
