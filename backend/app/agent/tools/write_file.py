"""
===============================================================================
File: write_file.py
Path: app/agent/tools/write_file.py

Description:
    Creates or updates a project file.

Responsibilities:
    - Receive file write requests.
    - Delegate filesystem operations to FileManager.
    - Return write result.

Notes:
    - File security rules are handled by FileManager.
    - Only files inside the project directory can be modified.

Author:
    Amr Elhabbal
===============================================================================
"""

from app.agent.tools.base import BaseTool
from app.file_system.file_manager import FileManager


class WriteFileTool(BaseTool):

    def __init__(
        self,
        file_manager: FileManager | None = None,
    ):
        self.file_manager = (
            file_manager
            or FileManager()
        )

    @property
    def name(self) -> str:
        return "write_file"

    @property
    def description(self) -> str:
        return (
            "Creates a new file or replaces the contents "
            "of an existing file inside the project."
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
                            "description": (
                                "Relative path of the file to write."
                            ),
                        },
                        "content": {
                            "type": "string",
                            "description": (
                                "Complete file contents."
                            ),
                        },
                        "overwrite": {
                            "type": "boolean",
                            "description": (
                                "Whether to overwrite an existing file."
                            ),
                            "default": False,
                        },
                    },
                    "required": [
                        "path",
                        "content",
                    ],
                    "additionalProperties": False,
                },
            },
        }

    def execute(
        self,
        project_directory: str,
        path: str,
        content: str,
        overwrite: bool = False,
        **kwargs,
    ):
        """
        Write file through FileManager.
        """

        return self.file_manager.write_file(
            project_directory,
            path,
            content,
            overwrite,
        )