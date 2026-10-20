"""
===============================================================================
File:
    app/file_system/file_manager.py

Description:
    Central service for accessing uploaded project files.

Responsibilities:
    - Resolve project file paths.
    - Validate safe file access.
    - Read files.
    - Write files.
    - Edit files.
    - Delete files.
    - Search project contents.

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

    All tools should use FileManager instead
    of accessing the filesystem directly.
    """

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


    def get_root(
        self,
        project_directory: str,
    ) -> Path:
        """
        Return validated project root.
        """

        root = Path(
            project_directory
        ).resolve()


        if not root.exists():

            raise FileNotFoundError(
                "Project directory does not exist."
            )


        return root



    def is_safe_path(
        self,
        root: Path,
        path: Path,
    ) -> bool:
        """
        Prevent path traversal attacks.
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
    ) -> Path | list[Path]:
        """
        Resolve requested file.

        Supports:

            app/main.py

        or:

            main.py

        """

        root = self.get_root(
            project_directory
        )


        requested = Path(
            requested_path
        )


        direct_path = (
            root / requested
        ).resolve()


        if (
            direct_path.exists()
            and direct_path.is_file()
        ):

            if not self.is_safe_path(
                root,
                direct_path,
            ):

                raise ValueError(
                    "Invalid file path."
                )

            return direct_path



        matches = []


        for file in root.rglob("*"):

            if any(
                part in self.IGNORE_DIRS
                for part in file.parts
            ):

                continue


            if not file.is_file():

                continue


            if (
                file.name.lower()
                == requested_path.lower()
            ):

                resolved = file.resolve()


                if self.is_safe_path(
                    root,
                    resolved,
                ):

                    matches.append(
                        resolved
                    )



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

        file_path = self.resolve_file(
            project_directory,
            requested_path,
        )


        if isinstance(
            file_path,
            list,
        ):

            return {
                "status": "multiple_files",
                "message":
                    "Multiple files found.",
                "files": [
                    str(path)
                    for path in file_path
                ],
            }



        if not is_allowed_file(
            file_path
        ):

            raise ValueError(
                "File type is not supported."
            )


        if not is_file_size_allowed(
            file_path
        ):

            raise ValueError(
                "File too large."
            )


        content = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )


        max_length = 50000


        if len(content) > max_length:

            return (
                "File too large.\n\n"
                f"Showing first {max_length} characters.\n\n"
                f"{content[:max_length]}"
            )


        return content



    def list_files(
        self,
        project_directory: str,
    ) -> list[str]:
        """
        Return project files.
        """

        root = self.get_root(
            project_directory
        )


        files = []


        for file in root.rglob("*"):

            if any(
                part in self.IGNORE_DIRS
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


        return sorted(files[:1000])



    def write_file(
        self,
        project_directory: str,
        requested_path: str,
        content: str,
        overwrite: bool = False,
    ) -> dict:

        root = self.get_root(
            project_directory
        )


        file_path = (
            root / requested_path
        ).resolve()


        if not self.is_safe_path(
            root,
            file_path,
        ):

            raise ValueError(
                "Invalid file path."
            )



        if (
            file_path.exists()
            and not overwrite
        ):

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


        content = self.read_file(
            project_directory,
            requested_path,
        )


        if isinstance(content, dict):

            return content



        if old_text not in content:

            return {
                "status": "text_not_found",
                "path": requested_path,
            }



        updated = content.replace(
            old_text,
            new_text,
        )


        self.write_file(
            project_directory,
            requested_path,
            updated,
            overwrite=True,
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

            file_path = self.resolve_file(
                project_directory,
                requested_path,
            )

        except FileNotFoundError:

            return {
                "status": "not_found",
                "path": requested_path,
            }



        if isinstance(
            file_path,
            list,
        ):

            return {
                "status": "multiple_files",
                "files": [
                    str(path)
                    for path in file_path
                ],
            }



        file_path.unlink()


        return {
            "status": "deleted",
            "path": requested_path,
        }



    def search_text(
        self,
        project_directory: str,
        query: str,
    ) -> list[dict]:

        root = self.get_root(
            project_directory
        )


        results = []


        for relative in self.list_files(
            project_directory
        ):

            file_path = root / relative


            try:

                with file_path.open(
                    "r",
                    encoding="utf-8",
                    errors="ignore",
                ) as file:


                    for number, line in enumerate(
                        file,
                        start=1,
                    ):

                        if query.lower() in line.lower():

                            results.append(
                                {
                                    "file": relative,
                                    "line": number,
                                    "text": line.rstrip(),
                                }
                            )


            except Exception:

                continue


        return results



    def find_files(
        self,
        project_directory: str,
        query: str,
    ) -> list[dict]:

        results = []


        for file in self.list_files(
            project_directory
        ):

            path = Path(file)


            if query.lower() in path.name.lower():

                results.append(
                    {
                        "path": file
                    }
                )


        return results