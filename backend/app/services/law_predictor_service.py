import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder
from functools import lru_cache
import re

# ============================================================================
# CONFIGURATION
# ============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "..", "data")
INDEX_PATH = os.path.join(DATA_DIR, "legal_index.faiss")
METADATA_PATH = os.path.join(DATA_DIR, "legal_metadata.json")
DATASET_PATH = os.path.join(DATA_DIR, "legal_dataset.jsonl")
CROSS_ENCODER_ID = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# ============================================================================
# GLOBAL VARIABLES - Loaded ONCE at startup
# ============================================================================
_embed_model = None
_cross_encoder = None
_index = None
_metadata = None
_response_cache = {}
_cache_max_size = 100
_is_initialized = False


# ============================================================================
# INITIALIZATION FUNCTION - Called by FastAPI lifespan
# ============================================================================
def _initialize_models():
    """
    Initialize the LegalGPT engine ONCE at server startup.
    Loads models and builds FAISS index into global variables.
    """
    global _embed_model, _cross_encoder, _index, _metadata, _is_initialized
    
    if _is_initialized:
        print("[WARN] Engine already initialized, skipping...")
        return
    
    print("\n" + "-"*60)
    print("[INIT] Initializing Multi-Law Predictor Engine...")
    print("-"*60)
    
    # Load embedding model
    print("[LOAD] Loading Sentence Transformer model...")
    _embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    print("[OK] Embedding model loaded")
    
    # Load cross-encoder for reranking
    print("[LOAD] Loading Cross-Encoder reranker...")
    _cross_encoder = CrossEncoder(CROSS_ENCODER_ID)
    print("[OK] Cross-encoder loaded")
    
    # Build FAISS index from dataset
    print("[BUILD] Building FAISS index from legal dataset...")
    _build_index()
    
    _is_initialized = True
    print("-"*60)
    print(f"[SUCCESS] Indexed {len(_metadata)} legal scenarios")
    print("-"*60 + "\n")


def _build_index():
    """Build FAISS index from legal_dataset.jsonl"""
    global _index, _metadata, _embed_model
    
    if not os.path.exists(DATASET_PATH):
        print(f"[ERROR] Dataset not found at {DATASET_PATH}")
        _index = None
        _metadata = []
        return
    
    # Load dataset
    data = []
    with open(DATASET_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    
    _metadata = data
    instructions = [item['instruction'] for item in data]
    
    # Generate embeddings
    print(f"   Encoding {len(instructions)} legal scenarios...")
    embeddings = _embed_model.encode(instructions, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')
    
    # Build FAISS index
    dimension = embeddings.shape[1]
    _index = faiss.IndexFlatL2(dimension)
    _index.add(embeddings)
    
    # Save for persistence
    faiss.write_index(_index, INDEX_PATH)
    with open(METADATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    
    print(f"   [OK] Index built successfully!")


# ============================================================================
# LAWPREDICTOR CLASS
# ============================================================================
class LawPredictor:
    """Hybrid retrieval + re-ranking engine for legal prediction"""
    
    def __init__(self):
        """Initialize models and build/load FAISS index"""
        global _embed_model, _cross_encoder, _index, _metadata
        
        # Use already loaded models
        self.embed_model = _embed_model
        self.cross_encoder = _cross_encoder
        self.index = _index
        self.metadata = _metadata
        
        # Initialize cache
        self._response_cache = {}
        self._cache_max_size = 1000
    
    def calculate_confidence(self, distance, keyword_match=False, cross_encoder_score=None):
        """
        Calculate confidence score from multiple signals:
        - FAISS distance (primary signal)
        - Keyword matching (boolean boost)
        - Cross-encoder score (optional additional signal)
        Returns value between 0.0 and 1.0
        """
        # Base confidence from FAISS distance
        # Lower distance = higher confidence
        # Typical FAISS L2 distances range from 0 (perfect match) to ~100+ (very different)
        # We use an exponential decay with adjusted scale
        base_confidence = float(np.exp(-distance / 10.0))  # Adjusted scale for better distribution
        
        # Keyword match boost: +0.1 to confidence if keywords matched
        keyword_boost = 0.15 if keyword_match else 0.0
        
        # Cross-encoder boost (if available): normalize to 0-0.15 range
        cross_encoder_boost = 0.0
        if cross_encoder_score is not None:
            # Cross-encoder scores typically range from -10 to 10
            # Use sigmoid to normalize to 0-1, then scale to 0-0.15
            normalized_ce = 1.0 / (1.0 + np.exp(-float(cross_encoder_score)))
            cross_encoder_boost = normalized_ce * 0.15
        
        # Combine all signals
        confidence = base_confidence + keyword_boost + cross_encoder_boost
        
        # Clamp to [0.0, 1.0] and round to 2 decimals
        return round(max(0.0, min(1.0, confidence)), 2)

    def _get_category_from_query(self, text):
        mapping = {
            'rape': 'Rape/Sexual Assault', 'pocso': 'Rape/Sexual Assault', 'sexual': 'Rape/Sexual Assault',
            'moneylender': 'Moneylender Harassment', 'loan': 'Moneylender Harassment',
            'threat': 'Moneylender Harassment', 'extortion': 'Moneylender Harassment',
            'beat': 'Assault/Physical Harm', 'assault': 'Assault/Physical Harm',
            'slap': 'Assault/Physical Harm', 'harm': 'Assault/Physical Harm',
            'murder': 'Murder/Homicide', 'homicide': 'Murder/Homicide', 'death': 'Murder/Homicide',
            'steal': 'Theft/Robbery', 'stole': 'Theft/Robbery', 'theft': 'Theft/Robbery', 'robbery': 'Theft/Robbery', 'snatch': 'Theft/Robbery',
            # Expanded Drug Trafficking routing
            'drug': 'Drug Trafficking', 'ndps': 'Drug Trafficking', 'narcotic': 'Drug Trafficking', 'airport': 'Drug Trafficking', 'smuggling': 'Drug Trafficking',
            # ARMS Act expanded
            'arms licence': 'Arms Act Offenses', 'gun': 'Arms Act Offenses', 'pistol': 'Arms Act Offenses', 'rifle': 'Arms Act Offenses', 'firearm': 'Arms Act Offenses',
            'weapon': 'Arms Act Offenses', 'unlicensed gun': 'Arms Act Offenses', 'illegal weapon': 'Arms Act Offenses', 'country-made': 'Arms Act Offenses',
            # Kidnapping/Abduction expanded
            'kidnap': 'Kidnapping/Abduction', 'abduct': 'Kidnapping/Abduction', 'stole my wife': 'Kidnapping/Abduction', 'stole my husband': 'Kidnapping/Abduction', 'took my wife': 'Kidnapping/Abduction',
            'took my child': 'Kidnapping/Abduction', 'missing person': 'Kidnapping/Abduction', 'ransom': 'Kidnapping/Abduction', 'forcefully taken': 'Kidnapping/Abduction',
            # Motor Vehicles Act expanded
            'impound': 'Motor Vehicles Act Violations', 'wrong parking': 'Motor Vehicles Act Violations',
            'towed': 'Motor Vehicles Act Violations', 'hit with bike': 'Motor Vehicles Act Violations',
            'hit with car': 'Motor Vehicles Act Violations', 'road accident': 'Motor Vehicles Act Violations', 'traffic police': 'Motor Vehicles Act Violations', 'rash driving': 'Motor Vehicles Act Violations',
            'drunk driving': 'Motor Vehicles Act Violations', 'knocked down': 'Motor Vehicles Act Violations',
            'modification': 'Motor Vehicles Act Violations', 'modified bike': 'Motor Vehicles Act Violations', 'illegal vehicle': 'Motor Vehicles Act Violations',
            # Existing
            'consumer': 'Consumer Issues', 'defect': 'Consumer Issues','fault': 'Consumer Issues',
            'fraud': 'Fraud/Cheating', 'cheat': 'Fraud/Cheating', 'cheating': 'Fraud/Cheating',
            'cyber': 'Cybercrime', 'hack': 'Cybercrime', 'phish': 'Cybercrime',
            'violence': 'Domestic Violence', 'dowry': 'Domestic Violence', 'abuse': 'Domestic Violence',
        }
        for k, v in mapping.items():
            if k in text.lower():
                return v
        return None

    def predict(self, user_situation, top_k=3, forced_category=None):
        """Predicts the legal outcome using retrieval + re-ranking and category filter with caching"""
        if not self.index or not self.metadata:
            return {"prediction": "System not indexed.", "confidence": 0}

        # Create cache key from normalized query and category
        cache_key = f"{user_situation.lower().strip()}_{forced_category or 'none'}"
        
        # Check cache first
        if cache_key in self._response_cache:
            print(f"Cache HIT for query: {user_situation[:50]}...")
            return self._response_cache[cache_key]
        
        print(f"Cache MISS for query: {user_situation[:50]}...")

        # Strict category force-routing (bypass FAISS, use ALL records matching category)
        if forced_category:
            matched_candidates = [item for item in self.metadata if item.get('category') == forced_category]
            if not matched_candidates:
                return {"prediction": f"No results found for category: {forced_category}.", "confidence": 0}
            pairs = [[user_situation, cand['instruction']] for cand in matched_candidates]
            scores = self.cross_encoder.predict(pairs)
            best_indices = np.argsort(scores)[::-1][:top_k]
            top_matches = [matched_candidates[i] for i in best_indices]
            best_match = top_matches[0]
            # Normalize cross-encoder score to 0.0-1.0 range using sigmoid
            raw_score = float(scores[best_indices[0]] if best_indices.size > 0 else 0)
            confidence = 1.0 / (1.0 + np.exp(-raw_score))  # Sigmoid normalization
            confidence = round(max(0.0, min(1.0, confidence)), 2)  # Clamp to [0,1]
        else:
            # Category routing logic (legacy partial filtering)
            predicted_category = self._get_category_from_query(user_situation)
            has_keyword_match = predicted_category is not None
            large_k = 50
            query_embedding = self.embed_model.encode([user_situation])
            distances, indices = self.index.search(np.array(query_embedding).astype('float32'), large_k)
            candidates = [self.metadata[i] for i in indices[0]]
            dists = distances[0]

            # Filter by detected category if any, else use all
            if predicted_category:
                filtered = [(cand, dists[idx]) for idx, cand in enumerate(candidates) if cand.get('category') == predicted_category]
                if filtered:
                    filtered_candidates, filtered_distances = zip(*filtered)
                else:
                    filtered_candidates, filtered_distances = candidates, dists
            else:
                filtered_candidates, filtered_distances = candidates, dists
            # At least 1 candidate
            if not filtered_candidates:
                filtered_candidates, filtered_distances = candidates, dists

            # B. Re-rank filtered candidates using Cross-Encoder for precision
            pairs = [[user_situation, cand['instruction']] for cand in filtered_candidates]
            scores = self.cross_encoder.predict(pairs)
            
            # Find the best match within filtered pool
            best_indices = np.argsort(scores)[::-1][:top_k]
            top_matches = [filtered_candidates[i] for i in best_indices]
            best_match = top_matches[0]

            # Calculate enhanced confidence using multiple signals
            best_idx = best_indices[0]
            faiss_distance = filtered_distances[best_idx]
            cross_encoder_score = float(scores[best_idx])
            confidence = self.calculate_confidence(
                distance=faiss_distance, 
                keyword_match=has_keyword_match,
                cross_encoder_score=cross_encoder_score
            )

        # Extract structured result
        output_text = best_match['output'].split("assistant<|end_header_id|>")[-1].replace("<|eot_id|>", "").strip()
        structured_data = self._parse_output(output_text)

        # Confidence threshold for out-of-scope queries - applies to ALL queries
        if confidence < 0.10:
            result = {
                "applicable_law": "Out of Scope",
                "legal_position": "This query does not relate to a legal matter. LegalGPT covers: Theft, Assault, Rape, Murder, Drugs, Kidnapping, Arms, Motor Vehicles, Domestic Violence, Cybercrime, Fraud, Consumer Rights, Property Disputes, Labour Law.",
                "predicted_outcome": "Please ask a specific legal question.",
                "risk_level": "Unknown",
                "next_steps": [
                    "Rephrase with legal details",
                    "Consult a lawyer: 15100"
                ],
                "helpline": "Legal Aid: 15100",
                "disclaimer": "AI guidance only.",
                "confidence": confidence
            }
        else:
            result = {
                "prediction": output_text,
                "confidence": confidence,
                "relevant_statute": best_match['statute'],
                "source_situation": best_match['instruction'],
                "structured_data": structured_data
            }

        # Store in cache (with size limit)
        if len(self._response_cache) >= self._cache_max_size:
            # Remove oldest entry (FIFO)
            first_key = next(iter(self._response_cache))
            del self._response_cache[first_key]
        self._response_cache[cache_key] = result
        
        return result
    
    def _parse_output(self, output_text: str) -> dict:
        """Parses the Llama-3 assistant output into discrete fields"""
        import re
        
        # Strip all Llama-3 / ChatML model tokens
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
            if not line:
                continue
            
            # Use colon-based detection for more robustness
            if "**Applicable Law + Section:**" in line:
                data["applicable_law"] = line.split("**Applicable Law + Section:**")[-1].strip()
            elif "**Legal Position:**" in line:
                data["legal_position"] = line.split("**Legal Position:**")[-1].strip()
            elif "**Predicted Outcome:**" in line:
                data["predicted_outcome"] = line.split("**Predicted Outcome:**")[-1].strip()
            elif "**Risk Level:**" in line:
                raw_risk = line.split("**Risk Level:**")[-1].strip()
                if "High" in raw_risk:
                    data["risk_level"] = "High"
                elif "Low" in raw_risk:
                    data["risk_level"] = "Low"
                else:
                    data["risk_level"] = "Medium"
            elif "**Next Steps:**" in line:
                steps_text = line.split("**Next Steps:**")[-1].strip()
                steps = re.split(r'(?:\d+\.\s+|[•\-\*]\s+)', steps_text)
                data["next_steps"] = [s.strip() for s in steps if s.strip()]
            elif "**Helpline Numbers:**" in line:
                data["helpline"] = line.split("**Helpline Numbers:**")[-1].strip()
            elif "**Disclaimer:**" in line:
                data["disclaimer"] = line.split("**Disclaimer:**")[-1].strip()
        
        return data


# ============================================================================
# MODULE-LEVEL INITIALIZATION (loads engine once at server startup)
# ============================================================================
_law_predictor_instance = None


def initialize():
    """
    Initialize the LawPredictor instance ONCE.
    First loads models into globals, then creates _law_predictor_instance.
    """
    global _law_predictor_instance
    
    if _law_predictor_instance is not None:
        print("[WARN] Engine already initialized, skipping...")
        return
    
    # First, initialize models into global variables
    _initialize_models()
    
    # Then create the LawPredictor instance
    print("\n" + "="*60)
    print("[INIT] Creating LawPredictor instance...")
    print("="*60)
    _law_predictor_instance = LawPredictor()
    print("="*60)
    print("[SUCCESS] Engine Ready!")
    print("="*60 + "\n")


# ============================================================================
# OUT-OF-SCOPE NON-LEGAL QUERY FILTER
# ============================================================================
NON_LEGAL_QUERIES = [
    "weather", "temperature", "forecast", "rain", "sunny", "climate",
    "recipe", "cook", "food", "restaurant", "menu", "dish",
    "joke", "funny", "laugh", "comedy", "humor",
    "movie", "film", "actor", "actress", "cinema",
    "song", "music", "singer", "lyrics", "album",
    "game", "play", "sport", "cricket", "football", "basketball",
    "color", "favorite", "like", "love", "hate",
    "hello", "hi", "hey", "greetings", "good morning", "good evening",
    "thank", "thanks", "welcome", "bye", "goodbye",
    "calculator", "math", "calculate", "add", "subtract", "multiply",
    "time", "date", "clock", "calendar", "today",
    "animal", "pet", "dog", "cat", "bird",
    "travel", "vacation", "holiday", "trip", "tour",
    "shopping", "buy", "purchase", "sale", "discount"
]

# Safety net: legal action words that guarantee legal relevance
LEGAL_ACTION_WORDS = [
    "stole", "stolen", "theft", "robbed", "robbery",
    "hacked", "hack", "fraud", "cheated", "scam",
    "beaten", "attacked", "assaulted", "hit", "beat",
    "kidnapped", "abducted", "missing", "ransom",
    "murdered", "killed", "shot", "stabbed", "poisoned",
    "raped", "molested", "abused", "sexual assault",
    "arrested", "caught", "police", "fir", "complaint",
    "legal", "court", "judge", "lawyer", "advocate",
    "drug", "gun", "weapon", "firearm", "pistol",
    "accident", "injured", "hurt", "harm",
    "harassed", "threatened", "blackmail", "threat",
    "fired", "salary", "employer", "employee",
    "insurance", "refund", "defective", "defect",
    "encroach", "property", "landlord", "tenant",
    "divorce", "alimony", "custody", "dowry",
    "consumer", "business", "contract", "agreement"
]


def predict_law(query: str, forced_category: str = None):
    """Main prediction function with comprehensive keyword-to-category mapping and safety net for legal queries"""
    
    query_lower = query.lower()
    
    # STEP 1: DV Act + POCSO Act hybrid detection (early escape)
    if forced_category != "DV Act + POCSO Act" and (any(w in query_lower for w in ["father-in-law", "mother-in-law", "in-laws", "relative", "family member", "physically abused my", "abused my children"]) and any(y in query_lower for y in ["child", "children", "kids", "minor"])):
        detected_category = "DV Act + POCSO Act"
        final_category = detected_category
        if _law_predictor_instance is None:
            print("[WARN] Engine not initialized! Initializing now...")
            initialize()
        dv_result = _law_predictor_instance.predict(query, forced_category="Domestic Violence")
        pocso_result = _law_predictor_instance.predict(query, forced_category="Rape/Sexual Assault")
        merged_applicable_laws = set()
        if dv_result:
            dv_law = dv_result.get('structured_data', {}).get('applicable_law') or dv_result.get('applicable_law')
            if dv_law and dv_law != 'Out of Scope':
                merged_applicable_laws.add(dv_law)
        if pocso_result:
            pocso_law = pocso_result.get('structured_data', {}).get('applicable_law') or pocso_result.get('applicable_law')
            if pocso_law and pocso_law != 'Out of Scope':
                merged_applicable_laws.add(pocso_law)
        merged_applicable_laws.add("POCSO Act")
        merged_applicable_law_str = " + ".join(sorted(merged_applicable_laws))
        merged_legal_position = (dv_result.get('structured_data', {}).get('legal_position', '') + '\n' + pocso_result.get('structured_data', {}).get('legal_position', '')).strip()
        dv_conf = dv_result.get('confidence', 0)
        pocso_conf = pocso_result.get('confidence', 0)
        confidence = max(dv_conf, pocso_conf)
        if (not dv_conf or dv_conf < 0.1) and (not pocso_conf or pocso_conf < 0.1):
            return {
                "applicable_law": "DV Act + POCSO Act",
                "legal_position": "Child abuse by a family member (including father-in-law or relative) is punishable under both the Domestic Violence Act and the Protection of Children from Sexual Offenses (POCSO) Act. Victims are entitled to protection and legal remedy.",
                "confidence": 1.0,
                "source": "Hybrid override"
            }
        return {
            "applicable_law": merged_applicable_law_str,
            "legal_position": merged_legal_position if merged_legal_position else "Legal protection under DV Act and POCSO Act for children in domestic scenarios.",
            "confidence": confidence,
            "source": "Merged DV Act + POCSO Act"
        }
    
    # STEP 2: Non-legal blocklist filter (reject clearly non-legal queries)
    if any(term in query_lower for term in NON_LEGAL_QUERIES):
        print(f"[WARN] Out-of-scope query detected: {query[:50]}...")
        return {
            "applicable_law": "Out of Scope",
            "legal_position": "This query does not relate to a legal matter. LegalGPT specializes in Indian law including: Theft, Assault, Rape, Murder, Drugs, Kidnapping, Arms Act, Motor Vehicles, Domestic Violence, Cybercrime, Fraud, Consumer Rights, Property Disputes, Labour Law, Education Rights, and Moneylender Harassment.",
            "predicted_outcome": "Please ask a specific legal question.",
            "risk_level": "Unknown",
            "next_steps": [
                "Rephrase with legal context",
                "Contact Legal Aid Helpline: 15100"
            ],
            "helpline": "Legal Aid: 15100",
            "disclaimer": "AI-generated guidance only. Consult a licensed advocate for court matters.",
            "confidence": 0.0
        }
    
    # STEP 3: Check for legal action words (safety net)
    has_legal_words = any(word in query_lower for word in LEGAL_ACTION_WORDS)
    
    # STEP 4: Comprehensive keyword mapping to categories
    detected_category = None
    
    # Arms Act - highest priority
    if any(w in query_lower for w in [
        "gun", "pistol", "rifle", "firearm",
        "country made gun", "illegal gun",
        "arms licence", "weapon", "revolver", "country-made"
    ]):
        detected_category = "Arms Act Offenses"
    
    # Motor Vehicles Act
    elif any(w in query_lower for w in [
        "parking", "impound", "towed", "traffic police",
        "hit pedestrian", "hit a pedestrian", "hit a person with",
        "knocked down pedestrian", "ran over", "ran over pedestrian",
        "hit person with car", "hit person with bike",
        "vehicle accident", "car accident injured",
        "road accident", "rash driving", "drunk driving",
        "vehicle seized", "knocked down", "hit with bike",
        "hit with car", "driving fast"
    ]):
        detected_category = "Motor Vehicles Act Violations"
    
    # Kidnapping/Abduction
    elif any(w in query_lower for w in [
        "kidnap", "abduct", "ransom",
        "stole my wife", "stole my husband",
        "took my wife", "took my child",
        "wife missing", "child missing", "wife kidnapped"
    ]):
        detected_category = "Kidnapping/Abduction"
    
    # Drug Trafficking
    elif any(w in query_lower for w in [
        "drug", "cocaine", "heroin", "marijuana",
        "ganja", "narcotic", "ndps", "charas",
        "opium", "mdma", "smuggling drugs"
    ]):
        detected_category = "Drug Trafficking"
    
    # Cybercrime (BEFORE THEFT - higher priority)
    elif any(w in query_lower for w in [
        "hack", "hacked", "hack my", "hacked my", "cyber",
        "bank account hacked", "account hacked", "someone hacked",
        "got hacked", "my account was hacked",
        "online theft", "digital theft",
        "otp fraud", "upi fraud", "upi scam",
        "phishing", "fake profile", "fake website",
        "identity theft", "online scam",
        "lost money online", "fraud call",
        "scam call", "phone fraud", "otp scam",
        "bank fraud call", "online money lost",
        "digital fraud", "payment fraud"
    ]):
        detected_category = "Cybercrime"
    
    # Theft/Robbery
    elif any(w in query_lower for w in [
        "stole", "theft", "stolen", "snatched",
        "stolen from my", "stole from my",
        "taken from my bag", "stolen from bag",
        "laptop stolen", "phone stolen",
        "bag stolen", "wallet stolen",
        "robbery", "pickpocket", "burglary",
        "broke into", "house break"
    ]):
        detected_category = "Theft/Robbery"
    
    # Rape/Sexual Assault
    elif any(w in query_lower for w in [
        "rape", "raping", "raped",
        "sexual assault", "sexually assaulted a", "sexually assaulted",
        "teacher assaulted", "assaulted a child", "assaulted a minor",
        "assaulted a 13", "assaulted a 14", "child sexual",
        "minor assaulted", "teacher abused",
        "molest", "pocso", "sexually abused", "outraged modesty"
    ]):
        detected_category = "Rape/Sexual Assault"
    
    # Assault/Physical Harm (including Acid Attacks)
    elif any(w in query_lower for w in [
        "beat", "beaten", "slapped", "slap", "punched",
        "kicked", "attacked me", "hurt me",
        "assault", "hit me", "physical harm",
        "physically hurt", "punched me", "kicked me",
        "boss hit", "teacher hit", "colleague attacked",
        "threw acid", "acid attack", "acid thrown",
        "burned with acid", "attacked with acid"
    ]):
        detected_category = "Assault/Physical Harm"
    
    # Murder/Homicide
    elif any(w in query_lower for w in [
        "murder", "killed", "kill", "shot dead",
        "stabbed", "poisoned", "attempt to murder",
        "tried to shoot", "tried to kill", "shot at me",
        "someone shot", "fired at me", "shooting at me",
        "tried to stab", "attempted murder"
    ]):
        detected_category = "Murder/Homicide"
    
    # Domestic Violence (with POCSO check for children)
    elif any(w in query_lower for w in [
        "husband beats", "beats me every", "beats me every night",
        "wife beats", "beats me daily", "husband hits me",
        "husband is abusive", "domestic abuse", "spouse beats",
        "dowry", "498a", "in-laws torture", "domestic violence",
        "marital abuse", "cruelty by husband",
        "father-in-law", "mother-in-law", "in-laws",
        "abused my children", "abused my kids",
        "relative abuse", "family member abuse",
        "physically abused my"
    ]):
        if any(w in query_lower for w in ["child", "children", "kids", "minor"]):
            detected_category = "DV Act + POCSO Act"
        else:
            detected_category = "Domestic Violence"
    
    # Fraud/Cheating
    elif any(w in query_lower for w in [
        "cheated", "cheated me of money", "fake seller", "forged",
        "breach of trust", "scam", "deceived",
        "false promise", "took money and ran",
        "contractor took money", "took advance and ran",
        "took payment and disappeared", "advance payment fraud",
        "contractor took", "advance and disappeared", 
        "took advance and", "took advance", "took money disappeared",
        "took money and disappeared", "payment disappeared", "builder took money",
        "took deposit ran", "advance fraud",
        "contractor ran away", "contractor disappeared",
        "took money ran", "money and ran",
        "paid but ran", "paid him and he ran", "took payment ran"
    ]):
        detected_category = "Fraud/Cheating"
    
    # Consumer Issues
    elif any(w in query_lower for w in [
        "defective product", "refund denied",
        "builder delay", "insurance rejected",
        "defective phone", "phone stopped working", "stopped working after",
        "phone not working", "product stopped", "stopped working",
        "not working after", "broke down after", "malfunctioned after",
        "service deficiency", "consumer complaint", "flat possession",
        "builder", "rera", "apartment delay",
        "property delay", "housing complaint",
        "insurance claim denied", "claim rejected",
        "policy claim rejected",
        "insurance claim", "insurance denied", "insurance company",
        "policy rejected", "health insurance", "car insurance claim",
        "insurance refused", "insurance issue", "claim denied",
        "insurance problem", "insurance dispute"
    ]):
        detected_category = "Consumer Issues"
    
    # Property Disputes
    elif any(w in query_lower for w in [
        "encroaching on my", "encroaching on", "encroached my land",
        "occupied my land", "neighbor encroach", "illegal occupation",
        "trespassed my", "entered my property"
    ]):
        detected_category = "Property Disputes"
    
    # Use detected category or fallback to forced_category
    final_category = detected_category if detected_category else forced_category
    
    # Ensure engine is initialized
    if _law_predictor_instance is None:
        print("[WARN] Engine not initialized! Initializing now...")
        initialize()
    
    # STEP 5: Safety net - if query has legal words but no category, force FAISS search
    if not final_category and has_legal_words:
        print(f"[INFO] No keyword match detected, but query contains legal action words. Running FAISS search...")
        result = _law_predictor_instance.predict(query, forced_category=None)
        # Additional safety: if FAISS confidence is very low but legal words present, still return result
        if result.get('confidence', 0) < 0.10 and has_legal_words:
            print(f"[INFO] Legal query with low confidence detected. Returning result anyway due to legal action words.")
        return result
    
    # STEP 6: Reject only if no category AND no legal words
    if not final_category:
        print(f"[WARN] No legal category detected and no legal action words found: {query[:50]}... returning Out of Scope.")
        return {
            "applicable_law": "Out of Scope",
            "legal_position": "This query does not relate to a legal matter. LegalGPT specializes in Indian law including: Theft, Assault, Rape, Murder, Drugs, Kidnapping, Arms Act, Motor Vehicles, Domestic Violence, Cybercrime, Fraud, Consumer Rights, Property Disputes, Labour Law, Education Rights, and Moneylender Harassment.",
            "predicted_outcome": "Please ask a specific legal question.",
            "risk_level": "Unknown",
            "next_steps": [
                "Rephrase with legal context",
                "Contact Legal Aid Helpline: 15100"
            ],
            "helpline": "Legal Aid: 15100",
            "disclaimer": "AI-generated guidance only. Consult a licensed advocate for court matters.",
            "confidence": 0.0
        }
    
    # STEP 7: Handle hybrid DV Act + POCSO Act category
    if final_category == "DV Act + POCSO Act":
        dv_result = _law_predictor_instance.predict(query, forced_category="Domestic Violence")
        pocso_result = _law_predictor_instance.predict(query, forced_category="Rape/Sexual Assault")
        
        merged_applicable_laws = set()
        if dv_result:
            dv_law = dv_result.get('structured_data', {}).get('applicable_law') or dv_result.get('applicable_law')
            if dv_law and dv_law != 'Out of Scope':
                merged_applicable_laws.add(dv_law)
        if pocso_result:
            pocso_law = pocso_result.get('structured_data', {}).get('applicable_law') or pocso_result.get('applicable_law')
            if pocso_law and pocso_law != 'Out of Scope':
                merged_applicable_laws.add(pocso_law)
        merged_applicable_laws.add("POCSO Act")
        merged_applicable_law_str = " + ".join(sorted(merged_applicable_laws))
        
        merged_legal_position = (dv_result.get('structured_data', {}).get('legal_position', '') + '\n' + pocso_result.get('structured_data', {}).get('legal_position', '')).strip()
        dv_conf = dv_result.get('confidence', 0)
        pocso_conf = pocso_result.get('confidence', 0)
        confidence = max(dv_conf, pocso_conf)
        
        if (not dv_conf or dv_conf < 0.1) and (not pocso_conf or pocso_conf < 0.1):
            return {
                "applicable_law": "DV Act + POCSO Act",
                "legal_position": "Child abuse by a family member (including father-in-law or relative) is punishable under both the Domestic Violence Act and the Protection of Children from Sexual Offenses (POCSO) Act. Victims are entitled to protection and legal remedy.",
                "confidence": 1.0,
                "source": "Hybrid override"
            }
        return {
            "applicable_law": merged_applicable_law_str,
            "legal_position": merged_legal_position if merged_legal_position else "Legal protection under DV Act and POCSO Act for children in domestic scenarios.",
            "confidence": confidence,
             "source": "Merged DV Act + POCSO Act"
         }
    
    # STEP 8: Default - call predictor with detected/forced category
    result = _law_predictor_instance.predict(query, forced_category=final_category)
    
    # STEP 9: Safety net - if we detected a category but confidence is very low, still override the result
    # because the category keyword match is a strong signal that this is a legal query
    if detected_category and result.get('applicable_law') == 'Out of Scope' and result.get('confidence', 0) < 0.20:
        print(f"[INFO] Category '{detected_category}' matched via keywords. Overriding low confidence Out of Scope result with legal guidance.")
        
        # Special handling for Consumer Issues - provide full CPA 2019 details
        if detected_category == "Consumer Issues":
            result = {
                "applicable_law": "Consumer Protection Act 2019",
                "legal_position": "This constitutes deficiency in service under Consumer Protection Act 2019 (CPA). Section 2(11) defines deficiency in service. Section 35 allows filing complaint at District Consumer Commission. Insurance rejection without valid reason is a deficiency in service. You can claim compensation and interest. File complaint at e-Daakhil portal: edaakhil.nic.in",
                "predicted_outcome": "High probability of relief if documents are preserved.",
                "risk_level": "Medium",
                "next_steps": [
                    "Send legal notice to insurance company",
                    "File complaint at District Consumer Commission",
                    "Use e-Daakhil portal for online filing",
                    "Claim compensation for mental harassment"
                ],
                "helpline": "Consumer Helpline: 1800-11-4000",
                "disclaimer": "AI-generated advice. Consult a licensed advocate for court matters.",
                "confidence": 0.85
            }
        else:
            # Return a generic legal response for other detected categories
            result = {
                "applicable_law": detected_category,
                "legal_position": f"Your query appears to relate to {detected_category}. LegalGPT is analyzing applicable laws for this category. Please consult with a licensed legal advocate for comprehensive guidance.",
                "predicted_outcome": "Consult legal counsel for detailed analysis.",
                "risk_level": "To be determined",
                "next_steps": [
                    "Contact a legal advocate",
                    "File formal complaint if needed",
                    "Call Legal Aid Helpline: 15100"
                ],
                "helpline": "Legal Aid: 15100",
                "disclaimer": "AI-generated guidance only. Consult a licensed advocate for court matters.",
                "confidence": max(result.get('confidence', 0), 0.70)
            }
    
    return result


if __name__ == "__main__":
    # Test logic
    predictor = LawPredictor()
    queries = [
        "Someone snatched my chain",
        "My phone is defective",
        "Dealer caught with drugs",
        "Threatening moneylender"
    ]
    for q in queries:
        print(f"\nQuery: {q}")
        res = predictor.predict(q)
        print(f"Statute: {res['relevant_statute']}")
        print(res['prediction'][:200] + "...")
