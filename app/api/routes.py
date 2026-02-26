import logging

from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.core.ingest import ingest_memories
from app.core.llm import llm
from app.core.retriever import retriever
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    IngestResponse,
)
from app.services.chat_service import chat_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat with Savta - the Heritage AI grandmother persona.

    Send a message and receive a warm, wise response from Savta.
    Optionally include a session_id for conversation continuity.
    """
    try:
        result = chat_service.chat(
            message=request.message,
            session_id=request.session_id,
        )
        return ChatResponse(**result)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest", response_model=IngestResponse)
async def ingest() -> IngestResponse:
    """
    Ingest memory documents from the data directory.

    This will load all markdown files from data/stories, data/recipes,
    and data/wisdom, chunk them, embed them, and store in ChromaDB.
    """
    try:
        result = ingest_memories()
        return IngestResponse(**result)
    except Exception as e:
        logger.error(f"Error in ingest endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """
    Check the health of the Heritage AI system.

    Returns status of Ollama and ChromaDB connections.
    """
    ollama_ok = llm.is_available()
    chroma_ok = retriever.is_ready()

    status = "healthy" if (ollama_ok and chroma_ok) else "degraded"
    if not ollama_ok:
        status = "unhealthy"

    return HealthResponse(
        status=status,
        ollama_available=ollama_ok,
        chroma_ready=chroma_ok,
        model=settings.ollama_model,
    )
