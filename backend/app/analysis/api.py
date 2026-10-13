from pathlib import Path
import re

from app.analysis.base import BaseAnalyzer
from app.analysis.constants import IGNORED_DIRECTORIES


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

            if any(
                part in IGNORED_DIRECTORIES
                for part in path.parts
            ):
                continue

            try:
                content = path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

            except Exception:
                continue


            for method in self.HTTP_METHODS:

                pattern = (
                    rf"@.*\.{method}\("
                    r"[\"'](.*?)[\"']"
                )

                matches = re.findall(
                    pattern,
                    content,
                )

                for route in matches:

                    routes.append(
                        {
                            "method": method.upper(),
                            "path": route,
                            "file": str(
                                path.relative_to(root)
                            ),
                        }
                    )


        return {
            "api": {
                "total_routes": len(routes),
                "routes": routes,
            }
        }