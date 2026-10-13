"""
===============================================================================
File: file_manager.py
Path: app/file_system/file_manager.py

Description:
    Central service for accessing uploaded project files. 
    FileManager focused on file operations

Responsibilities:
    - Resolve project file paths.
    - Validate safe file access.
    - Read file contents.

Does NOT:
    - Know about database models.
    - Execute AI analysis.
    - Manage uploads.

Author:
    Amr Elhabbal
===============================================================================
"""


from pathlib import Path

from app.file_system.file_policy import (
    is_allowed_file,
    is_file_size_allowed,
)



class FileManager:
    """
    Handles filesystem operations for uploaded projects.
    """



    def resolve_file(
        self,
        project_directory: str,
        requested_path: str,
    ) -> Path | list[Path]:
        """
        Resolve a requested file inside a project directory.

        Returns:
            Path:
                When exactly one file is found.

            list[Path]:
                When multiple files have the same name.

        """

        root = Path(project_directory).resolve()

        if not root.exists():
            raise FileNotFoundError(
                "Project directory does not exist."
            )

        requested = Path(requested_path)

        # Try exact path first
        direct_path = (
            root / requested
        ).resolve()

        if direct_path.exists() and direct_path.is_file():

            if not str(direct_path).startswith(
                str(root)
            ):
                raise ValueError(
                    "Invalid file path."
                )

            return direct_path


        # Search project files
        matches = []

        ignore_dirs = {
            ".git",
            ".venv",
            "venv",
            "env",
            "__pycache__",
            "node_modules",
        }


        for file in root.rglob(requested_path):

            if any(
                part in ignore_dirs
                for part in file.parts
            ):
                continue

            if file.is_file():

                resolved = file.resolve()

                if not str(resolved).startswith(
                    str(root)
                ):
                    continue

                matches.append(resolved)


        if not matches:
            raise FileNotFoundError(
                requested_path
            )

        if len(matches) > 1:
            return sorted(matches)


        return matches[0]
    

    def read_file(
        self,
        project_directory: str,
        requested_path: str,
    ):
        """
        Read a file from a project.

        Returns:
            File content if one file is found.
            File list if multiple matches exist.
        """

        result = self.resolve_file(
            project_directory,
            requested_path,
        )


        if isinstance(result, list):
            return {
                "status": "multiple_files",
                "message": "Multiple files found. Please select one.",
                "files": [
                    str(
                        file.relative_to(
                            Path(project_directory).resolve()
                        )
                    )
                    for file in result
                ],
            }


        if not is_allowed_file(result):
            raise ValueError(
                "File type is not supported."
            )


        if not is_file_size_allowed(result):
            raise ValueError(
                "File is too large to read."
            )


        return result.read_text(
            encoding="utf-8",
            errors="ignore",
        )


    def list_files(
        self,
        project_directory: str,
    ) -> list[str]:
        """
        List all files inside a project directory.

        Returns:
            Relative file paths only.

        Example:
            [
                "app/main.py",
                "app/models/user.py"
            ]
        """

        root = Path(project_directory).resolve()


        if not root.exists():
            return []


        ignore_dirs = {
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


        max_files = 1000


        files = []


        for file in root.rglob("*"):

            if any(
                part in ignore_dirs
                for part in file.parts
            ):
                continue


            if not file.is_file():
                continue


            files.append(
                str(
                    file.relative_to(root)
                )
            )


            if len(files) >= max_files:
                break


        return sorted(files)

    def write_file(
        self,
        project_directory: str,
        requested_path: str,
        content: str,
        overwrite: bool = False,
    ) -> dict:
        """
        Create or update a project file.

        Returns:
            Status information.
        """

        root = Path(project_directory).resolve()

        if not root.exists():
            raise FileNotFoundError(
                "Project directory does not exist."
            )

        file_path = (
            root / requested_path
        ).resolve()

        # Security check
        if not str(file_path).startswith(
            str(root)
        ):
            raise ValueError(
                "Invalid file path."
            )

        if file_path.exists() and not overwrite:
            return {
                "status": "already_exists",
                "path": requested_path,
            }

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path.write_text(
            content,
            encoding="utf-8",
        )

        return {
            "status": "created",
            "path": requested_path,
        }
    

    def edit_file(
        self,
        project_directory: str,
        requested_path: str,
        old_text: str,
        new_text: str,
    ) -> dict:
        """
        Replace text inside an existing project file.

        Returns:
            Status information.
        """

        file_path = self.resolve_file(
            project_directory,
            requested_path,
        )

        # Multiple files found
        if isinstance(file_path, list):
            return {
                "status": "multiple_files",
                "message": "Multiple files found. Please select one.",
                "files": [
                    str(path)
                    for path in file_path
                ],
            }

        if not is_allowed_file(file_path):
            raise ValueError(
                "File type is not supported."
            )

        if not is_file_size_allowed(file_path):
            raise ValueError(
                "File is too large to edit."
            )

        content = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        if old_text not in content:
            return {
                "status": "text_not_found",
                "path": requested_path,
            }

        updated_content = content.replace(
            old_text,
            new_text,
        )

        file_path.write_text(
            updated_content,
            encoding="utf-8",
        )

        return {
            "status": "updated",
            "path": requested_path,
        }
    

    def delete_file(
        self,
        project_directory: str,
        requested_path: str,
    ) -> dict:

        try:
            result = self.resolve_file(
                project_directory,
                requested_path,
            )

        except FileNotFoundError:
            return {
                "status": "not_found",
                "path": requested_path,
            }

        if isinstance(result, list):
            return {
                "status": "multiple_files",
                "message": "Multiple files found. Please select one.",
                "files": [
                    str(
                        file.relative_to(
                            Path(project_directory).resolve()
                        )
                    )
                    for file in result
                ],
            }

        result.unlink()

        return {
            "status": "deleted",
            "path": requested_path,
        }
    

    def search_text(
        self,
        project_directory: str,
        query: str,
    ) -> list[dict]:
        """
        Search for text in all project files.

        Returns:
            A list of matches containing the file path,
            line number, and matching line.
        """

        root = Path(project_directory).resolve()

        if not root.exists():
            return []

        results = []

        for relative_path in self.list_files(project_directory):

            try:
                file_path = root / relative_path

                if not is_allowed_file(file_path):
                    continue

                if not is_file_size_allowed(file_path):
                    continue

                with file_path.open(
                    "r",
                    encoding="utf-8",
                    errors="ignore",
                ) as file:

                    for line_number, line in enumerate(file, start=1):

                        if query.lower() in line.lower():

                            results.append(
                                {
                                    "file": relative_path,
                                    "line": line_number,
                                    "text": line.rstrip(),
                                }
                            )

            except Exception:
                continue

        return results