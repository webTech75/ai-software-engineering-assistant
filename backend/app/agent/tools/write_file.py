"""
===============================================================================
File:
    app/agent/tools/write_file.py

Description:
    Creates or updates a project file.

Responsibilities:
    - Expose file writing capability to the AI agent.
    - Delegate filesystem operations to FileManager.
    - Return write results.

Does NOT:
    - Access filesystem directly.
    - Validate file security rules.
    - Manage project context.
    - Perform AI reasoning.

Author:
    Amr Elhabbal
===============================================================================
"""

from app.agent.tools.base import BaseTool
from app.file_system.file_manager import FileManager


class WriteFileTool(BaseTool):
    """
    Tool used by the agent to create or update files.

    All filesystem operations are handled by FileManager.
    """

    def __init__(
        self,
        file_manager: FileManager,
    ):
        self.file_manager = file_manager


    @property
    def name(self) -> str:
        return "write_file"


    @property
    def description(self) -> str:
        return (
            "Create a new file or replace the contents "
            "of an existing file inside the project."
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
                                "to write."
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
                                "Whether to overwrite "
                                "an existing file."
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
    ) -> dict:
        """
        Write file through FileManager.
        """

        return self.file_manager.write_file(
            project_directory=project_directory,
            requested_path=path,
            content=content,
            overwrite=overwrite,
        )