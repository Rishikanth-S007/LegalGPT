#!/bin/bash
set -e  # Exit on error

echo "=========================================="
echo "Building LegalGPT Backend"
echo "=========================================="

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing Python packages..."
pip install -r requirements.txt

# Pre-download ML models (caches them for faster cold starts)
echo "Pre-downloading sentence-transformers models..."
python -c "
from sentence_transformers import SentenceTransformer, CrossEncoder
print('Downloading embedding model...')
SentenceTransformer('all-MiniLM-L6-v2')
print('Downloading cross-encoder model...')
CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
print('Models cached successfully!')
"

# Verify FAISS index exists
if [ -f "data/legal_index.faiss" ]; then
    echo "✓ FAISS index found ($(du -h data/legal_index.faiss | cut -f1))"
else
    echo "⚠️  WARNING: FAISS index not found at data/legal_index.faiss"
    echo "   The app may fail at runtime. Ensure it's committed to git."
fi

# Verify legal dataset exists
if [ -f "data/legal_dataset.jsonl" ]; then
    echo "✓ Legal dataset found ($(du -h data/legal_dataset.jsonl | cut -f1))"
else
    echo "⚠️  WARNING: Legal dataset not found"
fi

echo "=========================================="
echo "Build completed successfully!"
echo "=========================================="
