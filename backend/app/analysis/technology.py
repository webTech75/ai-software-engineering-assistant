from pathlib import Path

from app.analysis.base import BaseAnalyzer


class TechnologyAnalyzer(BaseAnalyzer):

    def analyze(self, project_directory: str) -> dict:

        root = Path(project_directory)

        technology = {
            "language": None,
            "framework": None,
            "database": None,
            "orm": None,
            "migration_tool": None,
        }

        python_files = list(root.rglob("*.py"))

        if python_files:
            technology["language"] = "Python"

        requirements = root / "requirements.txt"

        if requirements.exists():

            content = requirements.read_text(
                encoding="utf-8",
                errors="ignore",
            ).lower()

            if "fastapi" in content:
                technology["framework"] = "FastAPI"

            if "sqlalchemy" in content:
                technology["orm"] = "SQLAlchemy"

            if "alembic" in content:
                technology["migration_tool"] = "Alembic"

        if list(root.rglob("*.db")):
            technology["database"] = "SQLite"

        return {
            "technology": technology
        }