"""
Agent Orchestrator for Multi-Agent Workflows
"""

from typing import Dict, Any, List, Optional, Callable
import logging
from dataclasses import dataclass, field

from .base import BaseAgent, AgentState


logger = logging.getLogger(__name__)


@dataclass
class WorkflowStep:
    """Single step in an agent workflow"""

    agent: BaseAgent
    task_template: str  # Can use {variable} placeholders
    depends_on: List[str] = field(default_factory=list)  # List of step names
    condition: Optional[Callable[[Dict[str, Any]], bool]] = None  # Optional condition


@dataclass
class WorkflowResult:
    """Result of workflow execution"""

    success: bool
    results: Dict[str, str]  # step_name -> result
    errors: Dict[str, str]  # step_name -> error
    execution_order: List[str]
    total_steps: int


class AgentOrchestrator:
    """
    Orchestrates multi-agent workflows for complex GRC tasks

    Supports:
    - Sequential execution
    - Parallel execution (where dependencies allow)
    - Conditional branching
    - Error handling and recovery

    Example:
        orchestrator = AgentOrchestrator()

        # Add agents
        orchestrator.add_step(
            "research",
            research_agent,
            "Research {topic} in our policy database"
        )
        orchestrator.add_step(
            "analyze",
            analysis_agent,
            "Analyze findings: {research}",
            depends_on=["research"]
        )
        orchestrator.add_step(
            "generate",
            generation_agent,
            "Generate report based on: {analyze}",
            depends_on=["analyze"]
        )

        # Execute workflow
        result = orchestrator.execute({"topic": "data privacy"})
    """

    def __init__(self, name: str = "default_workflow"):
        """
        Initialize orchestrator

        Args:
            name: Workflow name
        """
        self.name = name
        self.steps: Dict[str, WorkflowStep] = {}
        self.execution_history: List[WorkflowResult] = []

    def add_step(
        self,
        step_name: str,
        agent: BaseAgent,
        task_template: str,
        depends_on: Optional[List[str]] = None,
        condition: Optional[Callable[[Dict[str, Any]], bool]] = None
    ):
        """
        Add step to workflow

        Args:
            step_name: Unique step identifier
            agent: Agent to execute
            task_template: Task template (can use {variable} placeholders)
            depends_on: List of step names this depends on
            condition: Optional function that returns True if step should execute
        """
        if step_name in self.steps:
            raise ValueError(f"Step '{step_name}' already exists")

        # Validate dependencies
        depends_on = depends_on or []
        for dep in depends_on:
            if dep not in self.steps and dep != step_name:
                logger.warning(f"Dependency '{dep}' not yet added to workflow")

        self.steps[step_name] = WorkflowStep(
            agent=agent,
            task_template=task_template,
            depends_on=depends_on,
            condition=condition
        )

        logger.info(f"Added step '{step_name}' to workflow '{self.name}'")

    def execute(
        self,
        context: Optional[Dict[str, Any]] = None,
        max_retries: int = 2
    ) -> WorkflowResult:
        """
        Execute workflow

        Args:
            context: Initial context variables
            max_retries: Maximum retries per step on failure

        Returns:
            Workflow result
        """
        context = context or {}
        results = {}
        errors = {}
        execution_order = []

        logger.info(f"Starting workflow '{self.name}' with {len(self.steps)} steps")

        # Determine execution order (topological sort)
        try:
            execution_order = self._topological_sort()
        except ValueError as e:
            logger.error(f"Workflow has circular dependencies: {e}")
            return WorkflowResult(
                success=False,
                results={},
                errors={"workflow": str(e)},
                execution_order=[],
                total_steps=len(self.steps)
            )

        # Execute steps in order
        for step_name in execution_order:
            step = self.steps[step_name]

            # Check condition
            if step.condition and not step.condition(context):
                logger.info(f"Skipping step '{step_name}' (condition not met)")
                continue

            # Check dependencies
            deps_satisfied = all(dep in results for dep in step.depends_on)
            if not deps_satisfied:
                error_msg = f"Dependencies not satisfied: {step.depends_on}"
                logger.error(f"Step '{step_name}' failed: {error_msg}")
                errors[step_name] = error_msg
                continue

            # Build task from template
            task_context = {**context, **results}
            task = step.task_template.format(**task_context)

            # Execute with retries
            retry_count = 0
            while retry_count <= max_retries:
                try:
                    logger.info(f"Executing step '{step_name}' (attempt {retry_count + 1})")

                    result = step.agent.execute(task, task_context)
                    results[step_name] = result

                    logger.info(f"Step '{step_name}' completed successfully")
                    break

                except Exception as e:
                    retry_count += 1
                    logger.warning(f"Step '{step_name}' failed (attempt {retry_count}): {str(e)}")

                    if retry_count > max_retries:
                        errors[step_name] = str(e)
                        logger.error(f"Step '{step_name}' failed after {max_retries} retries")

        # Create result
        workflow_result = WorkflowResult(
            success=len(errors) == 0,
            results=results,
            errors=errors,
            execution_order=execution_order,
            total_steps=len(self.steps)
        )

        self.execution_history.append(workflow_result)

        logger.info(
            f"Workflow '{self.name}' completed: "
            f"{len(results)} successful, {len(errors)} failed"
        )

        return workflow_result

    def _topological_sort(self) -> List[str]:
        """
        Perform topological sort to determine execution order

        Returns:
            Ordered list of step names

        Raises:
            ValueError: If circular dependencies detected
        """
        # Build graph
        graph = {name: step.depends_on for name, step in self.steps.items()}

        # Kahn's algorithm
        in_degree = {name: len(deps) for name, deps in graph.items()}

        queue = [name for name, degree in in_degree.items() if degree == 0]
        result = []

        while queue:
            # Sort for consistent ordering
            queue.sort()
            node = queue.pop(0)
            result.append(node)

            # Reduce in-degree for dependent nodes
            for name, deps in graph.items():
                if node in deps:
                    in_degree[name] -= 1
                    if in_degree[name] == 0 and name not in result:
                        queue.append(name)

        if len(result) != len(graph):
            raise ValueError("Circular dependencies detected in workflow")

        return result

    def visualize(self) -> str:
        """
        Generate text visualization of workflow

        Returns:
            ASCII workflow diagram
        """
        lines = [f"Workflow: {self.name}", "=" * 50, ""]

        try:
            order = self._topological_sort()
        except ValueError:
            return "Error: Circular dependencies in workflow"

        for i, step_name in enumerate(order, 1):
            step = self.steps[step_name]
            agent_name = step.agent.config.name

            lines.append(f"{i}. {step_name}")
            lines.append(f"   Agent: {agent_name}")
            lines.append(f"   Task: {step.task_template}")

            if step.depends_on:
                lines.append(f"   Depends on: {', '.join(step.depends_on)}")

            if step.condition:
                lines.append(f"   Conditional: Yes")

            lines.append("")

        return "\n".join(lines)

    def get_stats(self) -> Dict[str, Any]:
        """
        Get workflow statistics

        Returns:
            Statistics dict
        """
        total_executions = len(self.execution_history)

        if total_executions == 0:
            return {
                "name": self.name,
                "total_steps": len(self.steps),
                "total_executions": 0,
                "success_rate": 0.0,
            }

        successful = sum(1 for r in self.execution_history if r.success)
        success_rate = successful / total_executions

        return {
            "name": self.name,
            "total_steps": len(self.steps),
            "total_executions": total_executions,
            "successful_executions": successful,
            "failed_executions": total_executions - successful,
            "success_rate": round(success_rate * 100, 2),
        }

    def clear_history(self):
        """Clear execution history"""
        self.execution_history = []
        logger.info(f"Cleared execution history for workflow '{self.name}'")

    def __str__(self) -> str:
        return f"AgentOrchestrator('{self.name}', {len(self.steps)} steps)"

    def __repr__(self) -> str:
        return f"<AgentOrchestrator: {self.name} with {len(self.steps)} steps>"
