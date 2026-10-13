from app.agent.tools.base import BaseTool
from app.file_system.file_manager import FileManager


class EditFileTool(BaseTool):

    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager


    @property
    def name(self):
        return "edit_file"


    @property
    def description(self):
        return (
            "Replace text inside an existing file. "
            "Use this tool when modifying an existing project file. "
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

                        "old_text": {
                            "type": "string",
                            "description": "Existing text to replace."
                        },

                        "new_text": {
                            "type": "string",
                            "description": "Replacement text."
                        }

                    },
                    "required": [
                        "path",
                        "old_text",
                        "new_text"
                    ],
                    "additionalProperties": False
                }
            }
        }


    def execute(
        self,
        project_directory: str,
        path: str,
        old_text: str,
        new_text: str,
        **kwargs
    ):

        return self.file_manager.edit_file(
            project_directory=project_directory,
            requested_path=path,
            old_text=old_text,
            new_text=new_text,
        )