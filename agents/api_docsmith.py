"""API Docsmith agent implementation."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Mapping

from .base import BaseAgent
from .config import AGENTS


class APIDocsmith(BaseAgent):
    """Produce concise API documentation artifacts."""

    def __init__(self):
        super().__init__(config=AGENTS["api_docsmith"])

    def generate_markdown(self, endpoints: Iterable[Mapping[str, str]], output_path: str | Path) -> str:
        """Generate a simple Markdown reference for the provided endpoints."""

        output_path = Path(output_path)
        lines: List[str] = ["# API Reference", ""]
        for endpoint in endpoints:
            name = endpoint.get("name", "Unnamed Endpoint")
            method = endpoint.get("method", "GET")
            path = endpoint.get("path", "/")
            description = endpoint.get("description", "No description provided.")
            lines.extend([f"## {name}", f"**Method:** `{method}`", f"**Path:** `{path}`", "", description, ""])

        output_path.write_text("\n".join(lines))
        report = f"Wrote documentation to {output_path}"
        return self.deliver(report, context=["api", "docs"])

    def summarize_changes(self, changelog: Iterable[str]) -> str:
        """Create a changelog summary for clients."""

        bullet_points = "\n- ".join(changelog)
        if not bullet_points:
            report = "No changes to report."
        else:
            report = "API changes:\n- " + bullet_points
        return self.deliver(report, context=["api", "changelog"])
