"""
===============================================================================
File: file_policy.py
Path: app/file_system/file_policy.py

Description:
    Defines rules for accessing project files.

Responsibilities:
    - Control which files can be analyzed.
    - Ignore unnecessary directories.
    - Prevent processing unsafe files.
    - Enforce file size limits.

Does NOT:
    - Read files.
    - Search files.
    - Access the database.

Author:
    Amr Elhabbal
===============================================================================
"""


from pathlib import Path


# Directories that should not be analyzed
IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "dist",
    "build",
}


# File types that should never be processed
IGNORED_EXTENSIONS = {
    ".pyc",
    ".exe",
    ".dll",
    ".so",
    ".db",
    ".sqlite",
}


# File extensions we support for code analysis
ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".java",
    ".go",
    ".rs",
    ".cpp",
    ".c",
    ".h",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".txt",
}


# Maximum file size allowed for reading
MAX_FILE_SIZE = 500_000  # 500 KB



def is_ignored_directory(directory: Path) -> bool:
    """
    Check whether a directory should be skipped.
    """

    return directory.name in IGNORED_DIRECTORIES



def is_allowed_file(file_path: Path) -> bool:
    """
    Check whether a file type can be processed.
    """

    extension = file_path.suffix.lower()

    if extension in IGNORED_EXTENSIONS:
        return False

    if extension not in ALLOWED_EXTENSIONS:
        return False

    return True



def is_file_size_allowed(file_path: Path) -> bool:
    """
    Check whether the file size is within the limit.
    """

    return file_path.stat().st_size <= MAX_FILE_SIZE