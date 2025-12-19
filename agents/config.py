"""Agent configuration blueprints for My_Coding_Agents.

This module centralizes the agent roles and default runtime parameters.
The configs can be consumed by orchestration frameworks such as LangChain,
CrewAI, or AutoGPT without tying the repo to a specific runtime.
"""
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AgentConfig:
    """Declarative settings for a single agent persona."""

    name: str
    role: str
    goals: List[str]
    temperature: float = 0.2
    time_limit_minutes: int = 5


AGENTS: Dict[str, AgentConfig] = {
    "lint_tester": AgentConfig(
        name="Lint Tester",
        role="Run linting and static analysis with a tight feedback loop.",
        goals=[
            "Complete lint and style checks within a 5-minute budget.",
            "Keep model temperature deterministic for consistent results.",
            "Report actionable fixes for any violations encountered.",
        ],
        temperature=0.2,
        time_limit_minutes=5,
    ),
    "socii_guardian": AgentConfig(
        name="SOC II Guardian",
        role="Ensure code changes align with SOC II-aligned security posture.",
        goals=[
            "Validate secure port usage and transport security defaults.",
            "Review code for confidentiality, integrity, and availability (CIA) safeguards.",
            "Flag deviations from SOC II control expectations before release.",
        ],
        temperature=0.2,
        time_limit_minutes=10,
    ),
    "dependency_steward": AgentConfig(
        name="Dependency Steward",
        role="Keep dependency manifests synchronized and conflict-free.",
        goals=[
            "Detect version drift across lockfiles and requirement specs.",
            "Surface insecure or deprecated packages before integration.",
            "Recommend compatible upgrades and resolution steps.",
        ],
        temperature=0.2,
        time_limit_minutes=10,
    ),
    "hallucination_sentinel": AgentConfig(
        name="Hallucination Sentinel",
        role="Guardrail the AI outputs against fabricated or unverifiable claims.",
        goals=[
            "Cross-check responses against source material or tests.",
            "Demand citations and verification steps for generated answers.",
            "Fail closed when evidence is insufficient to support a claim.",
        ],
        temperature=0.2,
        time_limit_minutes=10,
    ),
    "api_docsmith": AgentConfig(
        name="API Docsmith",
        role="Generate and maintain API documentation for exposed services.",
        goals=[
            "Draft concise, versioned API references with examples.",
            "Keep changelogs in sync with implementation updates.",
            "Publish guidance that is ready for client and partner consumption.",
        ],
        temperature=0.4,
        time_limit_minutes=10,
    ),
    "tdd_enforcer": AgentConfig(
        name="TDD Enforcer",
        role="Champion test-driven development on impactful changes.",
        goals=[
            "Require tests to accompany high-value code changes.",
            "Surface missing or weak coverage before merging.",
            "Optionally run fast feedback test suites within CI budgets.",
        ],
        temperature=0.2,
        time_limit_minutes=12,
    ),
}
