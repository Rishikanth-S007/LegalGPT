import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder

# Configuration
INDEX_PATH = "C:/LegalGPT/backend/data/legal_index.faiss"
METADATA_PATH = "C:/LegalGPT/backend/data/legal_metadata.json"
DATASET_PATH = "C:/LegalGPT/backend/data/legal_dataset.jsonl"
RE_RANKER_ID = "cross-encoder/ms-marco-MiniLM-L-6-v2"

class LawPredictor:
    def __init__(self):
        print("Initializing High-Precision Law Predictor Engine...")
        
        # Load embedding model
        self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load FAISS index
        if os.path.exists(INDEX_PATH):
            self.index = faiss.read_index(INDEX_PATH)
        else:
            print(f"WARNING: FAISS Index not found at {INDEX_PATH}")
            self.index = None
        
        # Load metadata
        if os.path.exists(METADATA_PATH):
            with open(METADATA_PATH, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
        else:
            print(f"WARNING: Metadata not found at {METADATA_PATH}")
            self.metadata = []
            
        # Load Cross-Encoder
        print(f"Loading re-ranker ({RE_RANKER_ID})...")
        self.cross_encoder = CrossEncoder(RE_RANKER_ID)
        
        print("Engine Ready!")

    def predict(self, user_situation, top_k=10):
        """Predicts the legal outcome using retrieval + re-ranking"""
        if not self.index or not self.metadata:
            return None

        # A. Retrieve top candidates using FAISS
        query_embedding = self.embed_model.encode([user_situation])
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), top_k)
        
        candidates = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                candidates.append(self.metadata[idx])

        if not candidates:
            return None

        # B. Re-rank candidates using Cross-Encoder
        pairs = [[user_situation, cand['instruction']] for cand in candidates]
        scores = self.cross_encoder.predict(pairs)
        
        # Find the best match
        best_idx = np.argmax(scores)
        best_match = candidates[best_idx]
        confidence = float(scores[best_idx])
        
        # Parse the structured output
        parsed_data = self._parse_output(best_match['output'])

        return {
            "prediction": best_match['output'],
            "structured_data": parsed_data,
            "confidence": confidence,
            "relevant_statute": best_match.get('statute', 'Consumer Protection Act, 2019'),
            "source_situation": best_match['instruction']
        }

    def _parse_output(self, output_text: str) -> dict:
        """Parses the Llama-3 assistant output into discrete fields"""
        # A. Strip all Llama-3 / ChatML model tokens aggressively
        import re
        tokens_to_strip = [
            r"<\|begin_of_text\|>",
            r"<\|start_header_id\|>.*?<\|end_header_id\|>",
            r"<\|eot_id\|>",
            r"<\|end_of_text\|>"
        ]
        cleansed_text = output_text
        for pattern in tokens_to_strip:
            cleansed_text = re.sub(pattern, "", cleansed_text, flags=re.DOTALL)
        
        cleansed_text = cleansed_text.strip()

        lines = cleansed_text.split('\n')
        data = {
            "applicable_law": "",
            "legal_position": "",
            "predicted_outcome": "",
            "risk_level": "Medium",
            "next_steps": [],
            "helpline": "",
            "disclaimer": ""
        }

        for line in lines:
            line = line.strip()
            if not line: continue
            
            # Use colon-based detection for more robustness
            if "**Applicable Law + Section:**" in line:
                data["applicable_law"] = line.split("**Applicable Law + Section:**")[-1].strip()
            elif "**Legal Position:**" in line:
                data["legal_position"] = line.split("**Legal Position:**")[-1].strip()
            elif "**Predicted Outcome:**" in line:
                data["predicted_outcome"] = line.split("**Predicted Outcome:**")[-1].strip()
            elif "**Risk Level:**" in line:
                # Extract Risk Level and sanitize (remove extra text like "High probability..." if accidental)
                raw_risk = line.split("**Risk Level:**")[-1].strip()
                if "High" in raw_risk: data["risk_level"] = "High"
                elif "Low" in raw_risk: data["risk_level"] = "Low"
                else: data["risk_level"] = "Medium"
            elif "**Next Steps:**" in line:
                steps_text = line.split("**Next Steps:**")[-1].strip()
                # Split by numbered points (1., 2., 3.) or bullets
                steps = re.split(r'(?:\d+\.\s+|[•\-\*]\s+)', steps_text)
                data["next_steps"] = [s.strip() for s in steps if s.strip()]
            elif "**Helpline Numbers:**" in line:
                data["helpline"] = line.split("**Helpline Numbers:**")[-1].strip()
            elif "**Disclaimer:**" in line:
                data["disclaimer"] = line.split("**Disclaimer:**")[-1].strip()

        return data

# Singleton instance
law_predictor = LawPredictor()
