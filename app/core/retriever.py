import logging

import chromadb
from langchain_ollama import OllamaEmbeddings

from app.core.config import settings

logger = logging.getLogger(__name__)


class MemoryRetriever:
    """Retrieves relevant memories from ChromaDB using semantic search."""

    def __init__(self):
        self._client = None
        self._collection = None
        self._embeddings = None

    @property
    def client(self):
        if self._client is None:
            self._client = chromadb.PersistentClient(path=str(settings.chroma_path))
        return self._client

    @property
    def collection(self):
        if self._collection is None:
            try:
                self._collection = self.client.get_collection(settings.chroma_collection_name)
            except ValueError:
                logger.warning(f"Collection {settings.chroma_collection_name} not found. Run /ingest first.")
                return None
        return self._collection

    @property
    def embeddings(self):
        if self._embeddings is None:
            self._embeddings = OllamaEmbeddings(
                base_url=settings.ollama_base_url,
                model=settings.ollama_embedding_model,
            )
        return self._embeddings

    def search(self, query: str) -> dict:
        """
        Search for relevant memories based on the query.

        Returns:
            dict with:
                - context: str - Combined text from relevant memories
                - has_relevant_memories: bool - Whether good matches were found
                - sources: list - Source documents that contributed
        """
        if self.collection is None:
            return {
                "context": "",
                "has_relevant_memories": False,
                "sources": [],
            }

        # Embed query
        query_embedding = self.embeddings.embed_query(query)

        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=settings.top_k_results,
            include=["documents", "metadatas", "distances"],
        )

        # Process results
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        relevant_docs = []
        sources = []

        for doc, meta, dist in zip(documents, metadatas, distances):
            similarity = 1 - dist  # Convert distance to similarity
            if similarity >= settings.similarity_threshold:
                relevant_docs.append(doc)
                sources.append({
                    "title": meta.get("title", "Unknown"),
                    "category": meta.get("category", "Unknown"),
                    "similarity": round(similarity, 3),
                })
                logger.debug(f"Match: {meta.get('title')} (similarity: {similarity:.3f})")
            else:
                logger.debug(f"Below threshold: {meta.get('title')} (similarity: {similarity:.3f})")

        context = "\n\n---\n\n".join(relevant_docs) if relevant_docs else ""

        return {
            "context": context,
            "has_relevant_memories": bool(relevant_docs),
            "sources": sources,
        }

    def is_ready(self) -> bool:
        """Check if the retriever is ready (collection exists and has documents)."""
        try:
            if self.collection is None:
                return False
            return self.collection.count() > 0
        except Exception:
            return False

    def reset_collection(self):
        """Reset the collection reference - call after ingest."""
        self._collection = None


# Singleton instance
retriever = MemoryRetriever()
