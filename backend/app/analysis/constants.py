"""
Defines files, directories, and extensions excluded from project analysis.

Author: Amr Elhabbal | Powered by Meta AI Muse
"""

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".next",
    "coverage",
}

IGNORED_FILES = {".env", "assistant.db", ".DS_Store", "LICENSE"}


IGNORED_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".zip",
    ".so",
}
