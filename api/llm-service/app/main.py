from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
import os

from app.api.routes import router
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="LLM Script Generation Service",
    description="Generate podcast scripts from text using AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, tags=["Script Generation"])

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("=" * 60)
    logger.info("LLM Script Generation Service starting up...")
    logger.info("=" * 60)
    logger.info(f"Service running on port {settings.SERVICE_PORT}")

    # Check LLM Configuration
    logger.info("LLM Provider: Ollama (Primary) / OpenAI (Fallback)")
    logger.info(f"Ollama Base URL: {settings.OLLAMA_BASE_URL}")
    logger.info(f"Ollama Model: {settings.OLLAMA_MODEL}")
    
    if settings.OPENAI_API_KEY:
        logger.info("OpenAI API key configured (Fallback enabled)")
    else:
        logger.warning("OpenAI API key not found (Fallback disabled)")

    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("LLM Script Generation Service shutting down...")

@app.get("/")
async def root():
    """Root endpoint"""
    # Determine actual provider being used
    # Note: We prioritize Ollama, but this is just for display
    llm_provider = "Ollama (Primary) / OpenAI (Fallback)"
    llm_model = f"{settings.OLLAMA_MODEL} / {settings.DEFAULT_MODEL}"

    return {
        "service": "LLM Script Generation Service",
        "version": "1.0.0",
        "description": "Convert text content into engaging podcast dialogue",
        "config": {
            "llm_provider": llm_provider,
            "llm_model": llm_model
        },
        "endpoints": {
            "generate_script": "POST /generate-script - Generate podcast script",
            "refine_script": "POST /refine-script - Refine existing script",
            "validate_content": "POST /validate-content - Validate content suitability",
            "health": "GET /health - Health check",
            "tones": "GET /tones - Available conversation tones",
            "models": "GET /models - Available LLM models",
            "docs": "GET /docs - API documentation"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.SERVICE_PORT)
