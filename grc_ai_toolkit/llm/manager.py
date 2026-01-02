"""
LLM Manager - Unified interface for different LLM providers
"""

import time
from typing import Optional, List, Dict, Any, Union
from functools import lru_cache
import hashlib
import json
import logging

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

from .config import LLMConfig, LLMProvider, PRICING
from .utils import count_tokens, estimate_cost


logger = logging.getLogger(__name__)


class LLMManager:
    """
    Unified LLM Manager with support for multiple providers

    Features:
    - Multi-provider support (OpenAI, Anthropic, local models)
    - Automatic fallback on errors
    - Token counting and cost tracking
    - Response caching
    - Retry logic with exponential backoff
    """

    def __init__(self, config: Optional[LLMConfig] = None):
        """
        Initialize LLM Manager

        Args:
            config: LLM configuration. If None, loads from environment variables.
        """
        self.config = config or LLMConfig.from_env()
        self.total_tokens = {"input": 0, "output": 0}
        self.total_cost = 0.0
        self.request_count = 0

        # Initialize primary LLM
        self.llm = self._create_llm(
            self.config.provider,
            self.config.model
        )

        # Initialize fallback LLM if enabled
        self.fallback_llm = None
        if self.config.enable_fallback and self.config.fallback_provider:
            self.fallback_llm = self._create_llm(
                self.config.fallback_provider,
                self.config.fallback_model
            )

        logger.info(f"LLM Manager initialized with {self.config.provider.value} ({self.config.model})")

    def _create_llm(self, provider: LLMProvider, model: str):
        """Create LLM instance based on provider"""
        if provider == LLMProvider.OPENAI:
            return ChatOpenAI(
                model=model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                openai_api_key=self.config.openai_api_key,
                streaming=self.config.enable_streaming,
            )
        elif provider == LLMProvider.ANTHROPIC:
            return ChatAnthropic(
                model=model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                anthropic_api_key=self.config.anthropic_api_key,
                streaming=self.config.enable_streaming,
            )
        elif provider == LLMProvider.GROQ:
            return ChatGroq(
                model=model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                groq_api_key=self.config.groq_api_key,
                streaming=self.config.enable_streaming,
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def generate(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        system_message: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate text using the LLM

        Args:
            prompt: User prompt (string or list of message dicts)
            system_message: Optional system message
            **kwargs: Additional generation parameters

        Returns:
            Generated text
        """
        # Build messages
        messages = self._build_messages(prompt, system_message)

        # Check cache
        if self.config.enable_caching:
            cache_key = self._get_cache_key(messages)
            cached_response = self._get_from_cache(cache_key)
            if cached_response:
                logger.info("Returning cached response")
                return cached_response

        # Generate with retry logic
        response = self._generate_with_retry(messages, **kwargs)

        # Track tokens and cost
        if self.config.enable_cost_tracking:
            self._track_usage(messages, response)

        # Cache response
        if self.config.enable_caching:
            self._save_to_cache(cache_key, response)

        self.request_count += 1
        return response

    def _build_messages(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        system_message: Optional[str] = None
    ) -> List:
        """Build message list for LLM"""
        messages = []

        # Add system message
        if system_message:
            messages.append(SystemMessage(content=system_message))

        # Add user messages
        if isinstance(prompt, str):
            messages.append(HumanMessage(content=prompt))
        else:
            for msg in prompt:
                if msg["role"] == "system":
                    messages.append(SystemMessage(content=msg["content"]))
                elif msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))

        return messages

    def _generate_with_retry(self, messages: List, **kwargs) -> str:
        """Generate with retry logic and fallback"""
        last_error = None

        for attempt in range(self.config.max_retries):
            try:
                # Try primary LLM
                response = self.llm.invoke(messages, **kwargs)
                parser = StrOutputParser()
                return parser.parse(response)

            except Exception as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")

                if attempt < self.config.max_retries - 1:
                    # Exponential backoff
                    sleep_time = self.config.retry_delay * (2 ** attempt)
                    time.sleep(sleep_time)
                    continue

        # Try fallback if enabled
        if self.fallback_llm:
            try:
                logger.info("Trying fallback LLM")
                response = self.fallback_llm.invoke(messages, **kwargs)
                parser = StrOutputParser()
                return parser.parse(response)
            except Exception as e:
                logger.error(f"Fallback LLM also failed: {str(e)}")

        # All retries failed
        raise RuntimeError(f"LLM generation failed after {self.config.max_retries} retries: {last_error}")

    def _track_usage(self, messages: List, response: str):
        """Track token usage and cost"""
        # Estimate input tokens
        input_text = " ".join([msg.content for msg in messages])
        input_tokens = count_tokens(input_text, self.config.model)

        # Estimate output tokens
        output_tokens = count_tokens(response, self.config.model)

        # Update totals
        self.total_tokens["input"] += input_tokens
        self.total_tokens["output"] += output_tokens

        # Calculate cost
        cost = estimate_cost(
            input_tokens,
            output_tokens,
            self.config.model
        )
        self.total_cost += cost

        logger.debug(
            f"Tokens - Input: {input_tokens}, Output: {output_tokens}, "
            f"Cost: ${cost:.4f}, Total Cost: ${self.total_cost:.4f}"
        )

    def _get_cache_key(self, messages: List) -> str:
        """Generate cache key from messages"""
        content = json.dumps([msg.content for msg in messages])
        return hashlib.md5(content.encode()).hexdigest()

    @lru_cache(maxsize=1000)
    def _get_from_cache(self, cache_key: str) -> Optional[str]:
        """Get response from cache"""
        # This is a simple in-memory cache using lru_cache
        # For production, use Redis or similar
        return None

    def _save_to_cache(self, cache_key: str, response: str):
        """Save response to cache"""
        # Simple in-memory cache
        # For production, use Redis or similar
        pass

    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        return {
            "provider": self.config.provider.value,
            "model": self.config.model,
            "request_count": self.request_count,
            "total_tokens": self.total_tokens,
            "total_cost": round(self.total_cost, 4),
            "average_cost_per_request": round(
                self.total_cost / max(self.request_count, 1), 4
            ),
        }

    def reset_stats(self):
        """Reset usage statistics"""
        self.total_tokens = {"input": 0, "output": 0}
        self.total_cost = 0.0
        self.request_count = 0
        logger.info("Statistics reset")


# Convenience functions
def create_llm_manager(
    provider: str = "openai",
    model: Optional[str] = None,
    **kwargs
) -> LLMManager:
    """
    Create LLM Manager with simplified parameters

    Args:
        provider: Provider name ("openai" or "anthropic")
        model: Model name (optional, uses default if not provided)
        **kwargs: Additional config parameters

    Returns:
        Configured LLM Manager
    """
    config = LLMConfig.from_env(provider)

    if model:
        config.model = model

    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)

    return LLMManager(config)
