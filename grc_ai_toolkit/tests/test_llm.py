"""
Tests for LLM module
"""

import pytest
from unittest.mock import Mock, patch
from langchain_core.messages import AIMessage
from grc_ai_toolkit.llm import LLMManager, LLMConfig, PromptTemplate
from grc_ai_toolkit.llm.config import LLMProvider


class TestLLMConfig:
    """Tests for LLMConfig"""

    def test_default_config(self):
        """Test default configuration values"""
        config = LLMConfig(
            openai_api_key="test_key",
            provider=LLMProvider.OPENAI
        )

        assert config.provider == LLMProvider.OPENAI
        assert config.temperature == 0.7
        assert config.max_tokens == 2000
        assert config.enable_cost_tracking is True
        assert config.enable_caching is True

    def test_config_validation_temperature(self):
        """Test temperature validation"""
        with pytest.raises(ValueError, match="Temperature must be between 0 and 2"):
            LLMConfig(
                openai_api_key="test_key",
                provider=LLMProvider.OPENAI,
                temperature=3.0
            )

    def test_config_validation_max_tokens(self):
        """Test max_tokens validation"""
        with pytest.raises(ValueError, match="max_tokens must be positive"):
            LLMConfig(
                openai_api_key="test_key",
                provider=LLMProvider.OPENAI,
                max_tokens=-1
            )

    def test_config_api_key_required(self):
        """Test that API key is required for provider"""
        with pytest.raises(ValueError, match="OpenAI API key is required"):
            LLMConfig(provider=LLMProvider.OPENAI)


class TestPromptTemplate:
    """Tests for PromptTemplate"""

    def test_create_template(self):
        """Test creating a prompt template"""
        template = PromptTemplate(
            name="test_template",
            template="Create a {doc_type} for {framework}",
            input_variables=["doc_type", "framework"]
        )

        assert template.name == "test_template"
        assert len(template.input_variables) == 2

    def test_template_validation(self):
        """Test template validates required variables"""
        with pytest.raises(ValueError, match="Template missing required variable"):
            PromptTemplate(
                name="invalid",
                template="Create a {doc_type}",
                input_variables=["doc_type", "framework"]  # framework not in template
            )

    def test_template_format(self):
        """Test formatting template with values"""
        template = PromptTemplate(
            name="test",
            template="Create a {doc_type} for {framework}",
            input_variables=["doc_type", "framework"]
        )

        result = template.format(doc_type="policy", framework="SOC 2")

        assert result == "Create a policy for SOC 2"

    def test_template_format_missing_variable(self):
        """Test error when missing required variable"""
        template = PromptTemplate(
            name="test",
            template="Create a {doc_type} for {framework}",
            input_variables=["doc_type", "framework"]
        )

        with pytest.raises(ValueError, match="Missing required variables"):
            template.format(doc_type="policy")  # missing framework


class TestLLMManager:
    """Tests for LLMManager"""

    @pytest.fixture
    def mock_config(self):
        """Create mock configuration"""
        return LLMConfig(
            provider=LLMProvider.OPENAI,
            openai_api_key="test_key",
            enable_cost_tracking=False,
            enable_caching=False
        )

    @pytest.fixture
    def mock_llm_manager(self, mock_config):
        """Create LLMManager with mocked LLM"""
        with patch('grc_ai_toolkit.llm.manager.ChatOpenAI') as mock_llm, \
             patch('grc_ai_toolkit.llm.manager.StrOutputParser') as mock_parser:
            # Mock the LLM response
            mock_instance = Mock()
            mock_instance.invoke.return_value = AIMessage(content="Test response")
            mock_llm.return_value = mock_instance

            # Mock the parser to return string
            parser_instance = Mock()
            parser_instance.parse.return_value = "Test response"
            mock_parser.return_value = parser_instance

            manager = LLMManager(mock_config)
            yield manager

    def test_llm_manager_initialization(self, mock_llm_manager):
        """Test LLM manager initializes correctly"""
        assert mock_llm_manager is not None
        assert mock_llm_manager.request_count == 0
        assert mock_llm_manager.total_cost == 0.0

    def test_generate_simple_prompt(self, mock_llm_manager):
        """Test generating text from simple prompt"""
        response = mock_llm_manager.generate("Test prompt")

        assert isinstance(response, str)
        assert mock_llm_manager.request_count == 1

    def test_generate_with_system_message(self, mock_llm_manager):
        """Test generating with system message"""
        response = mock_llm_manager.generate(
            prompt="Test prompt",
            system_message="You are a test assistant"
        )

        assert isinstance(response, str)

    def test_get_stats(self, mock_llm_manager):
        """Test getting usage statistics"""
        mock_llm_manager.generate("Test")

        stats = mock_llm_manager.get_stats()

        assert "provider" in stats
        assert "model" in stats
        assert "request_count" in stats
        assert stats["request_count"] == 1

    def test_reset_stats(self, mock_llm_manager):
        """Test resetting statistics"""
        mock_llm_manager.generate("Test")
        assert mock_llm_manager.request_count == 1

        mock_llm_manager.reset_stats()

        assert mock_llm_manager.request_count == 0
        assert mock_llm_manager.total_cost == 0.0


# Integration tests (require actual API keys - skip in CI)
@pytest.mark.integration
@pytest.mark.skip(reason="Requires API keys and makes real API calls")
class TestLLMIntegration:
    """Integration tests with real LLM APIs"""

    def test_real_openai_call(self):
        """Test real OpenAI API call"""
        import os
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")

        config = LLMConfig.from_env()
        manager = LLMManager(config)

        response = manager.generate("Say 'Hello World'")

        assert "hello" in response.lower() or "world" in response.lower()

    def test_real_anthropic_call(self):
        """Test real Anthropic API call"""
        import os
        if not os.getenv("ANTHROPIC_API_KEY"):
            pytest.skip("ANTHROPIC_API_KEY not set")

        config = LLMConfig.from_env("anthropic")
        manager = LLMManager(config)

        response = manager.generate("Say 'Hello World'")

        assert "hello" in response.lower() or "world" in response.lower()
