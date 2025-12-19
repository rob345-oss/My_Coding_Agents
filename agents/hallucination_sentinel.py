"""Hallucination Sentinel agent implementation."""

from __future__ import annotations

from typing import Iterable, List, Mapping

from .base import BaseAgent
from .config import AGENTS


class HallucinationSentinel(BaseAgent):
    """Guardrail AI outputs with verification and citation checks."""

    def __init__(self):
        super().__init__(config=AGENTS["hallucination_sentinel"])

    def verify_claims(self, claims: Iterable[str], evidence: Mapping[str, List[str]]) -> str:
        """Require evidence for each claim.

        Args:
            claims: Claims to validate.
            evidence: Mapping of claim -> supporting evidence snippets.
        """

        missing: List[str] = []
        summary_lines: List[str] = []
        for claim in claims:
            support = evidence.get(claim, [])
            if not support:
                missing.append(claim)
                continue
            summary_lines.append(f"{claim}: supported by {len(support)} citation(s)")

        report_sections: List[str] = []
        if summary_lines:
            report_sections.append("Validated claims:\n- " + "\n- ".join(summary_lines))
        if missing:
            report_sections.append("Claims lacking evidence:\n- " + "\n- ".join(missing))

        report = "\n\n".join(report_sections) if report_sections else "No claims provided for verification."
        return self.deliver(report, context=["hallucination", "verification"])

    def gate_response(self, response: str, contains_evidence: bool) -> str:
        """Fail closed when a response lacks citations or tests."""

        if not response:
            report = "Response blocked: empty content."
        elif not contains_evidence:
            report = "Response blocked: insufficient evidence or citations detected."
        else:
            report = "Response approved for delivery."
        return self.deliver(report, context=["hallucination", "gating"])
