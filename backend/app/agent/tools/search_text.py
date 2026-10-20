"""
===============================================================================
File:
    app/agent/tools/search_text.py

Description:
    Searches project files.

Responsibilities:
    - Expose project search capability to the AI agent.
    - Search filenames through FileManager.
    - Search file contents through FileManager.
    - Return matching results.

Does NOT:
    - Access filesystem directly.
    - Manage project context.
    - Perform AI reasoning.
    - Validate filesystem security.

Author:
    Amr Elhabbal
===============================================================================
"""

from app.agent.tools.base import BaseTool
from app.file_system.file_manager import FileManager


class SearchTextTool(BaseTool):
    """
    Tool used by the agent to locate files
    or search inside project contents.

    Filesystem operations are delegated to FileManager.
    """

    def __init__(
        self,
        file_manager: FileManager,
    ):
        self.file_manager = file_manager


    @property
    def name(self) -> str:
        return "search_text"


    @property
    def description(self) -> str:
        return (
            "Search project files. "
            "Use 'file' to find filenames or paths. "
            "Use 'content' to search inside files."
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
                        "query": {
                            "type": "string",
                            "description": (
                                "Filename, path, or text "
                                "to search for."
                            ),
                        },
                        "search_type": {
                            "type": "string",
                            "enum": [
                                "file",
                                "content",
                            ],
                            "description": (
                                "file = locate files. "
                                "content = search inside files."
                            ),
                        },
                    },
                    "required": [
                        "query",
                        "search_type",
                    ],
                    "additionalProperties": False,
                },
            },
        }


    def execute(
        self,
        project_directory: str,
        query: str,
        search_type: str = "file",
        **kwargs,
    ) -> list[dict]:
        """
        Search project files through FileManager.
        """

        if search_type == "file":

            return self.file_manager.find_files(
                project_directory=project_directory,
                query=query,
            )


        if search_type == "content":

            return self.file_manager.search_text(
                project_directory=project_directory,
                query=query,
            )


        raise ValueError(
            "Invalid search_type. "
            "Use 'file' or 'content'."
        )