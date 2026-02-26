# Heritage AI

**Preserving loved ones' memories through AI.**

Heritage AI is a proof-of-concept application that demonstrates how AI can preserve and make interactive the memories of loved ones. Chat with "Savta" (Hebrew for grandmother), a warm and wise Holocaust survivor grandmother whose stories, recipes, and wisdom have been preserved through RAG (Retrieval-Augmented Generation).

## Features

- **RAG-based memory retrieval**: Semantic search finds relevant memories based on your questions
- **Warm persona**: Savta responds with love, Yiddish phrases, and grandmother wisdom
- **Conversation continuity**: Follow-up questions maintain context within a session
- **Privacy-first**: All processing happens locally using Ollama
- **Honest responses**: When no relevant memories exist, Savta responds warmly without inventing details

## Prerequisites

1. **Python 3.12+**
2. **Ollama** installed and running:
   ```bash
   # Install (macOS)
   brew install ollama

   # Start Ollama
   ollama serve

   # Pull required models
   ollama pull llama3.2
   ollama pull nomic-embed-text
   ```

## Quick Start

```bash
# Clone and enter directory
cd heritage_ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --port 8000
```

## Usage

### 1. Ingest Memories

First, ingest the memory documents into ChromaDB:

```bash
curl -X POST http://localhost:8000/ingest
```

Response:
```json
{
  "success": true,
  "chunks_created": 42,
  "documents_processed": 8,
  "categories": ["stories", "recipes", "wisdom"]
}
```

### 2. Chat with Savta

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about your chicken soup"}'
```

Response:
```json
{
  "response": "Ah, mayn kind, you want to know about my chicken soup? This soup is not just food...",
  "session_id": "abc123",
  "sources_found": true,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 3. Follow-up Questions

Use the `session_id` from the previous response for conversation continuity:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Who taught you that recipe?", "session_id": "abc123"}'
```

### 4. Check System Health

```bash
curl http://localhost:8000/health
```

## API Documentation

Visit `http://localhost:8000/docs` for the interactive Swagger UI documentation.

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /chat | Chat with Savta |
| POST | /ingest | Ingest memory documents |
| GET | /health | Check system health |
| GET | /docs | Swagger documentation |

## Project Structure

```
heritage_ai/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── core/
│   │   ├── config.py        # Configuration settings
│   │   ├── ingest.py        # Memory ingestion pipeline
│   │   ├── retriever.py     # Semantic search
│   │   ├── llm.py           # Ollama wrapper
│   │   └── prompts.py       # Persona prompts
│   ├── api/
│   │   └── routes.py        # API endpoints
│   ├── schemas/
│   │   └── chat.py          # Request/response models
│   └── services/
│       └── chat_service.py  # Business logic
├── data/
│   ├── stories/             # Life stories
│   ├── recipes/             # Family recipes
│   └── wisdom/              # Yiddish phrases, life lessons
└── db/                      # ChromaDB storage (gitignored)
```

## Adding Your Own Memories

To add new memories:

1. Create markdown files in the appropriate `data/` subdirectory
2. Run the ingest endpoint: `curl -X POST http://localhost:8000/ingest`
3. The new memories will be available for chat

## Configuration

Environment variables (or `.env` file):

| Variable | Default | Description |
|----------|---------|-------------|
| OLLAMA_BASE_URL | http://localhost:11434 | Ollama server URL |
| OLLAMA_MODEL | llama3.2 | LLM model for generation |
| OLLAMA_EMBEDDING_MODEL | nomic-embed-text | Model for embeddings |
| SIMILARITY_THRESHOLD | 0.5 | Minimum similarity for relevant results |

## License

MIT
