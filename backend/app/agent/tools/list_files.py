"""
AI tool for listing project files and inspecting structure through FileManager.

Author: Amr Elhabbal | Powered by Meta AI Muse
"""

from app.agent.tools.base import BaseTool
from app.file_system.file_manager import FileManager


class ListFilesTool(BaseTool):
    """
    Tool used by the agent to inspect project structure.

    Filesystem operations are delegated to FileManager.
    """

    def __init__(
        self,
        file_manager: FileManager,
    ):
        self.file_manager = file_manager

    @property
    def name(self) -> str:
        return "list_files"

    @property
    def description(self) -> str:
        return (
            "List files inside the project. "
            "Use this tool when inspecting "
            "the project structure."
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
                    "properties": {},
                    "additionalProperties": False,
                },
            },
        }

    def execute(
        self,
        project_directory: str,
        **kwargs,
    ) -> list[str]:
        """
        List project files through FileManager.
        """

        return self.file_manager.list_files(
            project_directory=project_directory,
        )
