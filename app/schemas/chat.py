from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="The message to send to Savta")
    session_id: Optional[str] = Field(
        default=None,
        description="Session ID for conversation continuity. If not provided, a new session will be created.",
    )


class ChatResponse(BaseModel):
    response: str = Field(..., description="Savta's response")
    session_id: str = Field(..., description="Session ID for follow-up messages")
    sources_found: bool = Field(..., description="Whether relevant memories were found")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class IngestResponse(BaseModel):
    success: bool
    chunks_created: int = 0
    documents_processed: int = 0
    categories: List[str] = []
    error: Optional[str] = None


class HealthResponse(BaseModel):
    status: str = Field(..., description="Overall health status")
    ollama_available: bool = Field(..., description="Whether Ollama is reachable")
    chroma_ready: bool = Field(..., description="Whether ChromaDB has ingested memories")
    model: str = Field(..., description="The LLM model in use")
