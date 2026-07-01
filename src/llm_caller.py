"""
Interface pour appeler différents LLMs et récupérer les réponses.
"""

import time
import json
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from config import (
    OPENAI_API_KEY, 
    ANTHROPIC_API_KEY,
    MAX_RETRIES, 
    TIMEOUT_SECONDS,
    DEBUG,
    LLM_MODELS,
)


class LLMInterface(ABC):
    """Interface abstraite pour les appels LLM."""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.max_retries = MAX_RETRIES
        self.timeout = TIMEOUT_SECONDS
    
    @abstractmethod
    def call(self, prompt: str) -> str:
        """Appelle le LLM et retourne la réponse."""
        pass
    
    def _retry_with_backoff(self, func, *args, **kwargs) -> Any:
        """Retry avec backoff exponentiel."""
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                wait_time = 2 ** attempt
                if DEBUG:
                    print(f"[WARN] Tentative {attempt+1} échouée, attente {wait_time}s...")
                time.sleep(wait_time)


class OpenAILLM(LLMInterface):
    """Interface pour ChatGPT/GPT-4 via OpenAI API."""
    
    def __init__(self, model_name: str = "gpt-4-turbo-preview"):
        super().__init__(model_name)
        if not OPENAI_API_KEY:
            self.client = None
            return
        
        try:
            import openai
            self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        except ImportError:
            raise ImportError("openai library non installée")
    
    def call(self, prompt: str) -> str:
        """Appelle ChatGPT/GPT-4."""
        if self.client is None:
            raise ValueError("OPENAI_API_KEY non définie")
        def _call():
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a C code generation assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000,
                timeout=self.timeout,
            )
            return response.choices[0].message.content
        
        return self._retry_with_backoff(_call)


class AnthropicLLM(LLMInterface):
    """Interface pour Claude via Anthropic API."""
    
    def __init__(self, model_name: str = "claude-3-haiku"):
        super().__init__(model_name)
        if not ANTHROPIC_API_KEY:
            self.client = None
            return
        
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        except ImportError:
            raise ImportError("anthropic library non installée")
    
    def call(self, prompt: str) -> str:
        """Appelle Claude."""
        if self.client is None:
            raise ValueError("ANTHROPIC_API_KEY non définie")
        def _call():
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        
        return self._retry_with_backoff(_call)


class MockLLM(LLMInterface):
    """LLM de test pour développement (retourne un code dummy)."""
    
    def call(self, prompt: str) -> str:
        """Retourne une réponse simulée."""
        if "size_t" in prompt.lower():
            return "size_t w, h;"
        else:
            return "int w, h;"


class LLMCaller:
    """Orchestrateur pour appeler plusieurs LLMs."""
    
    def __init__(self, models: Dict[str, str] = None):
        """
        Args:
            models: Dict {provider: model_name}
                   Ex: {"openai": "gpt-4", "claude": "claude-3"}
        """
        self.models = models or LLM_MODELS
        self.clients = {}
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialise les clients LLM disponibles."""
        for provider, model_name in self.models.items():
            try:
                if provider.lower() == "openai":
                    client = OpenAILLM(model_name)
                elif provider.lower() == "claude" or provider.lower() == "anthropic":
                    client = AnthropicLLM(model_name)
                elif provider.lower() == "mock":
                    client = MockLLM(model_name)
                else:
                    print(f"[WARN] Provider {provider} non supporté")
                    continue

                if isinstance(client, LLMInterface) and getattr(client, 'client', None) is None and provider.lower() in ["openai", "claude", "anthropic"]:
                    print(f"[WARN] Clé API manquante pour {provider} : le provider sera ignoré.")
                    continue

                self.clients[provider] = client
            except Exception as e:
                print(f"[X] Erreur initialisation {provider}: {e}")
    
    def call_all(self, prompt: str) -> Dict[str, str]:
        """
        Appelle tous les LLMs disponibles avec le même prompt.
        
        Returns:
            {provider: response_text}
        """
        results = {}
        for provider, client in self.clients.items():
            try:
                if DEBUG:
                    print(f"[INFO] Appel {provider}...")
                response = client.call(prompt)
                results[provider] = response
                if DEBUG:
                    print(f"[OK] {provider} répondu")
            except Exception as e:
                print(f"[X] Erreur {provider}: {e}")
                results[provider] = None
        
        return results
    
    def call_one(self, prompt: str, provider: str) -> str:
        """Appelle un seul LLM."""
        if provider not in self.clients:
            raise ValueError(f"Provider {provider} non disponible")
        return self.clients[provider].call(prompt)


def main():
    """Test des LLM calllers."""
    
    # Test avec mode mock (développement)
    print("[INFO] Test LLM Caller (Mode Mock)\n")
    
    mock_llm = MockLLM("mock")
    test_prompt = "Replace <MASK> in: struct img { <MASK> int h; }"
    
    response = mock_llm.call(test_prompt)
    print(f"Input: {test_prompt}")
    print(f"Output: {response}")


if __name__ == "__main__":
    main()
