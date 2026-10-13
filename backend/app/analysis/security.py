from pathlib import Path

from app.analysis.base import BaseAnalyzer
from app.analysis.constants import IGNORED_DIRECTORIES


class SecurityAnalyzer(BaseAnalyzer):
    """
    Analyze a project for basic security issues.
    """

    DANGEROUS_PATTERNS = {
        "eval(": {
            "type": "DANGEROUS_FUNCTION",
            "severity": "HIGH",
            "message": "Use of eval() can execute unsafe code.",
        },
        "exec(": {
            "type": "DANGEROUS_FUNCTION",
            "severity": "HIGH",
            "message": "Use of exec() can execute unsafe code.",
        },
    }

    SECRET_PATTERNS = {
        "password =": {
            "type": "HARDCODED_SECRET",
            "severity": "HIGH",
            "message": "Possible hardcoded password found.",
        },
        "secret =": {
            "type": "HARDCODED_SECRET",
            "severity": "HIGH",
            "message": "Possible hardcoded secret found.",
        },
        "api_key =": {
            "type": "HARDCODED_SECRET",
            "severity": "HIGH",
            "message": "Possible hardcoded API key found.",
        },
    }

    def analyze(self, project_directory: str) -> dict:
        """
        Scan Python files for basic security issues.
        """

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

            for line_number, line in enumerate(
                lines,
                start=1,
            ):
                lower_line = line.lower()

                for pattern, details in self.DANGEROUS_PATTERNS.items():
                    if pattern in line:
                        findings.append({
                            **details,
                            "file": str(path.relative_to(root)),
                            "line": line_number,
                        })

                for pattern, details in self.SECRET_PATTERNS.items():
                    if pattern in lower_line:
                        findings.append({
                            **details,
                            "file": str(path.relative_to(root)),
                            "line": line_number,
                        })

        return {
            "security": findings
        }