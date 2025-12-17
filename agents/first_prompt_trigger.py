"""Utilities to fire agents automatically on the first Codex prompt."""

from __future__ import annotations

from typing import Callable, List, Sequence

PromptHandler = Callable[[str], str]


class FirstPromptTrigger:
    """Ensure agent callbacks run exactly once on the first user prompt.

    Initialize with a set of callbacks that accept the initial prompt text and
    return string reports (for example, the output of an agent's run method).
    When invoked, the trigger executes each callback the first time and caches
    that it has fired so subsequent prompts do not re-run the callbacks.
    """

    def __init__(self, callbacks: Sequence[PromptHandler]):
        if not callbacks:
            raise ValueError("Provide at least one callback to trigger.")
        self._callbacks: List[PromptHandler] = list(callbacks)
        self._fired: bool = False

    @property
    def fired(self) -> bool:
        """Return whether the trigger has already executed the callbacks."""

        return self._fired

    def __call__(self, prompt: str) -> List[str]:
        """Execute callbacks on the first prompt and return their reports."""

        if self._fired:
            return []
        self._fired = True
        return [callback(prompt) for callback in self._callbacks]
