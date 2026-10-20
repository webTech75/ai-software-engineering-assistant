from pathlib import Path

from app.analysis.base import BaseAnalyzer
from app.analysis.constants import IGNORED_DIRECTORIES


class BugAnalyzer(BaseAnalyzer):
    """
    Analyze a project for potential bugs.
    """

    def analyze(self, project_directory: str) -> dict:

        root = Path(project_directory)

        bugs = []

        for path in root.rglob("*"):

            if any(
                part in IGNORED_DIRECTORIES
                for part in path.parts
            ):
                continue

            if not path.is_file():
                continue

            if path.suffix != ".py":
                continue

            try:
                lines = path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                ).splitlines()

            except Exception:
                continue

            bugs.extend(
                self._find_todos(path, root, lines)
            )

            bugs.extend(
                self._find_fixmes(path, root, lines)
            )

        return {
            "bugs": {
                "count": len(bugs),
                "issues": bugs
            }
        }

    def _find_todos(
        self,
        path: Path,
        root: Path,
        lines: list[str],
    ) -> list[dict]:

        findings = []

        for line_number, line in enumerate(
            lines,
            start=1,
        ):

            if "TODO" in line.upper():

                findings.append({
                    "type": "TODO",
                    "severity": "LOW",
                    "file": str(path.relative_to(root)),
                    "line": line_number,
                    "message": "TODO comment found.",
                })

        return findings

    def _find_fixmes(
        self,
        path: Path,
        root: Path,
        lines: list[str],
    ) -> list[dict]:

        findings = []

        for line_number, line in enumerate(
            lines,
            start=1,
        ):

            if "FIXME" in line.upper():

                findings.append({
                    "type": "FIXME",
                    "severity": "MEDIUM",
                    "file": str(path.relative_to(root)),
                    "line": line_number,
                    "message": "FIXME comment found.",
                })

        return findings