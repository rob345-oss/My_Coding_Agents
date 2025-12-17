"""TDD Enforcer agent implementation."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Iterable, List, Sequence

from .base import BaseAgent
from .config import AGENTS


class TDDEnforcer(BaseAgent):
    """Promote test-driven development for significant code changes."""

    DEFAULT_TEST_COMMAND: Sequence[str] = ("pytest", "-q")

    def __init__(self, test_command: Sequence[str] | None = None):
        super().__init__(config=AGENTS["tdd_enforcer"])
        self.test_command: Sequence[str] = test_command or self.DEFAULT_TEST_COMMAND

    def _expected_tests(self, code_path: Path) -> List[Path]:
        """Return likely test file locations for a given code file."""

        stem = code_path.stem
        return [
            code_path.parent / f"test_{stem}{code_path.suffix}",
            code_path.parent / f"{stem}_test{code_path.suffix}",
            Path("tests") / code_path.parent.name / f"test_{stem}{code_path.suffix}",
            Path("tests") / f"test_{stem}{code_path.suffix}",
        ]

    def review(self, changed_files: Iterable[str | Path], run_tests: bool = False) -> str:
        """Assess whether changes adhere to TDD expectations.

        Args:
            changed_files: Files touched in the change set.
            run_tests: If True, execute the configured fast-feedback test command.

        Returns:
            A report describing coverage posture and optional test results.
        """

        paths: List[Path] = [Path(p) for p in changed_files]
        if not paths:
            raise ValueError("No files provided to review.")

        test_paths: List[Path] = [p for p in paths if "test" in p.name.lower() or "tests" in p.parts]
        code_paths: List[Path] = [p for p in paths if p not in test_paths]

        missing_tests: List[str] = []
        found_tests: List[str] = [str(p) for p in test_paths]

        for code_path in code_paths:
            expected = self._expected_tests(code_path)
            discovered = [p for p in expected if p.exists()]
            if not discovered and not any(code_path.stem in t.name for t in test_paths):
                missing_tests.extend(str(p) for p in expected)

        lines: List[str] = [
            f"Reviewed {len(paths)} files (code: {len(code_paths)}, tests: {len(test_paths)}).",
        ]

        if found_tests:
            lines.append("Detected test coverage in: " + ", ".join(sorted(found_tests)))
        else:
            lines.append("No test files detected in the change set.")

        if missing_tests:
            unique_missing = sorted(set(missing_tests))
            lines.append("Add or update tests at likely locations:")
            lines.extend(f"- {path}" for path in unique_missing)
        else:
            lines.append("All code changes appear to have adjacent or discoverable tests.")

        if run_tests:
            def _operation() -> str:
                completed = subprocess.run(
                    self.test_command,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=self.config.time_limit_minutes * 60,
                )
                summary = completed.stdout + completed.stderr
                if completed.returncode != 0:
                    return f"Fast-feedback tests failed (exit {completed.returncode}).\n{summary}"
                return f"Fast-feedback tests passed.\n{summary}"

            test_report = self.run_with_deadline(minutes=None, operation=_operation)
            lines.append(test_report)
        else:
            lines.append("Tests were not executed; enable run_tests=True for fast feedback.")

        report = "\n".join(lines)
        return self.deliver(report, context=["tdd", "tests", "coverage"])
