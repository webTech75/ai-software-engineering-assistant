"""
===============================================================================
File: delete_file.py
Path: app/agent/tools/delete_file.py

Description:
    Deletes a file from the current project.

Responsibilities:
    - Expose delete_file capability to the AI agent.
    - Pass deletion requests to FileManager.
    - Return deletion results.

Does NOT:
    - Access filesystem directly.
    - Validate paths directly.
    - Manage project objects.
    - Execute AI reasoning.

Author:
    Amr Elhabbal
===============================================================================
"""

from app.agent.tools.base import BaseTool
from app.file_system.file_manager import FileManager


class DeleteFileTool(BaseTool):
    """
    Tool used by the agent to delete project files.

    All filesystem operations are handled by FileManager.
    """

    def __init__(
        self,
        file_manager: FileManager,
    ):
        self.file_manager = file_manager


    @property
    def name(self) -> str:
        return "delete_file"


    @property
    def description(self) -> str:
        return (
            "Delete an existing file from the project. "
            "Use only when the user explicitly requests "
            "file deletion."
        )


    @property
    def schema(self) -> dict:
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
                            "description": (
                                "Relative path of the file "
                                "to delete."
                            ),
                        },
                    },
                    "required": [
                        "path",
                    ],
                    "additionalProperties": False,
                },
            },
        }


    def execute(
        self,
        project_directory: str,
        path: str,
        **kwargs,
    ) -> dict:
        """
        Delete a file through FileManager.
        """

        return self.file_manager.delete_file(
            project_directory=project_directory,
            requested_path=path,
        )