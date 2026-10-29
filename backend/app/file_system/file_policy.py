"""
Project file access policies.

Defines rules for allowed files, ignored paths,
and safety limits for project processing.

Author:
    Amr Elhabbal
===============================================================================
"""

from pathlib import Path

# ============================================================
# Directories ignored during analysis
# ============================================================

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".idea",
    ".vscode",
    "dist",
    "build",
    ".next",
    ".cache",
    ".neura",
}


# ============================================================
# Files that should never be processed
# ============================================================

IGNORED_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".db",
    ".sqlite",
    ".sqlite3",
}

IGNORED_FILES = {
    ".env",
    ".env.example",
}

# ============================================================
# Files supported for analysis
# ============================================================

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


# ============================================================
# File read limits
# ============================================================

# Maximum individual file size Neura can read
MAX_FILE_SIZE = 500_000  # 500 KB


# ============================================================
# Upload limits
# ============================================================

# Maximum uploaded ZIP file size
MAX_UPLOAD_SIZE = 1 * 1024 * 1024 * 1024  # 1 GB

# Maximum extracted project size
MAX_EXTRACTED_SIZE = 1 * 1024 * 1024 * 1024  # 1 GB

# Maximum number of files allowed inside ZIP
MAX_FILES_IN_ZIP = 5000


# ============================================================
# Rules
# ============================================================


def is_ignored_directory(
    directory: Path,
) -> bool:
    """
    Check whether directory should be skipped.
    """

    return directory.name in IGNORED_DIRECTORIES


def is_allowed_file(
    file_path: Path,
) -> bool:
    """
    Check whether file can be analyzed.
    """

    extension = file_path.suffix.lower()

    if extension in IGNORED_EXTENSIONS:
        return False

    return extension in ALLOWED_EXTENSIONS


def is_file_size_allowed(
    file_path: Path,
) -> bool:
    """
    Check individual file size.
    """

    return file_path.stat().st_size <= MAX_FILE_SIZE


def is_zip_size_allowed(
    file_size: int,
) -> bool:
    """
    Check uploaded ZIP size.
    """

    return file_size <= MAX_UPLOAD_SIZE


def should_ignore_path(path: Path) -> bool:
    """
    Determine whether a path should be ignored.
    """

    for part in path.parts:

        if part in IGNORED_DIRECTORIES:
            return True

    if path.name in IGNORED_FILES:
        return True

    return False
