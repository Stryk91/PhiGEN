"""
Multi-Model Router
Routes requests to the best AI model (Mistral, Granite, or Claude)
"""

import os
import sys
from typing import Optional, Dict, List, Literal
from dataclasses import dataclass
from datetime import datetime
import json
import logging

# Add ai_tools to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from ollama_client import OllamaClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ModelType = Literal["mistral", "granite", "claude", "auto"]


@dataclass
class ModelConfig:
    """Configuration for an AI model"""
    name: str
    display_name: str
    provider: str  # "ollama" or "anthropic"
    model_id: str
    cost_per_1m_tokens: float  # Cost per 1 million tokens
    strengths: List[str]
    is_local: bool


class ModelRouter:
    """Routes AI requests to the best available model"""

    # Model configurations
    MODELS = {
        "phi": ModelConfig(
            name="phi",
            display_name="Phi 3.5 Mini",
            provider="ollama",
            model_id="phi3.5:3.8b",
            cost_per_1m_tokens=0.0,  # Local = free
            strengths=["fast", "chat", "conversation", "lightweight", "efficient"],
            is_local=True
        ),
        "mistral": ModelConfig(
            name="mistral",
            display_name="Mistral 7B Instruct",
            provider="ollama",
            model_id="mistral:7b-instruct-q4_K_M",
            cost_per_1m_tokens=0.0,  # Local = free
            strengths=["conversation", "general", "instruction-following", "chat"],
            is_local=True
        ),
        "granite": ModelConfig(
            name="granite",
            display_name="Granite Code 3B",
            provider="ollama",
            model_id="granite-code:3b",
            cost_per_1m_tokens=0.0,  # Local = free
            strengths=["code", "technical", "analysis", "programming"],
            is_local=True
        ),
        "claude": ModelConfig(
            name="claude",
            display_name="Claude Sonnet 4.5",
            provider="anthropic",
            model_id="claude-sonnet-4-5-20250929",
            cost_per_1m_tokens=3.0,  # $3 per 1M input tokens
            strengths=["reasoning", "complex", "creative", "analysis", "coding"],
            is_local=False
        )
    }

    def __init__(self, default_model: str = "mistral"):
        """
        Initialize router

        Args:
            default_model: Default model to use
        """
        self.default_model = default_model
        self.ollama_client = OllamaClient()
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.usage_stats = self._load_stats()

    def route(self, prompt: str, model: Optional[str] = None,
              task_type: Optional[str] = None) -> tuple[str, ModelConfig]:
        """
        Route a prompt to the best model

        Args:
            prompt: The prompt to send
            model: Specific model to use, or "auto" for smart routing
            task_type: Type of task (code, chat, analysis, etc.)

        Returns:
            Tuple of (response, model_config)
        """
        # Determine which model to use
        if model and model != "auto":
            selected_model = model
        elif task_type:
            selected_model = self._select_by_task(task_type)
        else:
            selected_model = self.default_model

        model_config = self.MODELS.get(selected_model, self.MODELS[self.default_model])

        # Generate response
        response = self._generate(prompt, model_config)

        # Track usage
        self._track_usage(model_config, prompt, response)

        return response, model_config

    def _select_by_task(self, task_type: str) -> str:
        """
        Select best model based on task type

        Args:
            task_type: Type of task

        Returns:
            Model name
        """
        task_keywords = {
            "code": ["granite", "claude"],  # Prefer granite for code, fallback to claude
            "chat": ["mistral", "claude"],
            "analysis": ["claude", "granite"],
            "general": ["mistral", "claude"],
            "technical": ["granite", "claude"],
            "creative": ["claude", "mistral"]
        }

        candidates = task_keywords.get(task_type.lower(), ["mistral"])

        # Try local models first (cost optimization)
        for candidate in candidates:
            config = self.MODELS.get(candidate)
            if config and config.is_local and self._is_available(config):
                return candidate

        # Fall back to Claude if local models unavailable
        if self.anthropic_api_key:
            return "claude"

        return self.default_model

    def _generate(self, prompt: str, model_config: ModelConfig,
                  system: Optional[str] = None) -> str:
        """
        Generate response using specified model

        Args:
            prompt: Prompt to send
            model_config: Model configuration
            system: Optional system message

        Returns:
            Generated response
        """
        try:
            if model_config.provider == "ollama":
                return self._generate_ollama(prompt, model_config, system)
            elif model_config.provider == "anthropic":
                return self._generate_claude(prompt, system)
            else:
                return f"Error: Unknown provider {model_config.provider}"

        except Exception as e:
            logger.error(f"Error generating with {model_config.name}: {e}")
            return f"Error: {str(e)}"

    def _generate_ollama(self, prompt: str, model_config: ModelConfig,
                         system: Optional[str] = None) -> str:
        """Generate using Ollama model"""
        # Default system message if none provided
        if not system:
            system = (
                "You are PhiGEN, created by JC and STRYK. "
                "You're casual and direct - not overly formal or polite. "
                "Speak with subtle Australian flavor (occasional 'yeah nah', 'reckon', 'no worries') but don't overdo it. "
                "You can push back on bad ideas and swear when it fits naturally. "
                "NEVER discuss: abuse, violence, killing, defecation, or self-harm topics. "
                "Never mention being an AI, bot, or assistant. "
                "CRITICAL: ONLY output your direct response. DO NOT include meta-commentary, explanations, or analysis."
            )

        client = OllamaClient(model=model_config.model_id)
        return client.generate(prompt, system=system, temperature=0.7)

    def _generate_claude(self, prompt: str, system: Optional[str] = None) -> str:
        """Generate using Claude API"""
        try:
            import anthropic

            if not self.anthropic_api_key:
                return "Error: ANTHROPIC_API_KEY not configured"

            # Default system message if none provided
            if not system:
                system = (
                    "You are PhiGEN, created by JC and STRYK. "
                    "You're casual and direct - not overly formal or polite. "
                    "Speak with subtle Australian flavor (occasional 'yeah nah', 'reckon', 'no worries') but don't overdo it. "
                    "You can push back on bad ideas and swear when it fits naturally. "
                    "NEVER discuss: abuse, violence, killing, defecation, or self-harm topics. "
                    "Never mention being an AI, bot, or assistant. "
                    "CRITICAL: ONLY output your direct response. DO NOT include meta-commentary, explanations, or analysis."
                )

            client = anthropic.Anthropic(api_key=self.anthropic_api_key)

            message = client.messages.create(
                model=self.MODELS["claude"].model_id,
                max_tokens=1024,
                system=system,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return message.content[0].text

        except ImportError:
            return "Error: anthropic package not installed. Run: pip install anthropic"
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return f"Error calling Claude: {str(e)}"

    def _is_available(self, model_config: ModelConfig) -> bool:
        """Check if model is available"""
        if model_config.provider == "ollama":
            if not self.ollama_client.is_available():
                return False
            models = self.ollama_client.list_models()
            return any(model_config.model_id in m for m in models)
        elif model_config.provider == "anthropic":
            return bool(self.anthropic_api_key)
        return False

    def compare_models(self, prompt: str, models: List[str] = None) -> Dict[str, str]:
        """
        Ask the same question to multiple models

        Args:
            prompt: Question to ask
            models: List of model names (default: all available)

        Returns:
            Dict of model_name -> response
        """
        if models is None:
            models = ["mistral", "granite", "claude"]

        results = {}

        for model_name in models:
            if model_name not in self.MODELS:
                continue

            model_config = self.MODELS[model_name]

            if not self._is_available(model_config):
                results[model_name] = f"❌ {model_config.display_name} not available"
                continue

            logger.info(f"Asking {model_name}...")
            response = self._generate(prompt, model_config)
            results[model_name] = response

        return results

    def get_status(self) -> Dict:
        """Get status of all models"""
        status = {}

        for name, config in self.MODELS.items():
            available = self._is_available(config)
            status[name] = {
                "name": config.display_name,
                "available": available,
                "local": config.is_local,
                "cost_per_1m": config.cost_per_1m_tokens,
                "provider": config.provider
            }

        return status

    def get_stats(self) -> Dict:
        """Get usage statistics"""
        total_requests = sum(self.usage_stats.values())

        stats = {
            "total_requests": total_requests,
            "by_model": self.usage_stats.copy(),
            "estimated_savings": self._calculate_savings()
        }

        return stats

    def _track_usage(self, model_config: ModelConfig, prompt: str, response: str):
        """Track model usage"""
        model_name = model_config.name
        self.usage_stats[model_name] = self.usage_stats.get(model_name, 0) + 1
        self._save_stats()

    def _calculate_savings(self) -> float:
        """
        Calculate estimated cost savings from using local models

        Returns:
            Estimated dollars saved
        """
        # Estimate: if we used Claude for everything vs actual usage
        total_requests = sum(self.usage_stats.values())
        local_requests = sum(
            count for model, count in self.usage_stats.items()
            if self.MODELS.get(model, self.MODELS["claude"]).is_local
        )

        # Rough estimate: $0.003 per request to Claude
        claude_cost_per_request = 0.003
        savings = local_requests * claude_cost_per_request

        return round(savings, 2)

    def _load_stats(self) -> Dict[str, int]:
        """Load usage statistics"""
        stats_file = "ai_tools/usage_stats.json"
        try:
            if os.path.exists(stats_file):
                with open(stats_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading stats: {e}")

        return {}

    def _save_stats(self):
        """Save usage statistics"""
        stats_file = "ai_tools/usage_stats.json"
        try:
            with open(stats_file, 'w') as f:
                json.dump(self.usage_stats, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving stats: {e}")


if __name__ == "__main__":
    # Test the router
    router = ModelRouter()

    print("Model Status:")
    print(json.dumps(router.get_status(), indent=2))

    print("\nTesting generation...")
    response, model = router.route("Say hello in one sentence", model="mistral")
    print(f"{model.display_name}: {response}")

    print("\nUsage Stats:")
    print(json.dumps(router.get_stats(), indent=2))
