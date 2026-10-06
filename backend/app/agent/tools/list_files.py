"""
===============================================================================
File: list_files.py
Path: app/agent/tools/list_files.py

Description:
    Lists every file in the current project.

Responsibilities:
    - Traverse the project directory.
    - Return relative file paths.
    - Exclude directories.
    - Sort results for deterministic output.

Notes:
    - Returns paths relative to the project root.
    - Absolute filesystem paths are never exposed.
    - Used by the AI to discover project files.

Author:
    Amr Elhabbal
===============================================================================
"""

from pathlib import Path

from app.agent.tools.base import BaseTool
from app.models.project import Project


class ListFilesTool(BaseTool):

    @property
    def name(self):
        return "list_files"

    @property
    def description(self):
        return (
            "List all files and folders in the project. Use this tool "
            "whenever you need to inspect the project structure."
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

    def execute(self, project: Project) -> list[str]:

        root = Path(project.project_directory).resolve()

        if not root.exists():
            return []

        IGNORE_DIRS = {
            ".git",
            ".venv",
            "venv",
            "env",
            "__pycache__",
            "node_modules",
            ".pytest_cache",
            ".mypy_cache",
            ".idea",
            ".vscode",
            "dist",
            "build",
            ".next",
            ".cache",
        }

        MAX_FILES = 1000

        files = []

        for file in root.rglob("*"):

            if any(part in IGNORE_DIRS for part in file.parts):
                continue

            if not file.is_file():
                continue

            files.append(str(file.relative_to(root)))

            if len(files) >= MAX_FILES:
                break

        print(f"ListFilesTool returned {len(files)} files.")
        
        return sorted(files)