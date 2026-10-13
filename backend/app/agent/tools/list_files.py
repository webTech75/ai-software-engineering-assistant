"""
===============================================================================
File: list_files.py
Path: app/agent/tools/list_files.py

Description:
    Lists project files.

Responsibilities:
    - Request file listing from FileManager.
    - Return discovered project files.

Notes:
    - Filesystem rules are handled by FileManager.
    - Absolute paths are never exposed.

Author:
    Amr Elhabbal
===============================================================================
"""


from app.agent.tools.base import BaseTool
from app.file_system.file_manager import FileManager



class ListFilesTool(BaseTool):


    def __init__(
        self,
        file_manager: FileManager | None = None,
    ):
        """
        Initialize filesystem manager.
        """

        self.file_manager = (
            file_manager
            or FileManager()
        )



    @property
    def name(self):
        return "list_files"



    @property
    def description(self):
        return (
            "List all files in the project. "
            "Use this tool whenever you need "
            "to inspect the project structure."
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
                    "properties": {},
                    "additionalProperties": False,
                },
            },
        }



    def execute(
        self,
        project_directory: str,
        **kwargs
    ) -> list[str]:
        """
        Return project files through FileManager.
        """

        return self.file_manager.list_files(
            project_directory
        )