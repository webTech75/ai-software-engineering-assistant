"""
===============================================================================
File: file_indexer.py
Path: app/agent/intelligence/file_indexer.py

Description:
    Indexes project files and extracts metadata
    for AI code intelligence.

Responsibilities:
    - Traverse project directory.
    - Ignore unnecessary directories.
    - Ignore binary/generated files.
    - Detect programming languages.
    - Collect file metadata.

Notes:
    - Used by FileIndexService.
    - Does not store data directly.
    - Only returns file metadata.

Author:
    Amr Elhabbal
===============================================================================
"""

import os
from pathlib import Path


class FileIndexer:
    """
    Indexes project files and stores metadata
    for AI code intelligence.
    """

    IGNORE_FILES = {
        ".env",
        ".env.local",
        ".env.production",
        ".DS_Store",
        "Thumbs.db",
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "poetry.lock",
        "Pipfile.lock",
        "composer.lock",
    }

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
        "coverage",
        "logs",
        "uploads",
        "assistant.db",
    }

    IGNORE_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".svg",
        ".ico",
        ".pdf",
        ".zip",
        ".tar",
        ".gz",
        ".exe",
        ".dll",
        ".so",
        ".bin",
        ".pyc",
        ".class",
    }

    MAX_FILE_SIZE = 2_000_000  # 2 MB

    MAX_FILES = 5000


    def index(
        self,
        project_directory: str,
    ) -> list[dict]:
        """
        Scan project directory and return file metadata.
        """

        root = Path(project_directory).resolve()

        files = []

        if not root.exists():
            return files


        for current_dir, directories, filenames in os.walk(root):

            # Prevent entering ignored folders
            directories[:] = [
                directory
                for directory in directories
                if directory not in self.IGNORE_DIRS
            ]


            for filename in filenames:

                file = Path(current_dir) / filename

                if filename in self.IGNORE_FILES:
                    continue
                
                if file.suffix.lower() in self.IGNORE_EXTENSIONS:
                    continue


                try:
                    size = file.stat().st_size

                except OSError:
                    continue


                if size > self.MAX_FILE_SIZE:
                    continue


                files.append(
                    {
                        "path": str(
                            file.relative_to(root)
                        ),
                        "extension": file.suffix,
                        "language": self.detect_language(file),
                        "size": size,
                    }
                )


                if len(files) >= self.MAX_FILES:
                    return files


        return files



    def detect_language(
        self,
        file: Path,
    ) -> str:

        languages = {
            ".py": "Python",
            ".js": "JavaScript",
            ".jsx": "JavaScript React",
            ".ts": "TypeScript",
            ".tsx": "TypeScript React",
            ".java": "Java",
            ".cpp": "C++",
            ".c": "C",
            ".cs": "C#",
            ".go": "Go",
            ".rs": "Rust",
            ".php": "PHP",
            ".html": "HTML",
            ".css": "CSS",
            ".scss": "SCSS",
            ".sql": "SQL",
            ".json": "JSON",
            ".yaml": "YAML",
            ".yml": "YAML",
            ".md": "Markdown",
            ".xml": "XML",
            ".sh": "Shell",
        }

        return languages.get(
            file.suffix.lower(),
            "Unknown",
        )