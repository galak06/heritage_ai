import logging
from pathlib import Path

import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings

from app.core.config import settings

logger = logging.getLogger(__name__)


def load_documents_from_directory(data_path: Path) -> list[dict]:
    """Load all markdown files from data directory with metadata."""
    documents = []

    for category_dir in data_path.iterdir():
        if not category_dir.is_dir():
            continue

        category = category_dir.name  # stories, recipes, wisdom

        for file_path in category_dir.glob("*.md"):
            content = file_path.read_text(encoding="utf-8")
            documents.append({
                "content": content,
                "metadata": {
                    "category": category,
                    "source": file_path.name,
                    "title": file_path.stem.replace("_", " ").title(),
                },
            })
            logger.info(f"Loaded: {category}/{file_path.name}")

    return documents


def chunk_documents(documents: list[dict]) -> list[dict]:
    """Split documents into chunks while preserving metadata."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = []
    for doc in documents:
        splits = text_splitter.split_text(doc["content"])
        for i, split in enumerate(splits):
            chunks.append({
                "content": split,
                "metadata": {
                    **doc["metadata"],
                    "chunk_index": i,
                },
            })

    return chunks


def ingest_memories() -> dict:
    """Main ingestion pipeline: load, chunk, embed, and store memories."""
    data_path = settings.data_path

    if not data_path.exists():
        return {
            "success": False,
            "error": f"Data directory not found: {data_path}",
            "chunks_created": 0,
        }

    # Load documents
    documents = load_documents_from_directory(data_path)
    if not documents:
        return {
            "success": False,
            "error": "No markdown files found in data directory",
            "chunks_created": 0,
        }

    # Chunk documents
    chunks = chunk_documents(documents)
    logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents")

    # Initialize embeddings
    embeddings = OllamaEmbeddings(
        base_url=settings.ollama_base_url,
        model=settings.ollama_embedding_model,
    )

    # Initialize ChromaDB
    settings.chroma_path.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(settings.chroma_path))

    # Delete existing collection if it exists
    try:
        client.delete_collection(settings.chroma_collection_name)
        logger.info(f"Deleted existing collection: {settings.chroma_collection_name}")
    except Exception:
        pass  # Collection doesn't exist

    # Create new collection
    collection = client.create_collection(
        name=settings.chroma_collection_name,
        metadata={"hnsw:space": "cosine"},
    )

    # Embed and store chunks
    for i, chunk in enumerate(chunks):
        embedding = embeddings.embed_query(chunk["content"])
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk["content"]],
            metadatas=[chunk["metadata"]],
        )

    logger.info(f"Stored {len(chunks)} chunks in ChromaDB")

    return {
        "success": True,
        "chunks_created": len(chunks),
        "documents_processed": len(documents),
        "categories": list({d["metadata"]["category"] for d in documents}),
    }
