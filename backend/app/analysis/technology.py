from pathlib import Path

from app.analysis.base import BaseAnalyzer
from app.analysis.constants import IGNORED_DIRECTORIES


class TechnologyAnalyzer(BaseAnalyzer):
    """
    Analyze project technologies.
    """

    def analyze(self, project_directory: str) -> dict:

        root = Path(project_directory)

        technology = {
            "language": None,
            "framework": None,
            "database": None,
            "orm": None,
            "migration_tool": None,
        }

        # Detect Python
        python_files = []

        for path in root.rglob("*.py"):

            if any(
                part in IGNORED_DIRECTORIES
                for part in path.parts
            ):
                continue

            python_files.append(path)

        if python_files:
            technology["language"] = "Python"

        # Find requirements.txt anywhere in project
        requirements_files = []

        for path in root.rglob("requirements.txt"):

            if any(
                part in IGNORED_DIRECTORIES
                for part in path.parts
            ):
                continue

            requirements_files.append(path)

        if requirements_files:

            requirements = requirements_files[0]

            try:
                content = requirements.read_text(
                    encoding="utf-8",
                    errors="ignore",
                ).lower()

            except Exception:
                content = ""

            if "fastapi" in content:
                technology["framework"] = "FastAPI"

            if "sqlalchemy" in content:
                technology["orm"] = "SQLAlchemy"

            if "alembic" in content:
                technology["migration_tool"] = "Alembic"

        # Detect database files
        database_files = []

        for path in root.rglob("*.db"):

            if any(
                part in IGNORED_DIRECTORIES
                for part in path.parts
            ):
                continue

            database_files.append(path)

        if database_files:
            technology["database"] = "SQLite"

        return {
            "technology": technology
        }