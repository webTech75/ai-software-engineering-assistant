from pathlib import Path

from app.analysis.base import BaseAnalyzer
from app.analysis.constants import IGNORED_DIRECTORIES


class CodeQualityAnalyzer(BaseAnalyzer):
    """
    Analyze code quality issues in a project.
    """

    MAX_FILE_LINES = 50

    def analyze(self, project_directory: str) -> dict:

        root = Path(project_directory)

        findings = []

        for path in root.rglob("*.py"):

            if any(
                part in IGNORED_DIRECTORIES
                for part in path.parts
            ):
                continue

            try:
                lines = path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                ).splitlines()

            except Exception:
                continue

            if len(lines) > self.MAX_FILE_LINES:

                findings.append({
                    "type": "LARGE_FILE",
                    "severity": "MEDIUM",
                    "file": str(path.relative_to(root)),
                    "line": None,
                    "message": (
                        f"File contains {len(lines)} lines. "
                        "Consider splitting it."
                    ),
                })

        return {
            "code_quality": findings
        }