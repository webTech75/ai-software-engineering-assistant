"""
AI tool for reading project files through FileManager.

Author: Amr Elhabbal | Powered by Meta AI Muse
"""

from app.agent.tools.base import BaseTool
from app.file_system.file_manager import FileManager


class ReadFileTool(BaseTool):
    """
    Tool used by the agent to read project files.

    Filesystem operations are handled by FileManager.
    """

    def __init__(
        self,
        file_manager: FileManager,
    ):
        self.file_manager = file_manager

    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return (
            "Read the contents of a file. "
            "Use this tool before answering questions "
            "about a file or before modifying it."
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
                            "description": ("Relative path of the file " "to read."),
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
    ):
        """
        Read file contents through FileManager.
        """

        return self.file_manager.read_file(
            project_directory=project_directory,
            requested_path=path,
        )
