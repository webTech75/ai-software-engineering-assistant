from pathlib import Path

from app.analysis.base import BaseAnalyzer
from app.analysis.constants import IGNORED_DIRECTORIES, IGNORED_EXTENSIONS


class StructureAnalyzer(BaseAnalyzer):
    

    def analyze(self, project_directory: str) -> dict:

        root = Path(project_directory)

        files = []

        for path in root.rglob("*"):

            # Skip ignored directories and their contents
            if any(part in IGNORED_DIRECTORIES for part in path.parts):
                continue

            if (
                path.is_file()
                and path.suffix.lower() in IGNORED_EXTENSIONS
            ):
                continue


            if path.is_file():
                files.append(str(path.relative_to(root)))

        return {
            "structure": {
                "files": sorted(files),
            }
        }