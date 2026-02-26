import logging
import time
from typing import Dict, List, Optional

import ollama

from app.core.config import settings
from app.core.prompts import build_persona_prompt

logger = logging.getLogger(__name__)


class SavtaLLM:
    """Wrapper for Ollama LLM with Savta persona."""

    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = ollama.Client(host=settings.ollama_base_url)
        return self._client

    def generate_response(
        self,
        user_message: str,
        context: str,
        has_relevant_memories: bool,
        conversation_history: Optional[List[Dict]] = None,
    ) -> str:
        """
        Generate a response as Savta persona.

        Args:
            user_message: The user's question
            context: Retrieved memory context
            has_relevant_memories: Whether relevant memories were found
            conversation_history: Previous messages in the conversation

        Returns:
            Savta's response as a string
        """
        # Build system prompt
        system_prompt = build_persona_prompt(context, has_relevant_memories)

        # Build messages array
        messages = [{"role": "system", "content": system_prompt}]

        # Add conversation history if provided
        if conversation_history:
            # Limit to max history length
            history_to_add = conversation_history[-settings.max_history_length :]
            messages.extend(history_to_add)

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        # Generate response
        try:
            logger.info(f"Generating response for: {user_message[:50]}...")
            logger.debug(f"Context length: {len(context)} chars, History: {len(conversation_history or [])} messages")

            start_time = time.time()
            response = self.client.chat(
                model=settings.ollama_model,
                messages=messages,
                options={"num_predict": settings.max_response_tokens},
            )
            elapsed = time.time() - start_time

            content = response["message"]["content"]
            logger.info(f"Response generated in {elapsed:.2f}s ({len(content)} chars)")
            return content
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

    def is_available(self) -> bool:
        """Check if Ollama is available and the model is loaded."""
        try:
            response = self.client.list()
            # Handle both old dict format and new object format
            if hasattr(response, 'models'):
                model_names = [m.model for m in response.models]
            else:
                model_names = [m.get("name", m.get("model", "")) for m in response.get("models", [])]
            return any(
                settings.ollama_model in name or name.startswith(settings.ollama_model)
                for name in model_names
            )
        except Exception as e:
            logger.error(f"Error checking Ollama availability: {e}")
            return False


# Singleton instance
llm = SavtaLLM()
