"""
Analyzer for detecting project dependencies and package managers.

Author: Amr Elhabbal | Powered by Meta AI Muse
"""

from pathlib import Path

from app.analysis.base import BaseAnalyzer


class DependencyAnalyzer(BaseAnalyzer):
    """
    Analyze project dependencies.
    """

    def analyze(self, project_directory: str) -> dict:
        """
        Detect project dependency files and packages.
        """

        root = Path(project_directory)

        dependencies = []
        manager = None
        dependency_file = None

        # Python dependencies
        requirements_files = list(root.rglob("requirements.txt"))

        if requirements_files:

            requirements = requirements_files[0]

            manager = "pip"
            dependency_file = "requirements.txt"

            content = requirements.read_text(
                encoding="utf-8",
                errors="ignore",
            ).splitlines()

            for line in content:

                line = line.strip()

                if line and not line.startswith("#"):
                    dependencies.append(line)

        # Node dependencies
        package_files = list(root.rglob("package.json"))

        if package_files:

            manager = "npm"
            dependency_file = "package.json"

            dependencies.append("package.json detected")

        return {
            "dependencies": {
                "manager": manager,
                "file": dependency_file,
                "total": len(dependencies),
                "packages": sorted(dependencies),
            }
        }
