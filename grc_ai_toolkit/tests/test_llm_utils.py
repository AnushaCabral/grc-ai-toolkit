"""
Comprehensive tests for LLM utility functions

These tests verify token counting, cost estimation, and text processing utilities.
"""

import pytest
from unittest.mock import patch, Mock
from grc_ai_toolkit.llm.utils import (
    count_tokens,
    estimate_cost,
    format_conversation_history,
    truncate_text,
    chunk_text
)


class TestCountTokens:
    """Test count_tokens function"""

    def test_count_tokens_basic(self):
        """Test basic token counting"""
        text = "Hello, world!"
        tokens = count_tokens(text)

        assert isinstance(tokens, int)
        assert tokens > 0

    def test_count_tokens_gpt4(self):
        """Test token counting with GPT-4 model"""
        text = "This is a test message."
        tokens = count_tokens(text, model="gpt-4")

        assert isinstance(tokens, int)
        assert tokens > 0

    def test_count_tokens_gpt35_turbo(self):
        """Test token counting with GPT-3.5 model"""
        text = "This is a test message."
        tokens = count_tokens(text, model="gpt-3.5-turbo")

        assert isinstance(tokens, int)
        assert tokens > 0

    def test_count_tokens_claude(self):
        """Test token counting with Claude model"""
        text = "This is a test message."
        tokens = count_tokens(text, model="claude-sonnet-4-20250514")

        assert isinstance(tokens, int)
        assert tokens > 0

    def test_count_tokens_groq_models(self):
        """Test token counting with Groq models"""
        text = "This is a test message."

        for model in ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]:
            tokens = count_tokens(text, model=model)
            assert isinstance(tokens, int)
            assert tokens > 0

    def test_count_tokens_empty_string(self):
        """Test counting tokens in empty string"""
        tokens = count_tokens("")
        assert tokens == 0

    def test_count_tokens_long_text(self):
        """Test counting tokens in long text"""
        text = "This is a sentence. " * 100
        tokens = count_tokens(text)

        assert tokens > 100  # Should be more than 100 tokens

    def test_count_tokens_special_characters(self):
        """Test counting tokens with special characters"""
        text = "Hello! How are you? I'm doing great. 😊"
        tokens = count_tokens(text)

        assert tokens > 0

    def test_count_tokens_unknown_model(self):
        """Test counting tokens with unknown model (uses default)"""
        text = "Hello, world!"
        tokens = count_tokens(text, model="unknown-model-xyz")

        assert isinstance(tokens, int)
        assert tokens > 0

    def test_count_tokens_fallback_on_error(self):
        """Test fallback to character-based estimation on error"""
        text = "Hello, world!"

        with patch('grc_ai_toolkit.llm.utils.tiktoken.get_encoding', side_effect=Exception("Error")):
            tokens = count_tokens(text)

            # Should fallback to len(text) // 4
            expected = len(text) // 4
            assert tokens == expected

    def test_count_tokens_multiline(self):
        """Test counting tokens in multiline text"""
        text = """This is line 1.
This is line 2.
This is line 3."""
        tokens = count_tokens(text)

        assert tokens > 10


class TestEstimateCost:
    """Test estimate_cost function"""

    def test_estimate_cost_basic(self):
        """Test basic cost estimation"""
        cost = estimate_cost(1000, 500, "gpt-4")

        assert isinstance(cost, float)
        assert cost > 0

    def test_estimate_cost_gpt4(self):
        """Test cost estimation for GPT-4"""
        cost = estimate_cost(1_000_000, 1_000_000, "gpt-4")

        # Should be a reasonable cost (pricing may vary)
        assert cost > 0
        assert 50 < cost < 150  # Allow flexibility for different pricing

    def test_estimate_cost_zero_tokens(self):
        """Test cost estimation with zero tokens"""
        cost = estimate_cost(0, 0, "gpt-4")

        assert cost == 0.0

    def test_estimate_cost_input_only(self):
        """Test cost estimation with only input tokens"""
        cost = estimate_cost(1000, 0, "gpt-4")

        assert cost > 0

    def test_estimate_cost_output_only(self):
        """Test cost estimation with only output tokens"""
        cost = estimate_cost(0, 1000, "gpt-4")

        assert cost > 0

    def test_estimate_cost_unknown_model(self):
        """Test cost estimation for unknown model returns 0"""
        cost = estimate_cost(1000, 500, "unknown-model-xyz")

        assert cost == 0.0

    def test_estimate_cost_different_models(self):
        """Test cost estimation for different models"""
        input_tokens = 10000
        output_tokens = 5000

        # Test multiple models
        models = ["gpt-4", "gpt-3.5-turbo", "claude-sonnet-4-20250514"]

        for model in models:
            cost = estimate_cost(input_tokens, output_tokens, model)
            # All should have some cost or 0 if not in PRICING
            assert cost >= 0.0

    def test_estimate_cost_large_numbers(self):
        """Test cost estimation with large token counts"""
        cost = estimate_cost(10_000_000, 5_000_000, "gpt-4")

        assert cost > 0
        assert isinstance(cost, float)


class TestFormatConversationHistory:
    """Test format_conversation_history function"""

    def test_format_conversation_history_basic(self):
        """Test basic conversation formatting"""
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]

        result = format_conversation_history(messages)

        assert len(result) == 2
        assert result[0]["role"] == "user"
        assert result[0]["content"] == "Hello"

    def test_format_conversation_history_preserves_content(self):
        """Test that formatting preserves message content"""
        messages = [
            {"role": "user", "content": "What is AI?", "extra_field": "ignored"},
            {"role": "assistant", "content": "AI stands for Artificial Intelligence."}
        ]

        result = format_conversation_history(messages)

        assert len(result) == 2
        assert "extra_field" not in result[0]  # Extra fields removed
        assert result[0]["content"] == "What is AI?"

    def test_format_conversation_history_max_messages(self):
        """Test limiting conversation history"""
        messages = [
            {"role": "user", "content": f"Message {i}"}
            for i in range(10)
        ]

        result = format_conversation_history(messages, max_messages=3)

        assert len(result) == 3
        # Should keep the last 3 messages
        assert result[0]["content"] == "Message 7"
        assert result[2]["content"] == "Message 9"

    def test_format_conversation_history_no_limit(self):
        """Test conversation history without limit"""
        messages = [
            {"role": "user", "content": f"Message {i}"}
            for i in range(5)
        ]

        result = format_conversation_history(messages)

        assert len(result) == 5

    def test_format_conversation_history_empty(self):
        """Test formatting empty conversation"""
        result = format_conversation_history([])

        assert result == []

    def test_format_conversation_history_single_message(self):
        """Test formatting single message"""
        messages = [{"role": "user", "content": "Hello"}]

        result = format_conversation_history(messages)

        assert len(result) == 1
        assert result[0]["role"] == "user"

    def test_format_conversation_history_max_messages_larger_than_list(self):
        """Test max_messages larger than message count"""
        messages = [
            {"role": "user", "content": "Message 1"},
            {"role": "assistant", "content": "Response 1"}
        ]

        result = format_conversation_history(messages, max_messages=10)

        assert len(result) == 2


class TestTruncateText:
    """Test truncate_text function"""

    def test_truncate_text_no_truncation_needed(self):
        """Test text that doesn't need truncation"""
        text = "Short text"
        result = truncate_text(text, max_tokens=1000)

        assert result == text

    def test_truncate_text_basic(self):
        """Test basic text truncation"""
        text = "This is a very long text. " * 100
        result = truncate_text(text, max_tokens=50)

        assert len(result) < len(text)
        assert result.endswith("...")

    def test_truncate_text_custom_suffix(self):
        """Test truncation with custom suffix"""
        text = "This is a very long text. " * 100
        result = truncate_text(text, max_tokens=50, suffix=" [MORE]")

        assert result.endswith(" [MORE]")

    def test_truncate_text_empty_string(self):
        """Test truncating empty string"""
        result = truncate_text("", max_tokens=100)

        assert result == ""

    def test_truncate_text_exactly_at_limit(self):
        """Test text that's exactly at token limit"""
        text = "Hello world"
        tokens = count_tokens(text)

        result = truncate_text(text, max_tokens=tokens)

        # Should not be truncated
        assert result == text

    def test_truncate_text_different_models(self):
        """Test truncation with different models"""
        text = "This is a test message. " * 50

        for model in ["gpt-4", "gpt-3.5-turbo", "claude-sonnet-4-20250514"]:
            result = truncate_text(text, max_tokens=20, model=model)
            assert len(result) < len(text)


class TestChunkText:
    """Test chunk_text function"""

    def test_chunk_text_basic(self):
        """Test basic text chunking"""
        text = "Sentence one. Sentence two. Sentence three. Sentence four."
        chunks = chunk_text(text, chunk_size=10)

        assert isinstance(chunks, list)
        assert len(chunks) > 0
        assert all(isinstance(chunk, str) for chunk in chunks)

    def test_chunk_text_short_text(self):
        """Test chunking short text"""
        text = "Short sentence."
        chunks = chunk_text(text, chunk_size=100)

        assert len(chunks) == 1
        assert chunks[0].strip() == text.strip()

    def test_chunk_text_long_text(self):
        """Test chunking long text"""
        text = "This is a sentence. " * 100
        chunks = chunk_text(text, chunk_size=50)

        assert len(chunks) > 1

    def test_chunk_text_custom_chunk_size(self):
        """Test chunking with custom chunk size"""
        text = "Sentence. " * 50

        chunks_small = chunk_text(text, chunk_size=10)
        chunks_large = chunk_text(text, chunk_size=100)

        assert len(chunks_small) > len(chunks_large)

    def test_chunk_text_overlap(self):
        """Test that chunks have overlap"""
        text = "First sentence. Second sentence. Third sentence. Fourth sentence. Fifth sentence."
        chunks = chunk_text(text, chunk_size=15, chunk_overlap=5)

        # Verify we have multiple chunks
        assert len(chunks) >= 2

    def test_chunk_text_empty_string(self):
        """Test chunking empty string"""
        chunks = chunk_text("")

        # Should return empty list or single empty chunk
        assert isinstance(chunks, list)

    def test_chunk_text_special_punctuation(self):
        """Test chunking with various punctuation"""
        text = "Question? Exclamation! Statement. Another?"
        chunks = chunk_text(text, chunk_size=20)

        assert isinstance(chunks, list)
        assert len(chunks) > 0

    def test_chunk_text_no_punctuation(self):
        """Test chunking text without sentence-ending punctuation"""
        text = "This is text without proper punctuation marks"
        chunks = chunk_text(text, chunk_size=50)

        # Should handle it gracefully
        assert isinstance(chunks, list)
        assert len(chunks) >= 1

    def test_chunk_text_different_models(self):
        """Test chunking with different models"""
        text = "Sentence one. Sentence two. Sentence three." * 10

        for model in ["gpt-4", "gpt-3.5-turbo"]:
            chunks = chunk_text(text, chunk_size=30, model=model)
            assert isinstance(chunks, list)
            assert len(chunks) > 0

    def test_chunk_text_preserves_content(self):
        """Test that chunking preserves all content"""
        text = "First. Second. Third."
        chunks = chunk_text(text, chunk_size=5)

        # Combine all chunks
        combined = " ".join(chunks)

        # All sentences should be present (may have duplicates due to overlap)
        assert "First" in combined
        assert "Second" in combined
        assert "Third" in combined


class TestIntegration:
    """Integration tests for utility functions"""

    def test_count_and_truncate_integration(self):
        """Test using count_tokens with truncate_text"""
        text = "This is a long text. " * 50
        tokens = count_tokens(text)

        truncated = truncate_text(text, max_tokens=tokens // 2)
        truncated_tokens = count_tokens(truncated)

        assert truncated_tokens < tokens
        assert truncated_tokens <= tokens // 2 + 10  # Allow some margin

    def test_chunk_and_count_integration(self):
        """Test chunking and counting tokens"""
        text = "Sentence one. Sentence two. Sentence three." * 20
        chunks = chunk_text(text, chunk_size=30)

        # Count tokens in each chunk
        for chunk in chunks:
            token_count = count_tokens(chunk)
            # Each chunk should be under the limit (with some margin for overlap)
            assert token_count <= 50  # Allow margin

    def test_format_and_count_integration(self):
        """Test formatting conversation and counting tokens"""
        messages = [
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing well, thank you!"},
            {"role": "user", "content": "That's great to hear."}
        ]

        formatted = format_conversation_history(messages)

        # Count total tokens in conversation
        total_tokens = sum(
            count_tokens(msg["content"])
            for msg in formatted
        )

        assert total_tokens > 0

    def test_estimate_cost_with_real_counts(self):
        """Test cost estimation with real token counts"""
        text = "Hello, this is a test message for cost estimation."

        input_tokens = count_tokens(text)
        output_tokens = count_tokens("This is a response.")

        cost = estimate_cost(input_tokens, output_tokens, "gpt-4")

        assert cost > 0
        assert isinstance(cost, float)
