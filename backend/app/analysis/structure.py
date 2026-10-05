from pathlib import Path

from app.analysis.base import BaseAnalyzer


class StructureAnalyzer(BaseAnalyzer):
    """
    Analyze the directory structure of a project.
    """

    def analyze(self, project_directory: str) -> dict:

        root = Path(project_directory)

        directories = []
        files = []

        for path in root.rglob("*"):

            relative_path = str(path.relative_to(root))

            if path.is_dir():
                directories.append(relative_path)
            else:
                files.append(relative_path)

        return {
            "structure": {
                "directories": sorted(directories),
                "files": sorted(files),
            }
        }