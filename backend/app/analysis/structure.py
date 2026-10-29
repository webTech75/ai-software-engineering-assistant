"""
Analyzer for extracting project file structure information.

Author: Amr Elhabbal | Powered by Meta AI Muse
"""

from pathlib import Path

from app.analysis.base import BaseAnalyzer
from app.utils.should_ignore import should_ignore


class StructureAnalyzer(BaseAnalyzer):

    def analyze(self, project_directory: str) -> dict:

        root = Path(project_directory)

        files = []

        for path in root.rglob("*"):

            # Skip ignored directories and their contents
            if should_ignore(path):
                continue

            if path.is_file():
                files.append(str(path.relative_to(root)))

        return {
            "structure": {
                "files": sorted(files),
            }
        }
