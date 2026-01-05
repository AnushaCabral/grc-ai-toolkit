"""
Comprehensive tests for AgentOrchestrator

These tests verify multi-agent workflow coordination and execution.
"""

import pytest
from unittest.mock import Mock, MagicMock
from grc_ai_toolkit.agents.orchestrator import (
    AgentOrchestrator,
    WorkflowStep,
    WorkflowResult
)
from grc_ai_toolkit.agents import BaseAgent, AgentConfig


class TestWorkflowStep:
    """Test WorkflowStep dataclass"""

    def test_workflow_step_creation(self):
        """Test creating a workflow step"""
        mock_agent = Mock(spec=BaseAgent)

        step = WorkflowStep(
            agent=mock_agent,
            task_template="Test task for {topic}",
            depends_on=["step1"],
            condition=lambda ctx: True
        )

        assert step.agent == mock_agent
        assert step.task_template == "Test task for {topic}"
        assert step.depends_on == ["step1"]
        assert step.condition is not None

    def test_workflow_step_defaults(self):
        """Test workflow step with default values"""
        mock_agent = Mock(spec=BaseAgent)

        step = WorkflowStep(
            agent=mock_agent,
            task_template="Test task"
        )

        assert step.depends_on == []
        assert step.condition is None


class TestWorkflowResult:
    """Test WorkflowResult dataclass"""

    def test_workflow_result_creation(self):
        """Test creating a workflow result"""
        result = WorkflowResult(
            success=True,
            results={"step1": "result1", "step2": "result2"},
            errors={},
            execution_order=["step1", "step2"],
            total_steps=2
        )

        assert result.success is True
        assert len(result.results) == 2
        assert len(result.errors) == 0
        assert result.total_steps == 2

    def test_workflow_result_with_errors(self):
        """Test workflow result with errors"""
        result = WorkflowResult(
            success=False,
            results={"step1": "result1"},
            errors={"step2": "Error message"},
            execution_order=["step1", "step2"],
            total_steps=2
        )

        assert result.success is False
        assert len(result.errors) == 1


class TestAgentOrchestratorInit:
    """Test AgentOrchestrator initialization"""

    def test_orchestrator_creation(self):
        """Test creating an orchestrator"""
        orchestrator = AgentOrchestrator(name="test_workflow")

        assert orchestrator.name == "test_workflow"
        assert len(orchestrator.steps) == 0
        assert len(orchestrator.execution_history) == 0

    def test_orchestrator_default_name(self):
        """Test orchestrator with default name"""
        orchestrator = AgentOrchestrator()

        assert orchestrator.name == "default_workflow"


class TestAgentOrchestratorAddStep:
    """Test adding steps to orchestrator"""

    @pytest.fixture
    def mock_agent(self):
        """Create a mock agent"""
        agent = Mock(spec=BaseAgent)
        agent.config = Mock()
        agent.config.name = "TestAgent"
        agent.execute = Mock(return_value="Test result")
        return agent

    @pytest.fixture
    def orchestrator(self):
        """Create an orchestrator instance"""
        return AgentOrchestrator(name="test")

    def test_add_step_basic(self, orchestrator, mock_agent):
        """Test adding a basic step"""
        orchestrator.add_step(
            "step1",
            mock_agent,
            "Test task"
        )

        assert "step1" in orchestrator.steps
        assert orchestrator.steps["step1"].agent == mock_agent
        assert orchestrator.steps["step1"].task_template == "Test task"

    def test_add_step_with_dependencies(self, orchestrator, mock_agent):
        """Test adding a step with dependencies"""
        orchestrator.add_step("step1", mock_agent, "Task 1")
        orchestrator.add_step("step2", mock_agent, "Task 2", depends_on=["step1"])

        assert orchestrator.steps["step2"].depends_on == ["step1"]

    def test_add_step_with_condition(self, orchestrator, mock_agent):
        """Test adding a step with condition"""
        condition = lambda ctx: ctx.get("run_step", False)

        orchestrator.add_step("step1", mock_agent, "Task", condition=condition)

        assert orchestrator.steps["step1"].condition == condition

    def test_add_duplicate_step_raises_error(self, orchestrator, mock_agent):
        """Test adding duplicate step name raises error"""
        orchestrator.add_step("step1", mock_agent, "Task 1")

        with pytest.raises(ValueError, match="already exists"):
            orchestrator.add_step("step1", mock_agent, "Task 2")

    def test_add_step_warns_about_missing_dependency(self, orchestrator, mock_agent):
        """Test adding step with non-existent dependency logs warning"""
        # Should not raise error, just log warning
        orchestrator.add_step("step2", mock_agent, "Task", depends_on=["step1"])

        assert "step2" in orchestrator.steps


class TestAgentOrchestratorTopologicalSort:
    """Test topological sorting for execution order"""

    @pytest.fixture
    def orchestrator(self):
        """Create an orchestrator instance"""
        return AgentOrchestrator()

    @pytest.fixture
    def mock_agent(self):
        """Create a mock agent"""
        agent = Mock(spec=BaseAgent)
        agent.execute = Mock(return_value="Result")
        return agent

    def test_topological_sort_linear(self, orchestrator, mock_agent):
        """Test topological sort with linear dependencies"""
        orchestrator.add_step("step1", mock_agent, "Task 1")
        orchestrator.add_step("step2", mock_agent, "Task 2", depends_on=["step1"])
        orchestrator.add_step("step3", mock_agent, "Task 3", depends_on=["step2"])

        order = orchestrator._topological_sort()

        assert order == ["step1", "step2", "step3"]

    def test_topological_sort_parallel(self, orchestrator, mock_agent):
        """Test topological sort with parallel steps"""
        orchestrator.add_step("step1", mock_agent, "Task 1")
        orchestrator.add_step("step2", mock_agent, "Task 2")
        orchestrator.add_step("step3", mock_agent, "Task 3", depends_on=["step1", "step2"])

        order = orchestrator._topological_sort()

        # step1 and step2 can be in any order, but both before step3
        assert order.index("step1") < order.index("step3")
        assert order.index("step2") < order.index("step3")

    def test_topological_sort_complex(self, orchestrator, mock_agent):
        """Test topological sort with complex dependencies"""
        orchestrator.add_step("a", mock_agent, "Task A")
        orchestrator.add_step("b", mock_agent, "Task B", depends_on=["a"])
        orchestrator.add_step("c", mock_agent, "Task C", depends_on=["a"])
        orchestrator.add_step("d", mock_agent, "Task D", depends_on=["b", "c"])

        order = orchestrator._topological_sort()

        # a must be first
        assert order[0] == "a"
        # b and c must be before d
        assert order.index("b") < order.index("d")
        assert order.index("c") < order.index("d")

    def test_topological_sort_circular_dependency(self, orchestrator, mock_agent):
        """Test topological sort detects circular dependencies"""
        orchestrator.add_step("step1", mock_agent, "Task 1", depends_on=["step2"])
        orchestrator.add_step("step2", mock_agent, "Task 2", depends_on=["step1"])

        with pytest.raises(ValueError, match="Circular dependencies"):
            orchestrator._topological_sort()


class TestAgentOrchestratorExecute:
    """Test workflow execution"""

    @pytest.fixture
    def mock_agent(self):
        """Create a mock agent that returns predictable results"""
        agent = Mock(spec=BaseAgent)
        agent.config = Mock()
        agent.config.name = "TestAgent"
        agent.execute = Mock(return_value="Test result")
        return agent

    @pytest.fixture
    def orchestrator(self):
        """Create an orchestrator instance"""
        return AgentOrchestrator(name="test_workflow")

    def test_execute_single_step(self, orchestrator, mock_agent):
        """Test executing workflow with single step"""
        orchestrator.add_step("step1", mock_agent, "Test task")

        result = orchestrator.execute()

        assert result.success is True
        assert "step1" in result.results
        assert result.results["step1"] == "Test result"
        assert len(result.errors) == 0
        mock_agent.execute.assert_called_once()

    def test_execute_multiple_steps(self, orchestrator, mock_agent):
        """Test executing workflow with multiple steps"""
        orchestrator.add_step("step1", mock_agent, "Task 1")
        orchestrator.add_step("step2", mock_agent, "Task 2")

        result = orchestrator.execute()

        assert result.success is True
        assert len(result.results) == 2
        assert mock_agent.execute.call_count == 2

    def test_execute_with_context(self, orchestrator, mock_agent):
        """Test executing workflow with initial context"""
        orchestrator.add_step("step1", mock_agent, "Research {topic}")

        result = orchestrator.execute(context={"topic": "data privacy"})

        # Verify task was formatted with context
        call_args = mock_agent.execute.call_args[0]
        assert "data privacy" in call_args[0]

    def test_execute_with_dependencies(self, orchestrator):
        """Test executing workflow with dependencies"""
        agent1 = Mock(spec=BaseAgent)
        agent1.execute = Mock(return_value="Result from step1")

        agent2 = Mock(spec=BaseAgent)
        agent2.execute = Mock(return_value="Result from step2")

        orchestrator.add_step("step1", agent1, "Task 1")
        orchestrator.add_step("step2", agent2, "Task 2 using {step1}", depends_on=["step1"])

        result = orchestrator.execute()

        assert result.success is True
        # Verify step2 received result from step1
        call_args = agent2.execute.call_args[0]
        assert "Result from step1" in call_args[0]

    def test_execute_with_condition_true(self, orchestrator, mock_agent):
        """Test executing step with condition that evaluates to True"""
        orchestrator.add_step(
            "step1",
            mock_agent,
            "Task",
            condition=lambda ctx: ctx.get("run", True)
        )

        result = orchestrator.execute(context={"run": True})

        assert "step1" in result.results
        mock_agent.execute.assert_called_once()

    def test_execute_with_condition_false(self, orchestrator, mock_agent):
        """Test executing step with condition that evaluates to False"""
        orchestrator.add_step(
            "step1",
            mock_agent,
            "Task",
            condition=lambda ctx: ctx.get("run", False)
        )

        result = orchestrator.execute(context={"run": False})

        assert "step1" not in result.results
        mock_agent.execute.assert_not_called()

    def test_execute_with_failing_step(self, orchestrator, mock_agent):
        """Test executing workflow when a step fails"""
        mock_agent.execute = Mock(side_effect=Exception("Agent failed"))

        orchestrator.add_step("step1", mock_agent, "Task")

        result = orchestrator.execute()

        assert result.success is False
        assert "step1" in result.errors
        assert "Agent failed" in result.errors["step1"]

    def test_execute_with_retry(self, orchestrator):
        """Test step retry on failure"""
        agent = Mock(spec=BaseAgent)
        # Fail twice, then succeed
        agent.execute = Mock(side_effect=[
            Exception("Fail 1"),
            Exception("Fail 2"),
            "Success"
        ])

        orchestrator.add_step("step1", agent, "Task")

        result = orchestrator.execute(max_retries=2)

        assert result.success is True
        assert result.results["step1"] == "Success"
        assert agent.execute.call_count == 3

    def test_execute_max_retries_exceeded(self, orchestrator):
        """Test step fails after max retries"""
        agent = Mock(spec=BaseAgent)
        agent.execute = Mock(side_effect=Exception("Always fails"))

        orchestrator.add_step("step1", agent, "Task")

        result = orchestrator.execute(max_retries=1)

        assert result.success is False
        assert "step1" in result.errors
        assert agent.execute.call_count == 2  # 1 initial + 1 retry

    def test_execute_unsatisfied_dependencies(self, orchestrator):
        """Test step skipped when dependencies not satisfied"""
        agent1 = Mock(spec=BaseAgent)
        agent1.execute = Mock(side_effect=Exception("Failed"))

        agent2 = Mock(spec=BaseAgent)
        agent2.execute = Mock(return_value="Result")

        orchestrator.add_step("step1", agent1, "Task 1")
        orchestrator.add_step("step2", agent2, "Task 2", depends_on=["step1"])

        result = orchestrator.execute(max_retries=0)

        assert result.success is False
        assert "step1" in result.errors
        assert "step2" in result.errors  # Skipped due to missing dependency

    def test_execute_updates_history(self, orchestrator, mock_agent):
        """Test execution adds result to history"""
        orchestrator.add_step("step1", mock_agent, "Task")

        assert len(orchestrator.execution_history) == 0

        orchestrator.execute()

        assert len(orchestrator.execution_history) == 1
        assert isinstance(orchestrator.execution_history[0], WorkflowResult)

    def test_execute_circular_dependency_error(self, orchestrator, mock_agent):
        """Test execution handles circular dependency error"""
        orchestrator.add_step("step1", mock_agent, "Task", depends_on=["step2"])
        orchestrator.add_step("step2", mock_agent, "Task", depends_on=["step1"])

        result = orchestrator.execute()

        assert result.success is False
        assert "workflow" in result.errors
        assert "Circular" in result.errors["workflow"]


class TestAgentOrchestratorVisualize:
    """Test workflow visualization"""

    @pytest.fixture
    def orchestrator(self):
        """Create an orchestrator with some steps"""
        orch = AgentOrchestrator(name="test_workflow")

        agent = Mock(spec=BaseAgent)
        agent.config = Mock()
        agent.config.name = "TestAgent"

        orch.add_step("step1", agent, "Task 1")
        orch.add_step("step2", agent, "Task 2 with {step1}", depends_on=["step1"])

        return orch

    def test_visualize_workflow(self, orchestrator):
        """Test visualizing workflow"""
        viz = orchestrator.visualize()

        assert "test_workflow" in viz
        assert "step1" in viz
        assert "step2" in viz
        assert "TestAgent" in viz
        assert "Depends on" in viz

    def test_visualize_with_condition(self):
        """Test visualizing workflow with conditions"""
        orchestrator = AgentOrchestrator(name="test")
        agent = Mock(spec=BaseAgent)
        agent.config = Mock()
        agent.config.name = "TestAgent"

        orchestrator.add_step(
            "step1",
            agent,
            "Task",
            condition=lambda ctx: True
        )

        viz = orchestrator.visualize()

        assert "Conditional: Yes" in viz

    def test_visualize_circular_dependency(self):
        """Test visualizing workflow with circular dependency"""
        orchestrator = AgentOrchestrator()
        agent = Mock(spec=BaseAgent)
        agent.config = Mock()
        agent.config.name = "TestAgent"

        orchestrator.add_step("step1", agent, "Task", depends_on=["step2"])
        orchestrator.add_step("step2", agent, "Task", depends_on=["step1"])

        viz = orchestrator.visualize()

        assert "Circular dependencies" in viz


class TestAgentOrchestratorStats:
    """Test workflow statistics"""

    @pytest.fixture
    def orchestrator(self):
        """Create an orchestrator instance"""
        return AgentOrchestrator(name="stats_test")

    @pytest.fixture
    def mock_agent(self):
        """Create a mock agent"""
        agent = Mock(spec=BaseAgent)
        agent.execute = Mock(return_value="Result")
        return agent

    def test_get_stats_no_executions(self, orchestrator, mock_agent):
        """Test stats with no executions"""
        orchestrator.add_step("step1", mock_agent, "Task")

        stats = orchestrator.get_stats()

        assert stats["name"] == "stats_test"
        assert stats["total_steps"] == 1
        assert stats["total_executions"] == 0
        assert stats["success_rate"] == 0.0

    def test_get_stats_after_execution(self, orchestrator, mock_agent):
        """Test stats after successful execution"""
        orchestrator.add_step("step1", mock_agent, "Task")

        orchestrator.execute()

        stats = orchestrator.get_stats()

        assert stats["total_executions"] == 1
        assert stats["successful_executions"] == 1
        assert stats["failed_executions"] == 0
        assert stats["success_rate"] == 100.0

    def test_get_stats_mixed_results(self, orchestrator):
        """Test stats with mixed success/failure"""
        agent_success = Mock(spec=BaseAgent)
        agent_success.execute = Mock(return_value="Success")

        agent_fail = Mock(spec=BaseAgent)
        agent_fail.execute = Mock(side_effect=Exception("Fail"))

        orchestrator.add_step("step1", agent_success, "Task")

        # Execute successfully
        orchestrator.execute()

        # Clear steps and add failing step
        orchestrator.steps.clear()
        orchestrator.add_step("step1", agent_fail, "Task")

        # Execute with failure
        orchestrator.execute(max_retries=0)

        stats = orchestrator.get_stats()

        assert stats["total_executions"] == 2
        assert stats["successful_executions"] == 1
        assert stats["failed_executions"] == 1
        assert stats["success_rate"] == 50.0


class TestAgentOrchestratorUtilities:
    """Test orchestrator utility methods"""

    def test_clear_history(self):
        """Test clearing execution history"""
        orchestrator = AgentOrchestrator()
        agent = Mock(spec=BaseAgent)
        agent.execute = Mock(return_value="Result")

        orchestrator.add_step("step1", agent, "Task")
        orchestrator.execute()

        assert len(orchestrator.execution_history) == 1

        orchestrator.clear_history()

        assert len(orchestrator.execution_history) == 0

    def test_str_representation(self):
        """Test string representation"""
        orchestrator = AgentOrchestrator(name="test")
        agent = Mock(spec=BaseAgent)

        orchestrator.add_step("step1", agent, "Task")
        orchestrator.add_step("step2", agent, "Task")

        str_repr = str(orchestrator)

        assert "test" in str_repr
        assert "2 steps" in str_repr

    def test_repr_representation(self):
        """Test repr representation"""
        orchestrator = AgentOrchestrator(name="test")
        agent = Mock(spec=BaseAgent)

        orchestrator.add_step("step1", agent, "Task")

        repr_str = repr(orchestrator)

        assert "AgentOrchestrator" in repr_str
        assert "test" in repr_str
        assert "1 steps" in repr_str
