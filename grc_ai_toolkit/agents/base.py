"""
Base Agent Class for GRC AI Systems
"""

from typing import Dict, Any, Optional, List, TypedDict
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import logging

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.runnables import RunnableConfig

from ..llm import LLMManager


logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Configuration for individual agents"""

    name: str
    description: str
    system_message: str
    llm_manager: Optional[LLMManager] = None

    # Agent-specific settings
    temperature: float = 0.7
    max_iterations: int = 5
    verbose: bool = False

    # Tool/function access
    available_tools: List[str] = field(default_factory=list)

    # Memory settings
    enable_memory: bool = True
    max_memory_messages: int = 10


class AgentState(TypedDict):
    """
    State structure for agents (LangChain 1.0 pattern using TypedDict)
    """
    messages: List[Dict[str, Any]]
    current_task: str
    context: Dict[str, Any]
    iteration_count: int
    status: str  # "in_progress", "completed", "failed"
    result: Optional[str]


class BaseAgent(ABC):
    """
    Abstract base class for all GRC agents

    Follows LangChain 1.0 patterns with TypedDict-based state management.

    Example:
        class PolicyDraftingAgent(BaseAgent):
            def execute(self, task: str, context: Dict[str, Any]) -> str:
                # Implementation
                pass
    """

    def __init__(self, config: AgentConfig):
        """
        Initialize agent

        Args:
            config: Agent configuration
        """
        self.config = config
        self.llm_manager = config.llm_manager

        # Initialize state
        self.state: AgentState = {
            "messages": [],
            "current_task": "",
            "context": {},
            "iteration_count": 0,
            "status": "idle",
            "result": None,
        }

        logger.info(f"Initialized {self.config.name}")

    @abstractmethod
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Execute the agent's primary task

        Args:
            task: Task description
            context: Additional context for the task

        Returns:
            Task result
        """
        pass

    def _prepare_prompt(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Prepare prompt with system message and context

        Args:
            task: Task description
            context: Additional context

        Returns:
            Formatted prompt
        """
        context = context or {}

        # Build context string
        context_str = ""
        if context:
            context_str = "\n\nContext:\n"
            for key, value in context.items():
                context_str += f"- {key}: {value}\n"

        # Combine with task
        prompt = f"{task}{context_str}"

        return prompt

    def _update_state(
        self,
        task: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        status: Optional[str] = None,
        result: Optional[str] = None,
        increment_iteration: bool = False
    ):
        """
        Update agent state

        Args:
            task: New task (if any)
            context: Context updates
            status: New status
            result: Task result
            increment_iteration: Whether to increment iteration count
        """
        if task:
            self.state["current_task"] = task

        if context:
            self.state["context"].update(context)

        if status:
            self.state["status"] = status

        if result:
            self.state["result"] = result

        if increment_iteration:
            self.state["iteration_count"] += 1

    def _add_message(self, role: str, content: str):
        """
        Add message to state history

        Args:
            role: Message role ("system", "user", "assistant")
            content: Message content
        """
        self.state["messages"].append({
            "role": role,
            "content": content,
        })

        # Trim messages if exceeding max
        if len(self.state["messages"]) > self.config.max_memory_messages:
            # Keep system message and recent messages
            system_msgs = [m for m in self.state["messages"] if m["role"] == "system"]
            recent_msgs = self.state["messages"][-self.config.max_memory_messages:]
            self.state["messages"] = system_msgs + recent_msgs

    def reset_state(self):
        """Reset agent state to initial values"""
        self.state = {
            "messages": [],
            "current_task": "",
            "context": {},
            "iteration_count": 0,
            "status": "idle",
            "result": None,
        }
        logger.debug(f"Reset state for {self.config.name}")

    def get_state_summary(self) -> Dict[str, Any]:
        """
        Get summary of current agent state

        Returns:
            State summary dict
        """
        return {
            "name": self.config.name,
            "status": self.state["status"],
            "current_task": self.state["current_task"],
            "iteration_count": self.state["iteration_count"],
            "message_count": len(self.state["messages"]),
            "has_result": self.state["result"] is not None,
        }

    def __str__(self) -> str:
        return f"{self.config.name} ({self.state['status']})"

    def __repr__(self) -> str:
        return f"<BaseAgent: {self.config.name}>"


class SimpleAgent(BaseAgent):
    """
    Simple agent that executes a single LLM call

    Useful for straightforward tasks without complex orchestration.

    Example:
        agent = SimpleAgent(AgentConfig(
            name="summarizer",
            description="Summarizes documents",
            system_message="You are a document summarization expert.",
            llm_manager=llm_manager
        ))

        result = agent.execute("Summarize this policy document", {
            "document": policy_text
        })
    """

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Execute task with single LLM call

        Args:
            task: Task description
            context: Additional context

        Returns:
            LLM response
        """
        self._update_state(task=task, context=context, status="in_progress")

        try:
            # Prepare prompt
            prompt = self._prepare_prompt(task, context)

            # Add to message history
            self._add_message("system", self.config.system_message)
            self._add_message("user", prompt)

            # Generate response
            response = self.llm_manager.generate(
                prompt=prompt,
                system_message=self.config.system_message,
                temperature=self.config.temperature
            )

            # Add response to history
            self._add_message("assistant", response)

            # Update state
            self._update_state(
                status="completed",
                result=response,
                increment_iteration=True
            )

            logger.info(f"{self.config.name} completed task")

            return response

        except Exception as e:
            logger.error(f"{self.config.name} failed: {str(e)}")
            self._update_state(status="failed", result=str(e))
            raise
