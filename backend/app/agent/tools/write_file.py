"""
===============================================================================
File: write_file.py
Path: app/agent/tools/write_file.py

Description:
    Creates a new file or updates an existing file within the project.

Responsibilities:
    - Validate the destination path.
    - Prevent path traversal attacks.
    - Create parent directories when necessary.
    - Write content using UTF-8 encoding.

Notes:
    - Existing files are overwritten.
    - Parent directories are created automatically.
    - Only files inside the project directory can be modified.

Author:
    Amr Elhabbal
===============================================================================
"""
from pathlib import Path

from app.agent.tools.base import BaseTool
from app.models.project import Project


class WriteFileTool(BaseTool):
    @property
    def name(self) -> str:
        return "write_file"

    @property
    def description(self) -> str:
        return (
            "Creates a new file or replaces the contents of an existing file "
            "inside the user's project. Use this tool whenever the user requests "
            "to create, generate, write, update, edit, or modify a file."
        )

    @property
    def schema(self):
        return {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "Create or overwrite a file in the project.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Relative path of the file to write."
                        },
                        "content": {
                            "type": "string",
                            "description": "Complete file contents."
                        },
                        "overwrite": {
                            "type": "boolean",
                            "description": "Whether to overwrite an existing file.",
                            "default": False
                        }
                    },
                    "required": ["path", "content"],
                    "additionalProperties": False,
                },
            },
        }

    def execute(
        self,
        project: Project,
        path: str,
        content: str,
        overwrite: bool = False,
    ) -> str:

        root = Path(project.project_directory).resolve()
        file_path = (root / path).resolve()

        # Prevent path traversal
        if not str(file_path).startswith(str(root)):
            raise ValueError("Invalid file path.")

        if file_path.exists() and not overwrite:
            return {
                "status": "already_exists",
                "path": path,
            }

        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_path.write_text(
            content,
            encoding="utf-8",
        )

        return {
            "status": "created",
            "path": path,
        }