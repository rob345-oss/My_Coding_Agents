"""Lint Tester agent implementation."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Iterable, List, Sequence

from .base import BaseAgent
from .config import AGENTS


class LintTester(BaseAgent):
    """Run linting and static analysis within a strict time budget."""

    DEFAULT_COMMAND: Sequence[str] = ("ruff", "check")

    def __init__(self, command: Sequence[str] | None = None):
        super().__init__(config=AGENTS["lint_tester"])
        self.command: Sequence[str] = command or self.DEFAULT_COMMAND

    def run(self, paths: Iterable[str | Path]) -> str:
        """Execute linting against the provided paths.

        Args:
            paths: Files or directories to lint.

        Returns:
            Combined stdout/stderr from the lint command.
        """

        path_args: List[str] = [str(Path(p)) for p in paths]
        if not path_args:
            raise ValueError("No paths provided for linting.")

        def _operation() -> str:
            completed = subprocess.run(
                [*self.command, *path_args],
                check=False,
                capture_output=True,
                text=True,
                timeout=self.config.time_limit_minutes * 60,
            )
            output = completed.stdout + completed.stderr
            if completed.returncode != 0:
                return f"Linting completed with issues (exit {completed.returncode}):\n{output}"
            return f"Linting succeeded:\n{output}"

        report = self.run_with_deadline(minutes=None, operation=_operation)
        return self.deliver(report, context=["lint", "static analysis"])
