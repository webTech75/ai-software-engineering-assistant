"""
Handles storage and retrieval of project analysis context metadata.

Author: Amr Elhabbal | Powered by Meta AI Muse
"""

import json
from pathlib import Path
from typing import Any


class AnalysisStorage:

    DIRECTORY = ".neura"
    FILE_NAME = "analysis.json"

    @staticmethod
    def save(
        project_directory: str,
        analysis: dict[str, Any],
    ) -> str:

        root = Path(project_directory)

        neura_dir = root / AnalysisStorage.DIRECTORY

        neura_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = neura_dir / AnalysisStorage.FILE_NAME

        file_path.write_text(
            json.dumps(
                analysis,
                indent=4,
            ),
            encoding="utf-8",
        )

        return str(file_path)

    @staticmethod
    def load(
        project_directory: str,
    ) -> dict[str, Any]:

        file_path = (
            Path(project_directory)
            / AnalysisStorage.DIRECTORY
            / AnalysisStorage.FILE_NAME
        )

        if not file_path.exists():
            return {}

        try:
            return json.loads(file_path.read_text(encoding="utf-8"))

        except json.JSONDecodeError:
            return {}
