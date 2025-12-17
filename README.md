# My_Coding_Agents

This repository hosts a suite of specialized coding agents designed to automate and safeguard software delivery. The agents can be orchestrated with frameworks such as LangChain, CrewAI, or AutoGPT while primarily coding in Python. Each persona exposes a pluggable AI delegate so you can layer in LLM-backed summarization or remediation guidance without changing the core agent interfaces.

## Agent roster

- **Lint Tester** — Runs lint and static analysis with a strict 5-minute check budget and a deterministic temperature of `0.2`.
- **SOC II Guardian** — Enforces SOC II-aligned controls by checking for secure ports, transport protections, and broader CIA (confidentiality, integrity, availability) considerations.
- **Dependency Steward** — Keeps dependency manifests consistent and compatible across environments, flagging drift or insecure versions.
- **Hallucination Sentinel** — Guards against fabricated responses by demanding verification, tests, and citations for generated outputs.
- **API Docsmith** — Produces and maintains API documentation so client teams have accurate references and examples.
- **TDD Enforcer** — Blocks risky merges unless tests accompany meaningful code changes and can optionally trigger fast feedback suites.

## Getting started

1. Create and activate a virtual environment (e.g., `python -m venv .venv && source .venv/bin/activate`).
2. Install your preferred orchestration stack, for example:
   ```bash
   pip install "langchain>=0.2" "crewai>=0.28" "autogptq-client>=0.4"
   ```
3. Import the agent configurations to bootstrap your workflows:
    ```python
    from agents import AGENTS, AIDelegate

    lint_agent = AGENTS["lint_tester"]
    lint_agent.ai_delegate = AIDelegate()  # swap in a LangChain/CrewAI generator when available
    ```

## Suggested workflow

1. Kick off the **Lint Tester** first to unblock style and static-analysis regressions.
2. Run the **Dependency Steward** to verify lockfiles and dependency compatibility.
3. Engage the **SOC II Guardian** to review secure defaults and CIA-aligned safeguards.
4. Use the **Hallucination Sentinel** to verify AI-generated content with tests or citations.
5. Publish outputs through the **API Docsmith** to keep downstream consumers up to date.
6. Gate impactful changes with the **TDD Enforcer** before merging.

## Triggering agents on the first Codex prompt

To ensure the full suite activates as soon as you start a session, wire a
`FirstPromptTrigger` to your Codex entrypoint. The helper runs the provided
callbacks only on the very first prompt, preventing duplicate work on
follow-up messages:

```python
from agents import FirstPromptTrigger, LintTester, DependencySteward, TDDEnforcer

lint = LintTester()
deps = DependencySteward()
tdd = TDDEnforcer()

trigger = FirstPromptTrigger(
    callbacks=[
        lambda prompt: lint.run(paths=["."]),
        lambda prompt: deps.reconcile(["requirements.txt", "poetry.lock"]),
        lambda prompt: tdd.audit_change_set([
            "src/app.py",
            "tests/test_app.py",
        ]),
    ]
)

# In your Codex prompt handler
reports = trigger(prompt_text)
```

The `reports` list collects the outputs from each agent. Because the trigger
short-circuits after the first call, it can be safely composed into any
orchestration pipeline without rerunning the suite on subsequent prompts.

## Enforcing test-driven development (TDD)

To keep high-signal changes honest, wire the **TDD Enforcer** into pre-merge automation:

1. Collect the files in the change set (e.g., `git diff --name-only origin/main...HEAD`) and feed them into the agent.
2. Let the agent flag code files that lack adjacent or discoverable tests. It proposes likely test paths such as `tests/test_*.py` or siblings like `test_<module>.py` so engineers can add coverage quickly.
3. Enable `run_tests=True` when you want a fast sanity suite (default: `pytest -q`) that fits inside CI budgets; configure a different command when you need framework-specific smoke tests.
4. Treat missing tests or failing smoke suites as a blocking check alongside linting and security gates.
5. Optionally attach an `AIDelegate` to generate actionable prompts (e.g., example assertions) for the flagged files, keeping the workflow AI-assisted while still enforcing deterministic checks.

## Notes

- Default agent temperatures prioritize determinism; tune them only when exploration is needed.
- The SOC II Guardian should enforce secure defaults (e.g., TLS, restricted ports) across services.
- Extend `agents/config.py` with additional metadata (tools, prompts, credentials) as your orchestration stack requires.
