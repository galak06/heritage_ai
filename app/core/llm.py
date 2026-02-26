import logging
import time
from typing import Dict, List, Optional

from app.core.config import settings
from app.core.prompts import build_persona_prompt

logger = logging.getLogger(__name__)


class SavtaLLM:
    """Wrapper for LLM with Savta persona. Supports Gemini and Ollama."""

    def __init__(self):
        self._gemini_client = None
        self._ollama_client = None

    @property
    def gemini_client(self):
        if self._gemini_client is None:
            import google.generativeai as genai
            genai.configure(api_key=settings.gemini_api_key)
            self._gemini_client = genai.GenerativeModel(settings.gemini_model)
        return self._gemini_client

    @property
    def ollama_client(self):
        if self._ollama_client is None:
            import ollama
            self._ollama_client = ollama.Client(
                host=settings.ollama_base_url,
                timeout=settings.ollama_timeout,
            )
        return self._ollama_client

    def generate_response(
        self,
        user_message: str,
        context: str,
        has_relevant_memories: bool,
        conversation_history: Optional[List[Dict]] = None,
    ) -> str:
        """Generate a response as Savta persona."""
        system_prompt = build_persona_prompt(context, has_relevant_memories)

        logger.info(f"Generating response for: {user_message[:50]}...")
        logger.debug(f"Context length: {len(context)} chars, History: {len(conversation_history or [])} messages")
        start_time = time.time()

        if settings.llm_provider == "gemini":
            content = self._generate_gemini(system_prompt, user_message, conversation_history)
        else:
            content = self._generate_ollama(system_prompt, user_message, conversation_history)

        elapsed = time.time() - start_time
        logger.info(f"Response generated in {elapsed:.2f}s ({len(content)} chars)")
        return content

    def _generate_gemini(
        self,
        system_prompt: str,
        user_message: str,
        conversation_history: Optional[List[Dict]] = None,
    ) -> str:
        """Generate response using Gemini API."""
        # Build conversation for Gemini
        history = []
        if conversation_history:
            for msg in conversation_history[-settings.max_history_length:]:
                role = "user" if msg["role"] == "user" else "model"
                history.append({"role": role, "parts": [msg["content"]]})

        # Start chat with system instruction
        chat = self.gemini_client.start_chat(history=history)

        # Combine system prompt with user message for first turn
        full_prompt = f"{system_prompt}\n\n---\n\nהודעת המשתמש:\n{user_message}"

        response = chat.send_message(full_prompt)
        return response.text

    def _generate_ollama(
        self,
        system_prompt: str,
        user_message: str,
        conversation_history: Optional[List[Dict]] = None,
    ) -> str:
        """Generate response using Ollama."""
        messages = [{"role": "system", "content": system_prompt}]

        if conversation_history:
            history_to_add = conversation_history[-settings.max_history_length:]
            messages.extend(history_to_add)

        messages.append({"role": "user", "content": user_message})

        response = self.ollama_client.chat(
            model=settings.ollama_model,
            messages=messages,
            options={"num_predict": settings.max_response_tokens},
        )
        return response["message"]["content"]

    def is_available(self) -> bool:
        """Check if the LLM is available."""
        try:
            if settings.llm_provider == "gemini":
                return bool(settings.gemini_api_key)
            else:
                response = self.ollama_client.list()
                if hasattr(response, 'models'):
                    model_names = [m.model for m in response.models]
                else:
                    model_names = [m.get("name", m.get("model", "")) for m in response.get("models", [])]
                return any(
                    settings.ollama_model in name or name.startswith(settings.ollama_model)
                    for name in model_names
                )
        except Exception as e:
            logger.error(f"Error checking LLM availability: {e}")
            return False


# Singleton instance
llm = SavtaLLM()
