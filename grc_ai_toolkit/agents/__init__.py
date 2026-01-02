"""
AI Agent Components

Provides base agent classes and orchestration for multi-agent GRC systems.
"""

from .base import BaseAgent, AgentConfig
from .orchestrator import AgentOrchestrator
from .templates import (
    ResearchAgent,
    AnalysisAgent,
    GenerationAgent,
    ReviewAgent,
)

__all__ = [
    "BaseAgent",
    "AgentConfig",
    "AgentOrchestrator",
    "ResearchAgent",
    "AnalysisAgent",
    "GenerationAgent",
    "ReviewAgent",
]
