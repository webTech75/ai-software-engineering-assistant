"""
Analyzer for detecting and reporting project API endpoints.

Author: Amr Elhabbal | Powered by Meta AI Muse
"""

from pathlib import Path
import re

from app.analysis.base import BaseAnalyzer
from app.utils.should_ignore import should_ignore


class APIAnalyzer(BaseAnalyzer):
    """
    Analyze project API endpoints.
    """

    HTTP_METHODS = [
        "get",
        "post",
        "put",
        "patch",
        "delete",
    ]

    def analyze(self, project_directory: str) -> dict:

        root = Path(project_directory)

        routes = []

        for path in root.rglob("*.py"):

            if should_ignore(path):
                continue

            try:
                content = path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

            except Exception:
                continue

            for method in self.HTTP_METHODS:

                pattern = rf"@.*\.{method}\(" r"[\"'](.*?)[\"']"

                matches = re.findall(
                    pattern,
                    content,
                )

                for route in matches:

                    routes.append(
                        {
                            "method": method.upper(),
                            "path": route,
                            "file": str(path.relative_to(root)),
                        }
                    )

        return {
            "api": {
                "total_routes": len(routes),
                "routes": routes,
            }
        }
