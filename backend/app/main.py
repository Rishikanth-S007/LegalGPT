import sys
from contextlib import asynccontextmanager
import re
import threading

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.config.settings import settings
from app.services.ai_service import ai_service
from app.services.scholarship_service import scholarship_service
from app.api.endpoints import auth
from app.routers import google_auth
from app.db.session import engine
from app.db.base import Base

# Create DB tables
Base.metadata.create_all(bind=engine)

# ============================================================================
# BACKGROUND ENGINE INITIALIZATION - For Render deployment
# ============================================================================
# Thread-safe event to track if engine is ready
engine_ready_event = threading.Event()

def initialize_engine_background():
    """Initialize FAISS and models in background thread"""
    print("\n" + "="*60)
    print("[STARTUP] STARTING LEGALGPT ENGINE IN BACKGROUND...")
    print("="*60)
    
    try:
        # Import and initialize law predictor service
        from app.services import law_predictor_service
        law_predictor_service.initialize()
        
        # Set event - thread-safe notification that engine is ready
        engine_ready_event.set()
        print("="*60)
        print("[SUCCESS] ENGINE READY - Models loaded and cached in memory")
        print("="*60 + "\n")
    except Exception as e:
        print(f"❌ [ERROR] Engine initialization failed: {e}")
        import traceback
        traceback.print_exc()
        # Don't set event - keep engine_ready as False

# ============================================================================
# CUSTOM CORS HANDLER - Supports wildcard patterns
# ============================================================================
def is_cors_allowed(origin: str) -> bool:
    """Check if origin is allowed with wildcard pattern support"""
    allowed_patterns = [
        r"^https?://localhost:3000$",
        r"^https://legalgpt-l5zb\.onrender\.com$",
        r"^https://.*\.vercel\.app$",  # Matches all Vercel deployments
        r"^https://legal-gpt\.vercel\.app$",
    ]
    
    for pattern in allowed_patterns:
        if re.match(pattern, origin):
            return True
    return False

# ============================================================================
# LIFESPAN CONTEXT - Starts server immediately, loads models in background
# ============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start server immediately, initialize engine in background thread"""
    # Start engine in background thread - Server starts immediately without waiting
    try:
        thread = threading.Thread(
            target=initialize_engine_background,
            daemon=True,
            name="engine-init"
        )
        thread.start()
        print("[STARTUP] ⚡ Server started immediately! Engine loading in background...")
        print("          Port is now open for Render health checks ✓")
    except Exception as e:
        print(f"[WARN] Failed to start background thread: {e}")
    
    yield  # Server runs here
    
    # Cleanup (runs on shutdown)
    print("\n[SHUTDOWN] Shutting down LegalGPT engine...")


# Request/Response models
class QueryRequest(BaseModel):
    query: str

class LegalQuery(BaseModel):
    question: str
    language: str = "en"

class ScholarshipQuery(BaseModel):
    query: str
    language: str = "en"
    filters: Optional[dict] = None

# Create the FastAPI application with lifespan
app = FastAPI(
    title=settings.app_name,
    description="AI-powered legal assistant and scholarship finder for your React app",
    version="2.0.0",
    lifespan=lifespan  # <-- This ensures one-time initialization
)

# Add CORS middleware with custom origin checker
@app.middleware("http")
async def cors_middleware(request: Request, call_next):
    """Custom CORS middleware that supports wildcard patterns"""
    origin = request.headers.get("origin")
    
    # Handle preflight requests
    if request.method == "OPTIONS":
        if origin and is_cors_allowed(origin):
            return Response(
                status_code=200,
                headers={
                    "Access-Control-Allow-Origin": origin,
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization",
                    "Access-Control-Allow-Credentials": "true",
                    "Access-Control-Max-Age": "3600",
                },
            )
    
    # Process request
    response = await call_next(request)
    
    # Add CORS headers to response
    if origin and is_cors_allowed(origin):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    
    return response

# Include Auth Router
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(google_auth.router)

# Basic routes
@app.get("/")
def read_root():
    return {
        "message": "🚀 Legal GPT Backend is running!",
        "status": "success",
        "version": "2.0.0",
        "features": ["AI Legal Assistant", "Scholarship Search", "Multilingual Support"]
    }

@app.get("/health")
def health_check():
    """Health check with engine status"""
    is_ready = engine_ready_event.is_set()
    return {
        "status": "ok" if is_ready else "loading",
        "engine_ready": is_ready,
        "timestamp": datetime.now().isoformat(),
        "services": {
            "ai_service": "operational",
            "scholarship_service": "operational",
            "law_engine": "ready" if is_ready else "initializing (2-3 minutes)"
        },
        "message": "Engine ready!" if is_ready else "Engine is loading... Please wait 2-3 minutes."
    }

@app.get("/api/test/ping")
def ping():
    """Simple ping endpoint to test if server is responsive"""
    return {"status": "ok", "message": "pong"}

# AI-Powered Legal Assistant
@app.post("/api/legal/query")
async def process_legal_query(request: LegalQuery):
    """Process legal questions with AI - matches your ChatInterface expectations"""
    
    # Check if engine is ready
    if not engine_ready_event.is_set():
        raise HTTPException(
            status_code=503,
            detail="Engine is still initializing. Please try again in 2-3 minutes."
        )
    
    try:
        # Process with AI service
        ai_response = await ai_service.process_legal_query(
            question=request.question,
            language=request.language
        )
        
        return {
            "query": request.question,
            "response": ai_response["response"],
            "confidence": ai_response["confidence"],
            "language": request.language,
            "related_laws": ai_response["related_laws"],
            "suggested_actions": ai_response["suggested_actions"],
            "timestamp": datetime.now().isoformat(),
            "sender": "assistant"  # Matches your ChatInterface format
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing legal query: {str(e)}"
        )

# Scholarship Search Service
@app.post("/api/scholarship/search")
async def search_scholarships(request: ScholarshipQuery):
    """Search scholarships - matches your ChatInterface expectations"""
    
    try:
        # Search with scholarship service
        search_results = await scholarship_service.search_scholarships(
            query=request.query,
            filters=request.filters,
            language=request.language
        )
        
        return {
            "query": request.query,
            "scholarships": search_results["scholarships"],
            "total_found": search_results["total_found"],
            "language": request.language,
            "search_tips": search_results["search_tips"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching scholarships: {str(e)}"
        )

# Predict Law endpoint
@app.post("/api/predict")
async def predict_law_route(request: QueryRequest):
    """
    Law prediction endpoint - uses pre-loaded global models
    NO model initialization happens here
    """
    # Check if engine is ready
    if not engine_ready_event.is_set():
        raise HTTPException(
            status_code=503,
            detail="Engine is still initializing. Please try again in 2-3 minutes."
        )
    
    try:
        print(f"[API] Received prediction request: {request.query[:50]}...")
        
        from app.services.law_predictor_service import predict_law
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        # Run prediction in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor(max_workers=1)
        
        print("[API] Running prediction in thread pool...")
        result = await loop.run_in_executor(executor, predict_law, request.query)
        
        print(f"[API] Prediction completed. Result type: {type(result)}")
        return {"response": result}
        
    except Exception as e:
        print(f"❌ Prediction error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


# Test endpoints for development
@app.get("/api/test/ai")
async def test_ai_service():
    """Test the AI service"""
    try:
        response = await ai_service.process_legal_query(
            "What are my rights as a consumer?",
            "en"
        )
        return {"status": "AI service working", "sample_response": response}
    except Exception as e:
        return {"status": "AI service error", "error": str(e)}

@app.get("/api/test/scholarships")
async def test_scholarship_service():
    """Test the scholarship service"""
    try:
        response = await scholarship_service.search_scholarships("merit scholarship", {}, "en")
        return {"status": "Scholarship service working", "sample_results": response}
    except Exception as e:
        return {"status": "Scholarship service error", "error": str(e)}
