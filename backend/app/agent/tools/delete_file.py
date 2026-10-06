"""
===============================================================================
File: delete_file.py
Path: app/agent/tools/delete_file.py

Description:
    Deletes a file from the current project.

Responsibilities:
    - Validate the requested path.
    - Prevent path traversal attacks.
    - Delete the file if it exists.
    - Return a clear status message.

Notes:
    - Only files inside the project directory can be deleted.
    - Directories are not supported by this tool.

Author:
    Amr Elhabbal
===============================================================================
"""
from pathlib import Path

from app.agent.tools.base import BaseTool
from app.models.project import Project


class DeleteFileTool(BaseTool):

    @property
    def name(self) -> str:
        return "delete_file"

    @property
    def description(self) -> str:
        return (
            "Delete an existing file from the project. "
            "Only use this tool when the user explicitly requests to delete a file."
        )

    @property
    def schema(self):
        return {
            "type": "function",
            "function": {
                "name": "delete_file",
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Relative path of the file to delete."
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
    ):
        root = Path(project.project_directory).resolve()
        file_path = (root / path).resolve()

        # Prevent path traversal
        if not str(file_path).startswith(str(root)):
            raise ValueError("Invalid file path.")

        if not file_path.exists():
            return {
                "status": "not_found",
                "path": path,
            }

        if not file_path.is_file():
            return {
                "status": "not_a_file",
                "path": path,
            }

        file_path.unlink()

        return {
            "status": "deleted",
            "path": path,
        }