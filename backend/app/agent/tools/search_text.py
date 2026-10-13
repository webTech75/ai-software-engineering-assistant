from pathlib import Path

from app.agent.tools.base import BaseTool
from app.file_system.file_manager import FileManager


class SearchTextTool(BaseTool):

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
            "Search for text, functions, classes, variables, or other code within the project. "
            "Use this tool when you need to locate information."
        )

    @property
    def schema(self):
        return {
            "type": "function",
            "function": {
                "name": "search_text",
                "description": "Search the project for text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Text to search for."
                        }
                    },
                    "required": ["query"],
                    "additionalProperties": False,
                },
            },
        }

    def execute(
        self,
        project_directory: str,
        query: str,
        **kwargs
    ) -> list[dict]:

        return self.file_manager.search_text(
            project_directory=project_directory,
            query=query,
        )