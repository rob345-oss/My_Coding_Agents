"""Pluggable AI delegate helpers used to enhance agent outputs.

The delegate keeps this project lightweight while allowing orchestrators to
mix in LLM-backed improvements (e.g., LangChain, CrewAI, AutoGPT) when
available.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional


def _fallback_generator(report: str, context: Optional[List[str]] = None) -> str:
    """A deterministic summarizer used when no LLM is wired in."""

    context_hint = f"Context: {', '.join(context)}\n\n" if context else ""
    return context_hint + "AI-enhanced summary:\n- " + "\n- ".join(report.splitlines())


@dataclass
class AIDelegate:
    """Lightweight wrapper that can call into an LLM or heuristic enhancer."""

    generator: Callable[[str, Optional[List[str]]], str] = _fallback_generator

    def enhance(self, report: str, context: Optional[List[str]] = None) -> str:
        """Produce an AI-augmented report without changing core results."""

        return self.generator(report, context)
