"""
Integration tests for agent execution

These tests verify that agents work end-to-end with real or mocked LLM calls.
"""

import pytest
from unittest.mock import Mock, patch

from grc_ai_toolkit.agents import ResearchAgent, AnalysisAgent, GenerationAgent, SimpleAgent, AgentConfig
from grc_ai_toolkit.llm import LLMManager, LLMConfig


class TestAgentExecution:
    """Test agent execution end-to-end"""

    @pytest.fixture
    def mock_llm_manager(self):
        """Create a mock LLM manager for testing"""
        manager = Mock(spec=LLMManager)
        manager.generate.return_value = "This is a test response from the mock LLM."
        return manager

    def test_simple_agent_execution(self, mock_llm_manager):
        """Test SimpleAgent can execute a task"""
        # Create agent
        config = AgentConfig(
            name="TestAgent",
            description="Test agent for integration testing",
            system_message="You are a test agent.",
            llm_manager=mock_llm_manager
        )
        agent = SimpleAgent(config)

        # Execute task
        result = agent.execute("Test task", {"key": "value"})

        # Verify
        assert result == "This is a test response from the mock LLM."
        assert agent.state["status"] == "completed"
        assert agent.state["iteration_count"] == 1
        mock_llm_manager.generate.assert_called_once()

    def test_research_agent_execution(self, mock_llm_manager):
        """Test ResearchAgent can execute a research task"""
        agent = ResearchAgent(mock_llm_manager)

        result = agent.execute(
            "Research the latest cybersecurity threats",
            {"context": "Focus on ransomware attacks"}
        )

        assert result == "This is a test response from the mock LLM."
        assert agent.state["status"] == "completed"
        assert agent.config.name == "Research Agent"
        mock_llm_manager.generate.assert_called_once()

    def test_analysis_agent_execution(self, mock_llm_manager):
        """Test AnalysisAgent can execute an analysis task"""
        agent = AnalysisAgent(mock_llm_manager)

        result = agent.execute(
            "Analyze risk exposure",
            {"risk_data": "Sample risk data"}
        )

        assert result == "This is a test response from the mock LLM."
        assert agent.state["status"] == "completed"
        assert agent.config.name == "Analysis Agent"

    def test_generation_agent_execution(self, mock_llm_manager):
        """Test GenerationAgent can execute a generation task"""
        agent = GenerationAgent(mock_llm_manager)

        result = agent.execute(
            "Generate a data privacy policy",
            {"company": "Acme Corp"}
        )

        assert result == "This is a test response from the mock LLM."
        assert agent.state["status"] == "completed"
        assert agent.config.name == "Generation Agent"

    def test_agent_state_management(self, mock_llm_manager):
        """Test agent state is properly managed during execution"""
        agent = ResearchAgent(mock_llm_manager)

        # Initial state
        assert agent.state["status"] == "idle"
        assert agent.state["iteration_count"] == 0
        assert len(agent.state["messages"]) == 0

        # Execute task
        agent.execute("Test task")

        # Verify state updated
        assert agent.state["status"] == "completed"
        assert agent.state["iteration_count"] == 1
        assert len(agent.state["messages"]) > 0
        assert agent.state["result"] == "This is a test response from the mock LLM."

    def test_agent_error_handling(self, mock_llm_manager):
        """Test agent handles errors properly"""
        # Configure mock to raise an error
        mock_llm_manager.generate.side_effect = Exception("LLM error")

        agent = SimpleAgent(AgentConfig(
            name="TestAgent",
            description="Test agent",
            system_message="Test",
            llm_manager=mock_llm_manager
        ))

        # Execute should raise the exception
        with pytest.raises(Exception, match="LLM error"):
            agent.execute("Test task")

        # Verify state shows failure
        assert agent.state["status"] == "failed"
        assert "LLM error" in agent.state["result"]

    def test_agent_reset_state(self, mock_llm_manager):
        """Test agent state can be reset"""
        agent = ResearchAgent(mock_llm_manager)

        # Execute task
        agent.execute("Test task")
        assert agent.state["status"] == "completed"
        assert agent.state["iteration_count"] == 1

        # Reset state
        agent.reset_state()

        # Verify reset
        assert agent.state["status"] == "idle"
        assert agent.state["iteration_count"] == 0
        assert len(agent.state["messages"]) == 0
        assert agent.state["result"] is None

    def test_agent_multiple_executions(self, mock_llm_manager):
        """Test agent can handle multiple executions"""
        agent = ResearchAgent(mock_llm_manager)

        # First execution
        result1 = agent.execute("Task 1")
        assert result1 == "This is a test response from the mock LLM."
        assert agent.state["iteration_count"] == 1

        # Second execution
        result2 = agent.execute("Task 2")
        assert result2 == "This is a test response from the mock LLM."
        assert agent.state["iteration_count"] == 2

        # Verify both calls were made
        assert mock_llm_manager.generate.call_count == 2


@pytest.mark.integration
class TestAgentIntegrationWithRealLLM:
    """
    Integration tests with real LLM (requires API keys)

    These tests are marked with @pytest.mark.integration and are skipped by default.
    Run with: pytest -m integration
    """

    @pytest.fixture
    def real_llm_manager(self):
        """Create a real LLM manager (requires API keys)"""
        # This will fail if API keys are not configured
        config = LLMConfig.from_env()
        return LLMManager(config)

    @pytest.mark.skip(reason="Requires API keys and makes real API calls")
    def test_research_agent_with_real_llm(self, real_llm_manager):
        """Test ResearchAgent with real LLM"""
        agent = ResearchAgent(real_llm_manager)

        result = agent.execute(
            "What are the key principles of data privacy?",
            {"framework": "GDPR"}
        )

        # Basic validation of real response
        assert isinstance(result, str)
        assert len(result) > 50  # Should be a substantial response
        assert agent.state["status"] == "completed"

    @pytest.mark.skip(reason="Requires API keys and makes real API calls")
    def test_analysis_agent_with_real_llm(self, real_llm_manager):
        """Test AnalysisAgent with real LLM"""
        agent = AnalysisAgent(real_llm_manager)

        result = agent.execute(
            "Analyze the cybersecurity risks",
            {"scenario": "Remote work environment"}
        )

        assert isinstance(result, str)
        assert len(result) > 50
        assert agent.state["status"] == "completed"
