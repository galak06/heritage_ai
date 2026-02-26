import logging
from typing import Dict, List, Optional
from uuid import uuid4

from app.core.config import settings
from app.core.llm import llm
from app.core.retriever import retriever

logger = logging.getLogger(__name__)


class ChatService:
    """Service for managing chat sessions and generating responses."""

    def __init__(self):
        # In-memory session storage: session_id -> list of messages
        self._sessions: Dict[str, List[Dict]] = {}

    def get_or_create_session(self, session_id: Optional[str]) -> str:
        """Get existing session or create a new one."""
        if session_id and session_id in self._sessions:
            return session_id

        new_session_id = str(uuid4())
        self._sessions[new_session_id] = []
        logger.info(f"Created new session: {new_session_id}")
        return new_session_id

    def get_conversation_history(self, session_id: str) -> List[Dict]:
        """Get conversation history for a session."""
        return self._sessions.get(session_id, [])

    def add_to_history(self, session_id: str, role: str, content: str):
        """Add a message to the conversation history."""
        if session_id not in self._sessions:
            self._sessions[session_id] = []

        self._sessions[session_id].append({"role": role, "content": content})

        # Trim history to max length
        if len(self._sessions[session_id]) > settings.max_history_length:
            self._sessions[session_id] = self._sessions[session_id][-settings.max_history_length :]

    def chat(self, message: str, session_id: Optional[str] = None) -> Dict:
        """
        Process a chat message and return Savta's response.

        Args:
            message: The user's message
            session_id: Optional session ID for continuity

        Returns:
            dict with response, session_id, and sources_found
        """
        # Get or create session
        session_id = self.get_or_create_session(session_id)

        # Retrieve relevant memories
        retrieval_result = retriever.search(message)
        context = retrieval_result["context"]
        has_relevant_memories = retrieval_result["has_relevant_memories"]
        sources = retrieval_result["sources"]

        logger.info(
            f"Retrieved {len(sources)} relevant memories for query: {message[:50]}..."
        )

        # Get conversation history
        history = self.get_conversation_history(session_id)

        # Generate response
        response = llm.generate_response(
            user_message=message,
            context=context,
            has_relevant_memories=has_relevant_memories,
            conversation_history=history,
        )

        # Update conversation history
        self.add_to_history(session_id, "user", message)
        self.add_to_history(session_id, "assistant", response)

        return {
            "response": response,
            "session_id": session_id,
            "sources_found": has_relevant_memories,
        }


# Singleton instance
chat_service = ChatService()
