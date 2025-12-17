"""Common agent primitives used across the suite."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Optional

from .config import AgentConfig
from .ai_delegate import AIDelegate


def _now() -> float:
    return time.monotonic()


@dataclass
class BaseAgent:
    """Minimal base class to provide timing and metadata helpers."""

    config: AgentConfig
    clock: Callable[[], float] = field(default=_now)
    ai_delegate: Optional[AIDelegate] = None

    def describe(self) -> str:
        """Return a human-readable summary of the agent persona."""

        goals = "\n- ".join(self.config.goals)
        return (
            f"Agent: {self.config.name}\n"
            f"Role: {self.config.role}\n"
            f"Goals:\n- {goals}\n"
            f"Temperature: {self.config.temperature}\n"
            f"Time budget: {self.config.time_limit_minutes} minutes"
        )

    def deliver(self, report: str, context: Optional[list[str]] = None) -> str:
        """Optionally enhance the report with AI assistance for richer output.

        The `ai_delegate` is intentionally pluggable so orchestrators can wire in
        LLM-backed summarization or action-item generation without changing the
        core agent behaviors.
        """

        if self.ai_delegate is None:
            return report
        return self.ai_delegate.enhance(report=report, context=context)

    def run_with_deadline(self, minutes: Optional[int], operation: Callable[[], str]) -> str:
        """Run an operation while enforcing the configured time budget.

        Args:
            minutes: Override for the time limit in minutes. If None, uses the
                value from the agent config.
            operation: Callable that performs the agent's main action and
                returns a textual report.

        Returns:
            The operation's string result.

        Raises:
            TimeoutError: If the operation exceeds the allotted time.
        """

        deadline_minutes = minutes if minutes is not None else self.config.time_limit_minutes
        time_limit_seconds = deadline_minutes * 60
        start = self.clock()
        result = operation()
        duration = self.clock() - start
        if duration > time_limit_seconds:
            raise TimeoutError(
                f"Agent '{self.config.name}' exceeded the {deadline_minutes}-minute budget (took {duration:.1f}s)."
            )
        return result
