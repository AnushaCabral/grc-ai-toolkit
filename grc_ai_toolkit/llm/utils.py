"""
LLM Utility Functions
"""

import tiktoken
from typing import Optional
from .config import PRICING


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """
    Count tokens in text using tiktoken

    Args:
        text: Input text
        model: Model name for encoding

    Returns:
        Number of tokens
    """
    try:
        # Map model names to tiktoken encodings
        encoding_map = {
            "gpt-4": "cl100k_base",
            "gpt-4-turbo-preview": "cl100k_base",
            "gpt-4o": "cl100k_base",
            "gpt-3.5-turbo": "cl100k_base",
            "claude-sonnet-4-20250514": "cl100k_base",  # Approximate
            "claude-opus-4-20251101": "cl100k_base",  # Approximate
            "claude-3-5-sonnet-20241022": "cl100k_base",  # Approximate
            # Groq models (use cl100k_base for approximation)
            "llama-3.3-70b-versatile": "cl100k_base",  # Approximate
            "llama-3.1-8b-instant": "cl100k_base",  # Approximate
            "llama-4-scout": "cl100k_base",  # Approximate
            "llama-4-maverick": "cl100k_base",  # Approximate
            "mixtral-8x7b-32768": "cl100k_base",  # Approximate
            "gemma-7b-it": "cl100k_base",  # Approximate
        }

        encoding_name = encoding_map.get(model, "cl100k_base")
        encoding = tiktoken.get_encoding(encoding_name)
        return len(encoding.encode(text))

    except Exception as e:
        # Fallback to rough estimation (1 token ≈ 4 characters)
        return len(text) // 4


def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    model: str
) -> float:
    """
    Estimate cost of LLM request

    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        model: Model name

    Returns:
        Estimated cost in USD
    """
    if model not in PRICING:
        # Unknown model, return 0
        return 0.0

    pricing = PRICING[model]
    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]

    return input_cost + output_cost


def format_conversation_history(
    messages: list,
    max_messages: Optional[int] = None
) -> list:
    """
    Format conversation history for LLM

    Args:
        messages: List of message dicts with 'role' and 'content'
        max_messages: Maximum number of messages to include (most recent)

    Returns:
        Formatted message list
    """
    if max_messages and len(messages) > max_messages:
        messages = messages[-max_messages:]

    return [
        {"role": msg["role"], "content": msg["content"]}
        for msg in messages
    ]


def truncate_text(
    text: str,
    max_tokens: int,
    model: str = "gpt-4",
    suffix: str = "..."
) -> str:
    """
    Truncate text to fit within token limit

    Args:
        text: Input text
        max_tokens: Maximum number of tokens
        model: Model name for token counting
        suffix: Suffix to add when truncated

    Returns:
        Truncated text
    """
    current_tokens = count_tokens(text, model)

    if current_tokens <= max_tokens:
        return text

    # Binary search for the right length
    left, right = 0, len(text)

    while left < right:
        mid = (left + right + 1) // 2
        truncated = text[:mid] + suffix
        tokens = count_tokens(truncated, model)

        if tokens <= max_tokens:
            left = mid
        else:
            right = mid - 1

    return text[:left] + suffix


def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    model: str = "gpt-4"
) -> list[str]:
    """
    Split text into chunks based on token count

    Args:
        text: Input text
        chunk_size: Maximum tokens per chunk
        chunk_overlap: Number of overlapping tokens between chunks
        model: Model name for token counting

    Returns:
        List of text chunks
    """
    # Split into sentences
    sentences = text.replace("! ", "!|").replace("? ", "?|").replace(". ", ".|").split("|")

    chunks = []
    current_chunk = []
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = count_tokens(sentence, model)

        if current_tokens + sentence_tokens > chunk_size and current_chunk:
            # Save current chunk
            chunks.append(" ".join(current_chunk))

            # Start new chunk with overlap
            overlap_text = " ".join(current_chunk[-2:])  # Keep last 2 sentences
            current_chunk = [overlap_text, sentence]
            current_tokens = count_tokens(" ".join(current_chunk), model)
        else:
            current_chunk.append(sentence)
            current_tokens += sentence_tokens

    # Add final chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
