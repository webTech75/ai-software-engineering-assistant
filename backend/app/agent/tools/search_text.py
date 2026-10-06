from pathlib import Path

from app.agent.tools.base import BaseTool
from app.models.project import Project


class SearchTextTool(BaseTool):

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
        project: Project,
        query: str,
    ) -> list[dict]:

        root = Path(project.project_directory).resolve()

        results = []

        for file in root.rglob("*"):

            if not file.is_file():
                continue

            try:
                lines = file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                ).splitlines()

                for number, line in enumerate(lines, start=1):

                    if query.lower() in line.lower():

                        results.append(
                            {
                                "file": str(file.relative_to(root)),
                                "line": number,
                                "text": line.strip(),
                            }
                        )

            except Exception:
                # Skip binary or unreadable files
                continue

        return results