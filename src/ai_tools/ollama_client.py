"""
Ollama Client - Wrapper for local AI model interactions
Supports Granite and other Ollama models
"""

import os
import json
import requests
from typing import Optional, Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for interacting with Ollama API"""

    def __init__(self, host: Optional[str] = None, model: str = "granite-code:3b"):
        """
        Initialize Ollama client

        Args:
            host: Ollama host URL (default: from env or localhost)
            model: Model name to use
        """
        self.host = host or os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = model
        self.base_url = f"{self.host}/api"

    def generate(self, prompt: str, system: Optional[str] = None,
                 stream: bool = False, temperature: float = 0.7,
                 max_tokens: Optional[int] = None) -> str:
        """
        Generate text from prompt

        Args:
            prompt: Input prompt
            system: System message/context
            stream: Whether to stream response
            temperature: Sampling temperature (0-1)
            max_tokens: Max tokens to generate

        Returns:
            Generated text response
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": stream,
                "options": {
                    "temperature": temperature,
                }
            }

            if system:
                payload["system"] = system

            if max_tokens:
                payload["options"]["num_predict"] = max_tokens

            response = requests.post(
                f"{self.base_url}/generate",
                json=payload,
                timeout=120
            )
            response.raise_for_status()

            result = response.json()
            return result.get("response", "")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Ollama API: {e}")
            return f"Error: {str(e)}"

    def chat(self, messages: List[Dict[str, str]], stream: bool = False) -> str:
        """
        Chat with model using conversation history

        Args:
            messages: List of message dicts with 'role' and 'content'
            stream: Whether to stream response

        Returns:
            Model response
        """
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": stream
            }

            response = requests.post(
                f"{self.base_url}/chat",
                json=payload,
                timeout=120
            )
            response.raise_for_status()

            result = response.json()
            return result.get("message", {}).get("content", "")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error in chat: {e}")
            return f"Error: {str(e)}"

    def list_models(self) -> List[str]:
        """
        List available models

        Returns:
            List of model names
        """
        try:
            response = requests.get(f"{self.base_url}/tags")
            response.raise_for_status()
            models = response.json().get("models", [])
            return [m.get("name") for m in models]
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []

    def is_available(self) -> bool:
        """
        Check if Ollama service is available

        Returns:
            True if service is reachable
        """
        try:
            response = requests.get(f"{self.base_url}/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def pull_model(self, model_name: str) -> bool:
        """
        Pull a model from Ollama registry

        Args:
            model_name: Name of model to pull

        Returns:
            True if successful
        """
        try:
            response = requests.post(
                f"{self.base_url}/pull",
                json={"name": model_name},
                timeout=600  # 10 minutes for large models
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error pulling model: {e}")
            return False


if __name__ == "__main__":
    # Test the client
    client = OllamaClient()

    if client.is_available():
        print("✓ Ollama is running")
        print(f"Available models: {client.list_models()}")

        # Test generation
        response = client.generate("Write a haiku about Docker")
        print(f"\nResponse: {response}")
    else:
        print("✗ Ollama is not available")
        print(f"Tried connecting to: {client.host}")
