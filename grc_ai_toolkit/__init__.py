"""
GRC AI Toolkit - Shared Foundation Module

A comprehensive toolkit for building AI-powered GRC (Governance, Risk, and Compliance) applications.
Provides reusable components for LLM integration, agent orchestration, data processing, and UI development.

Version: 1.0.0
Author: Anusha Cabral
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Anusha Cabral"
__email__ = "cabral.anusha@gmail.com"

# Import main components for easy access
from .llm import LLMManager, PromptTemplate
from .agents import BaseAgent, AgentOrchestrator
from .data import DataProcessor, VectorStore
from .ui import StreamlitComponents

__all__ = [
    "LLMManager",
    "PromptTemplate",
    "BaseAgent",
    "AgentOrchestrator",
    "DataProcessor",
    "VectorStore",
    "StreamlitComponents",
]
