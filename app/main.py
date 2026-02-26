import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown events."""
    # Startup
    logger.info("Heritage AI starting up...")
    logger.info(f"Using Ollama model: {settings.ollama_model}")
    logger.info(f"ChromaDB path: {settings.chroma_path}")

    yield

    # Shutdown
    logger.info("Heritage AI shutting down...")


app = FastAPI(
    title="Heritage AI",
    description="Preserving loved ones' memories through AI. Chat with Savta, a warm and wise grandmother persona.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint with welcome message."""
    return {
        "message": "Welcome to Heritage AI",
        "description": "Chat with Savta at /chat, or visit /docs for API documentation",
        "endpoints": {
            "chat": "POST /chat - Chat with Savta",
            "ingest": "POST /ingest - Ingest memory documents",
            "health": "GET /health - Check system health",
            "docs": "GET /docs - API documentation",
        },
    }
