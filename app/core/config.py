from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM Provider: "gemini" or "ollama"
    llm_provider: str = "gemini"

    # Gemini settings
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"

    # Ollama settings (fallback)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "mistral"
    ollama_embedding_model: str = "nomic-embed-text"

    # ChromaDB settings
    chroma_persist_dir: str = "db/savta_collection"
    chroma_collection_name: str = "savta_memories"

    # RAG settings
    similarity_threshold: float = 0.5
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k_results: int = 3

    # Conversation settings
    max_history_length: int = 6  # 3 exchanges (user + assistant each)
    max_response_tokens: int = 150  # Limit response length - short like real conversation
    ollama_timeout: int = 60  # Timeout in seconds

    # Data paths
    data_dir: str = "data/hadassa"

    @property
    def data_path(self) -> Path:
        return Path(self.data_dir)

    @property
    def chroma_path(self) -> Path:
        return Path(self.chroma_persist_dir)


settings = Settings()
