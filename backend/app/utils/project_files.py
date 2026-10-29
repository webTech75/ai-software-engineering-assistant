"""
===============================================================================
File:
    app/utils/project_files.py

Description:
    Safely resolves project file paths.

Responsibilities:
    - Locate requested files.
    - Support direct and recursive lookup.
    - Prevent unsafe file access.

Author:
    Amr Elhabbal
===============================================================================
"""

from pathlib import Path

IGNORE_DIRECTORIES = {
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".git",
}


def resolve_project_file(
    project_directory: str,
    requested_path: str,
) -> Path:
    """
    Resolve a requested file path inside a project directory.

    Supports:

        app/main.py

    or:

        README.md

    """

    root = Path(project_directory).resolve()

    if not root.exists():
        raise FileNotFoundError("Project directory does not exist.")

    requested = Path(requested_path)

    # -----------------------------------------
    # 1. Try exact path first
    # -----------------------------------------

    direct_path = (root / requested).resolve()

    if direct_path.exists():
        file_path = direct_path

    else:

        # -------------------------------------
        # 2. Search recursively
        # ignoring dependencies
        # -------------------------------------

        matches = []

        for path in root.rglob(requested.name):

            if any(ignored in path.parts for ignored in IGNORE_DIRECTORIES):
                continue

            if path.is_file():
                matches.append(path)

        if not matches:
            raise FileNotFoundError(requested_path)

        if len(matches) > 1:
            raise ValueError(
                "Multiple files found:\n"
                + "\n".join(str(m.relative_to(root)) for m in matches)
            )

        file_path = matches[0].resolve()

    # -----------------------------------------
    # Security check
    # -----------------------------------------

    if not str(file_path).startswith(str(root)):
        raise ValueError("Invalid file path.")

    if not file_path.is_file():
        raise ValueError(f"{requested_path} is not a file.")

    return file_path
