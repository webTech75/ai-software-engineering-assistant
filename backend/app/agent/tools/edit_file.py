from pathlib import Path

from app.agent.tools.base import BaseTool
from app.models.project import Project


class EditFileTool(BaseTool):

    @property
    def name(self):
        return "edit_file"

    @property
    def description(self):
        return (
            "Replace the complete contents of an existing file. "
            "Use this after reading a file and generating the updated version. "
            "Do not use this tool to create new files."
        )

    @property
    def schema(self):
        return {
            "type": "function",
            "function": {
                "name": "edit_file",
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Relative file path."
                        },
                        "content": {
                            "type": "string",
                            "description": "The complete updated file contents."
                        }
                    },
                    "required": [
                        "path",
                        "content"
                    ],
                    "additionalProperties": False
                }
            }
        }

    def execute(
        self,
        project: Project,
        path: str,
        content: str,
    ):
        root = Path(project.project_directory).resolve()
        file_path = (root / path).resolve()

        if not str(file_path).startswith(str(root)):
            raise ValueError("Invalid file path.")

        if not file_path.exists():
            return {
                "status": "not_found",
                "path": path,
            }

        file_path.write_text(
            content,
            encoding="utf-8",
        )

        return {
            "status": "edited",
            "path": path,
        }