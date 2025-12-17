"""Dependency Steward agent implementation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Mapping

from .base import BaseAgent
from .config import AGENTS


@dataclass
class DependencySpec:
    name: str
    version: str
    source: str


class DependencySteward(BaseAgent):
    """Validate that dependency manifests remain consistent and secure."""

    def __init__(self):
        super().__init__(config=AGENTS["dependency_steward"])

    def detect_drift(self, manifests: Iterable[Mapping[str, str]]) -> str:
        """Find version drift across multiple manifests."""

        consolidated: dict[str, set[str]] = {}
        for manifest in manifests:
            for package, version in manifest.items():
                consolidated.setdefault(package, set()).add(version)

        drift = {pkg: versions for pkg, versions in consolidated.items() if len(versions) > 1}
        if not drift:
            report = "No version drift detected across manifests."
        else:
            lines = [f"{pkg}: {', '.join(sorted(versions))}" for pkg, versions in sorted(drift.items())]
            report = "Version drift detected:\n- " + "\n- ".join(lines)
        return self.deliver(report, context=["dependencies", "compatibility"])

    def flag_insecure(self, advisories: Mapping[str, List[str]], specs: Iterable[DependencySpec]) -> str:
        """Highlight dependencies with known issues."""

        findings: List[str] = []
        for spec in specs:
            vulnerable_versions = advisories.get(spec.name, [])
            if spec.version in vulnerable_versions:
                findings.append(
                    f"{spec.name} {spec.version} from {spec.source} is flagged by advisories; consider updating."
                )

        if not findings:
            report = "All dependencies passed advisory checks."
        else:
            report = "Insecure dependencies found:\n- " + "\n- ".join(findings)
        return self.deliver(report, context=["dependencies", "security"])
