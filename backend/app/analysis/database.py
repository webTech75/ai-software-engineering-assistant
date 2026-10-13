from pathlib import Path

from app.analysis.base import BaseAnalyzer
from app.analysis.constants import IGNORED_DIRECTORIES


class DatabaseAnalyzer(BaseAnalyzer):

    name = "DatabaseAnalyzer"


    def analyze(self, project_directory):

        root = Path(project_directory)

        result = {
            "engine": None,
            "database_files": [],
            "migration_tool": None,
            "migrations": []
        }


        for file in root.rglob("*"):

            if self.should_ignore(file):
                continue


            if file.is_file():

                self.detect_database_files(
                    file,
                    result
                )

                self.detect_migrations(
                    file,
                    result
                )


        result["engine"] = self.detect_engine(
            result
        )


        return {
            "database": result
        }



    def detect_database_files(self, file, result):

        suffix = file.suffix.lower()


        if suffix in [
            ".db",
            ".sqlite",
            ".sqlite3"
        ]:

            result["database_files"].append(
                {
                    "file": str(file),
                    "type": "SQLite"
                }
            )



    def detect_migrations(self, file, result):

        path_parts = file.parts


        if "alembic" in path_parts:

            result["migration_tool"] = "Alembic"


            if (
                "versions" in path_parts
                and file.suffix == ".py"
            ):

                result["migrations"].append(
                    {
                        "file": str(file)
                    }
                )



    def detect_engine(self, result):

        if result["database_files"]:

            return result["database_files"][0]["type"]


        return None



    def should_ignore(self, path):

        return any(
            part in IGNORED_DIRECTORIES
            for part in path.parts
        )