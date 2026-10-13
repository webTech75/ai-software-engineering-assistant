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
from app.file_system.file_manager import FileManager

class DeleteFileTool(BaseTool):

    def __init__(
        self,
        file_manager: FileManager
    ):
        self.file_manager = file_manager

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
        project_directory: str,
        path: str,
        **kwargs
    ):

        return self.file_manager.delete_file(
            project_directory=project_directory,
            requested_path=path,
        )