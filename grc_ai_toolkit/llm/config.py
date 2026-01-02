"""
LLM Configuration Management
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum


class LLMProvider(str, Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    LOCAL = "local"


class OpenAIModel(str, Enum):
    """OpenAI model options"""
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo-preview"
    GPT_4_O = "gpt-4o"
    GPT_3_5_TURBO = "gpt-3.5-turbo"


class AnthropicModel(str, Enum):
    """Anthropic model options"""
    CLAUDE_SONNET_4 = "claude-sonnet-4-20250514"
    CLAUDE_OPUS_4 = "claude-opus-4-20251101"
    CLAUDE_3_5_SONNET = "claude-3-5-sonnet-20241022"


class GroqModel(str, Enum):
    """Groq model options"""
    LLAMA_3_3_70B_VERSATILE = "llama-3.3-70b-versatile"
    LLAMA_3_1_8B_INSTANT = "llama-3.1-8b-instant"
    LLAMA_4_SCOUT = "llama-4-scout"
    LLAMA_4_MAVERICK = "llama-4-maverick"
    MIXTRAL_8X7B = "mixtral-8x7b-32768"
    GEMMA_7B_IT = "gemma-7b-it"


@dataclass
class LLMConfig:
    """Configuration for LLM providers"""

    # Provider settings
    provider: LLMProvider = LLMProvider.OPENAI
    model: str = OpenAIModel.GPT_4.value

    # API keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None

    # Generation parameters
    temperature: float = 0.7
    max_tokens: int = 2000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0

    # Retry and fallback
    max_retries: int = 3
    retry_delay: float = 1.0
    enable_fallback: bool = True
    fallback_provider: Optional[LLMProvider] = None
    fallback_model: Optional[str] = None

    # Cost and token management
    enable_cost_tracking: bool = True
    max_cost_per_request: Optional[float] = None  # in USD
    enable_caching: bool = True
    cache_ttl: int = 3600  # seconds

    # Streaming
    enable_streaming: bool = False

    # Custom parameters
    extra_params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate configuration"""
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("Temperature must be between 0 and 2")

        if self.max_tokens < 1:
            raise ValueError("max_tokens must be positive")

        if self.provider == LLMProvider.OPENAI and not self.openai_api_key:
            raise ValueError("OpenAI API key is required for OpenAI provider")

        if self.provider == LLMProvider.ANTHROPIC and not self.anthropic_api_key:
            raise ValueError("Anthropic API key is required for Anthropic provider")

        if self.provider == LLMProvider.GROQ and not self.groq_api_key:
            raise ValueError("Groq API key is required for Groq provider")

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "provider": self.provider.value,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "enable_streaming": self.enable_streaming,
            **self.extra_params
        }

    @classmethod
    def from_env(cls, provider: Optional[str] = None) -> "LLMConfig":
        """Create config from environment variables"""
        import os

        provider_enum = LLMProvider(provider) if provider else LLMProvider.OPENAI

        return cls(
            provider=provider_enum,
            model=os.getenv("LLM_MODEL", OpenAIModel.GPT_4.value),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2000")),
            enable_caching=os.getenv("LLM_ENABLE_CACHING", "True").lower() == "true",
            enable_cost_tracking=os.getenv("LLM_ENABLE_COST_TRACKING", "True").lower() == "true",
        )


# Pricing information (per 1M tokens as of Dec 2025)
PRICING = {
    "gpt-4": {"input": 30.0, "output": 60.0},
    "gpt-4-turbo-preview": {"input": 10.0, "output": 30.0},
    "gpt-4o": {"input": 5.0, "output": 15.0},
    "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
    "claude-sonnet-4-20250514": {"input": 3.0, "output": 15.0},
    "claude-opus-4-20251101": {"input": 15.0, "output": 75.0},
    "claude-3-5-sonnet-20241022": {"input": 3.0, "output": 15.0},
    # Groq models (as of Dec 2025)
    "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},
    "llama-3.1-8b-instant": {"input": 0.05, "output": 0.08},
    "llama-4-scout": {"input": 0.11, "output": 0.34},
    "llama-4-maverick": {"input": 0.20, "output": 0.60},
    "mixtral-8x7b-32768": {"input": 0.24, "output": 0.24},
    "gemma-7b-it": {"input": 0.10, "output": 0.10},
}
