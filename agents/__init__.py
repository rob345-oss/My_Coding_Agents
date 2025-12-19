"""Agent modules for the My_Coding_Agents suite.

This package exposes ready-to-use agent classes aligned with the personas
outlined in the README. Each agent ships with a focused interface to keep
orchestration frameworks free of boilerplate.
"""

from .ai_delegate import AIDelegate
from .api_docsmith import APIDocsmith
from .base import BaseAgent
from .config import AGENTS, AgentConfig
from .dependency_steward import DependencySteward
from .hallucination_sentinel import HallucinationSentinel
from .first_prompt_trigger import FirstPromptTrigger
from .lint_tester import LintTester
from .socii_guardian import SOCIIGuardian
from .tdd_enforcer import TDDEnforcer

__all__ = [
    "AIDelegate",
    "AGENTS",
    "APIDocsmith",
    "BaseAgent",
    "DependencySteward",
    "FirstPromptTrigger",
    "HallucinationSentinel",
    "LintTester",
    "AgentConfig",
    "SOCIIGuardian",
    "TDDEnforcer",
]
