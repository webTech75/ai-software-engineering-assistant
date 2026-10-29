"""
Analyzer for detecting project testing setup.

Identifies test files and testing frameworks.

Author:
    Amr Elhabbal
    Powered by Meta AI Muse
"""

from pathlib import Path

from app.analysis.base import BaseAnalyzer
from app.utils.should_ignore import should_ignore


class TestAnalyzer(BaseAnalyzer):
    """
    Analyze project testing setup.
    """

    def analyze(self, project_directory: str) -> dict:
        """
        Detect test files and testing frameworks.
        """

        root = Path(project_directory)

        test_files = []
        frameworks = []

        for path in root.rglob("*"):

            if should_ignore(path):
                continue

            if not path.is_file():
                continue

            file_name = path.name.lower()

            if file_name.startswith("test_") or file_name.endswith("_test.py"):
                test_files.append(str(path.relative_to(root)))

        # Python testing framework detection
        requirements_files = list(root.rglob("requirements.txt"))

        for requirements in requirements_files:

            try:
                content = requirements.read_text(
                    encoding="utf-8",
                    errors="ignore",
                ).lower()

            except Exception:
                continue

            if "pytest" in content:
                frameworks.append("pytest")

            if "unittest" in content:
                frameworks.append("unittest")

        return {
            "tests": {
                "exists": len(test_files) > 0,
                "frameworks": sorted(set(frameworks)),
                "total_test_files": len(test_files),
                "files": sorted(test_files),
            }
        }
