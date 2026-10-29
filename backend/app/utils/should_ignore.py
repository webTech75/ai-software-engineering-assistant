"""
===============================================================================
File:
    app/utils/should_ignore.py

Description:
    Filters files and directories excluded from project analysis.

Author:
    Amr Elhabbal
===============================================================================
"""

from pathlib import Path

from app.analysis.constants import (
    IGNORED_DIRECTORIES,
    IGNORED_FILES,
    IGNORED_EXTENSIONS,
)


def should_ignore(path: Path) -> bool:
    """
    Determine whether a file or directory should be ignored
    during project analysis.
    """

    if any(part in IGNORED_DIRECTORIES for part in path.parts):
        return True

    if path.name in IGNORED_FILES:
        return True

    if path.is_file() and path.suffix.lower() in IGNORED_EXTENSIONS:
        return True

    return False
