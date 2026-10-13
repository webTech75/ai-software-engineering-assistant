"""
===============================================================================
File: read_file.py
Path: app/agent/tools/read_file.py

Description:
    Reads the contents of a project file.

Responsibilities:
    - Receive a requested file path.
    - Delegate file access to FileManager.
    - Return file contents to the AI.

Notes:
    - File security rules are handled by FileManager.
    - Only files inside the project directory can be read.

Author:
    Amr Elhabbal
===============================================================================
"""


from app.agent.tools.base import BaseTool
from app.file_system.file_manager import FileManager



class ReadFileTool(BaseTool):


    def __init__(
        self,
        file_manager: FileManager | None = None,
    ):
        """
        Initialize tool with filesystem manager.
        """

        self.file_manager = (
            file_manager
            or FileManager()
        )



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
                            "description": (
                                "Relative path of the file to read."
                            )
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
    ) -> str:
        """
        Read file contents through FileManager.
        """

        return self.file_manager.read_file(
            project_directory,
            path,
        )