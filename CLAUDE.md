# Heritage AI - Project Context

## Overview
Heritage AI is a proof-of-concept application that demonstrates how AI can preserve and make interactive the memories of loved ones. The demo features "Savta" (Hebrew for grandmother), a Holocaust survivor grandmother persona built using RAG (Retrieval-Augmented Generation).

## Tech Stack
- **Framework**: FastAPI + uvicorn
- **LLM**: Ollama with qwen2.5 (multilingual support)
- **Embeddings**: Ollama with nomic-embed-text
- **Vector DB**: ChromaDB (persistent storage)
- **Python**: 3.9+ with typing module for type hints

## Project Structure
```
heritage_ai/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── core/
│   │   ├── config.py        # Settings (pydantic-settings)
│   │   ├── ingest.py        # RAG ingestion pipeline
│   │   ├── retriever.py     # ChromaDB semantic search
│   │   ├── llm.py           # Ollama LLM wrapper
│   │   └── prompts.py       # System prompts and persona
│   ├── api/
│   │   └── routes.py        # API endpoints
│   ├── schemas/
│   │   └── chat.py          # Pydantic models
│   └── services/
│       └── chat_service.py  # Business logic
├── data/                    # Memory documents (markdown)
│   ├── stories/             # Life stories
│   ├── recipes/             # Family recipes
│   └── wisdom/              # Yiddish phrases, life lessons
└── db/                      # ChromaDB persistence (gitignored)
```

## Key Design Decisions

### Similarity Threshold
When ChromaDB returns results with similarity < 0.5, the system switches to "General Warmth" mode - responding warmly without inventing memories.

### Conversation History
Sessions store last 6 messages (3 exchanges) for follow-up questions. Sessions are in-memory (dict keyed by session_id).

### Persona System Prompt
The Savta persona uses Yiddish endearments, shares wisdom through stories, and expresses love through food.

## Running the Application
```bash
# Prerequisites
ollama serve
ollama pull qwen2.5
ollama pull nomic-embed-text

# Start
cd heritage_ai
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Ingest memories
curl -X POST http://localhost:8000/ingest

# Chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about your chicken soup"}'
```

## API Endpoints
- `POST /chat` - Chat with Savta
- `POST /ingest` - Ingest memory documents
- `GET /health` - System health check
- `GET /docs` - Swagger UI

## Development Notes
- All imports are absolute (`from app.core.config import settings`)
- Singletons used for LLM, retriever, and chat_service
- No external APIs - all processing is local via Ollama
