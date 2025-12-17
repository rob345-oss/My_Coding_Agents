"""SOC II Guardian agent implementation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Mapping

from .base import BaseAgent
from .config import AGENTS


@dataclass
class ServicePort:
    name: str
    port: int
    tls_required: bool = True


class SOCIIGuardian(BaseAgent):
    """Review services for SOC II-aligned security posture."""

    def __init__(self):
        super().__init__(config=AGENTS["socii_guardian"])

    def review_ports(self, services: Iterable[ServicePort]) -> str:
        """Check whether services rely on secure, expected ports."""

        findings: List[str] = []
        for service in services:
            if service.port in {80, 21, 23}:
                findings.append(
                    f"{service.name}: port {service.port} is insecure; prefer TLS (443/8443) or tunneled access."
                )
            if not service.tls_required:
                findings.append(f"{service.name}: TLS not required; enforce TLS for confidentiality and integrity.")

        if not findings:
            report = "All services are using secure ports with TLS enforced."
        else:
            report = "Security review findings:\n- " + "\n- ".join(findings)
        return self.deliver(report, context=["soc2", "network", "cia"])

    def review_controls(self, controls: Mapping[str, bool]) -> str:
        """Evaluate CIA-aligned control checks."""

        missing = [name for name, passed in controls.items() if not passed]
        if not missing:
            report = "All evaluated controls meet SOC II expectations."
        else:
            report = "SOC II control gaps detected:\n- " + "\n- ".join(missing)
        return self.deliver(report, context=["soc2", "controls", "cia"])
