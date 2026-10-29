"""
Analyzer for collecting basic project statistics and file metrics.

Author: Amr Elhabbal | Powered by Meta AI Muse
"""

from pathlib import Path

from app.analysis.base import BaseAnalyzer
from app.utils.should_ignore import should_ignore


class StatisticsAnalyzer(BaseAnalyzer):
    """
    Collect basic statistics about a project.
    """

    def analyze(self, project_directory: str) -> dict:

        root = Path(project_directory)

        total_files = 0
        total_directories = 0
        extensions = {}

        total_size = 0
        largest_file = None
        largest_size = 0

        for path in root.rglob("*"):

            if should_ignore(path):
                continue

            if path.is_dir():
                total_directories += 1
                continue

            total_files += 1

            extension = path.suffix.lower()

            extensions[extension] = extensions.get(extension, 0) + 1

            try:
                size = path.stat().st_size

            except Exception:
                continue

            total_size += size

            if size > largest_size:
                largest_size = size
                largest_file = str(path.relative_to(root))

        average_size = total_size / total_files if total_files else 0

        return {
            "statistics": {
                "total_files": total_files,
                "total_directories": total_directories,
                "extensions": extensions,
                "total_size": total_size,
                "average_file_size": round(
                    average_size,
                    2,
                ),
                "largest_file": largest_file,
                "largest_file_size": largest_size,
            }
        }
