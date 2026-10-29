"""
Project file access management.

Provides safe reading, listing, and searching
of uploaded project source files.

Author:
    Amr Elhabbal
===============================================================================
"""

from pathlib import Path

from app.file_system.file_policy import (
    is_allowed_file,
    is_file_size_allowed,
    should_ignore_path,
)


class FileManager:
    """
    Provides safe access to project source files.
    """

    MAX_READ_CHARACTERS = 50_000

    def get_source_root(
        self,
        project_directory: str,
    ) -> Path:
        """
        Return the project source directory.
        """

        root = Path(project_directory).resolve()

        if not root.exists():
            raise FileNotFoundError("Source directory not found.")

        return root

    def is_safe_path(
        self,
        root: Path,
        path: Path,
    ) -> bool:
        """
        Prevent path traversal outside source directory.
        """

        try:

            path.relative_to(root)

            return True

        except ValueError:

            return False

    def resolve_file(
        self,
        project_directory: str,
        requested_path: str,
    ) -> Path:
        """
        Resolve requested file inside source directory.

        Example:
            app/main.py
        """

        root = self.get_source_root(project_directory)

        file_path = (root / requested_path).resolve()

        if not file_path.exists():

            raise FileNotFoundError(requested_path)

        if not file_path.is_file():

            raise ValueError("Path is not a file.")

        if not self.is_safe_path(
            root,
            file_path,
        ):

            raise ValueError("Unsafe file path.")

        return file_path

    def read_file(
        self,
        project_directory: str,
        requested_path: str,
    ) -> str:
        """
        Read source file contents.
        """

        file_path = self.resolve_file(
            project_directory,
            requested_path,
        )

        if not is_allowed_file(file_path):

            raise ValueError("Unsupported file type.")

        if not is_file_size_allowed(file_path):

            raise ValueError("File exceeds size limit.")

        content = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        if len(content) > self.MAX_READ_CHARACTERS:

            remaining = len(content) - self.MAX_READ_CHARACTERS

            return (
                "File truncated. "
                f"{remaining} more characters hidden.\n\n"
                f"{content[:self.MAX_READ_CHARACTERS]}"
            )

        return content

    def list_files(
        self,
        project_directory: str,
    ) -> list[str]:
        """
        Return source file tree.
        """

        root = self.get_source_root(project_directory)

        files = []

        for file in root.rglob("*"):

            if should_ignore_path(file):

                continue

            if not file.is_file():

                continue

            if not is_allowed_file(file):

                continue

            files.append(str(file.relative_to(root)))

        return sorted(files)

    def search_text(
        self,
        project_directory: str,
        query: str,
    ) -> list[dict]:
        """
        Search text inside project files.
        """

        root = self.get_source_root(project_directory)

        results = []

        for relative_path in self.list_files(project_directory):

            file_path = root / relative_path

            try:

                with file_path.open(
                    encoding="utf-8",
                    errors="ignore",
                ) as file:

                    for line_number, line in enumerate(
                        file,
                        start=1,
                    ):

                        if query.lower() in line.lower():

                            results.append(
                                {
                                    "file": relative_path,
                                    "line": line_number,
                                    "text": line.strip(),
                                }
                            )

            except Exception:

                continue

        return results
