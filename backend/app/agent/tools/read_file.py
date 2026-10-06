"""
===============================================================================
File: read_file.py
Path: app/agent/tools/read_file.py

Description:
    Reads the contents of a project file.

Responsibilities:
    - Validate the requested path.
    - Prevent path traversal attacks.
    - Read the file safely.
    - Return the file contents to the AI.

Notes:
    - Only files inside the project directory can be read.
    - Used before answering questions about a file or modifying it.

Author:
    Amr Elhabbal
===============================================================================
"""
from pathlib import Path

from app.agent.tools.base import BaseTool
from app.models.project import Project


class ReadFileTool(BaseTool):

    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return (
            "Read the contents of a file. Use this tool "
            "before answering questions about a file or before modifying it."
        )

    @property
    def schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Relative path of the file to read."
                        }
                    },
                    "required": ["path"],
                    "additionalProperties": False,
                },
            },
        }

    def execute(
        self,
        project: Project,
        path: str,
    ) -> str:

        root = Path(project.project_directory).resolve()

        file_path = (root / path).resolve()

       # Prevent path traversal
        if not str(file_path).startswith(str(root)):
            raise ValueError("Invalid file path.")

        if not file_path.exists():
            raise FileNotFoundError(path)

        if not file_path.is_file():
            raise ValueError(f"'{path}' is not a file.")

        return file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )
