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
            "Search project files. "
            "Use 'file' to find filenames or paths. "
            "Use 'content' to search inside files."
        )


    @property
    def schema(self):
        return {
            "type": "function",
            "function": {
                "name": "search_text",
                "description": (
                    "Search project files by filename or content."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": (
                                "Filename, path, or text to search for."
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
    ):

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
            "Invalid search_type. Use 'file' or 'content'."
        )