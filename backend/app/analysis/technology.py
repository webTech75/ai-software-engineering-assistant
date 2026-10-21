import json
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
            "languages": [],
            "frameworks": [],
            "database": None,
            "orms": [],
            "migration_tools": [],
            "package_manager": None,
            "build_tools": [],
            "testing_tools": [],
            "styling_tools": [],
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
            technology["languages"].append(
                "Python"
            )


        # Detect requirements.txt

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
                technology["frameworks"].append(
                    "FastAPI"
                )

            if "sqlalchemy" in content:
                technology["orms"].append(
                    "SQLAlchemy"
                )

            if "alembic" in content:
                technology["migration_tools"].append(
                    "Alembic"
                )

                        # Detect Python databases

            if "psycopg" in content or "psycopg2" in content:
                technology["database"] = "PostgreSQL"

            elif "asyncpg" in content:
                technology["database"] = "PostgreSQL"

            elif "pymysql" in content or "mysqlclient" in content:
                technology["database"] = "MySQL"

            elif "pymongo" in content:
                technology["database"] = "MongoDB"
            technology["package_manager"] = "pip"



        # Detect SQLite database files

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



        # Detect Prisma database

        prisma_files = []

        for path in root.rglob("schema.prisma"):

            if any(
                part in IGNORED_DIRECTORIES
                for part in path.parts
            ):
                continue

            prisma_files.append(path)


        if prisma_files:

            try:
                content = prisma_files[0].read_text(
                    encoding="utf-8",
                    errors="ignore",
                ).lower()

            except Exception:
                content = ""


            if "postgresql" in content:
                technology["database"] = "PostgreSQL"

            elif "mysql" in content:
                technology["database"] = "MySQL"

            elif "sqlite" in content:
                technology["database"] = "SQLite"

            elif "mongodb" in content:
                technology["database"] = "MongoDB"



        # Detect JavaScript / TypeScript ecosystem

        package_files = []

        for path in root.rglob("package.json"):

            if any(
                part in IGNORED_DIRECTORIES
                for part in path.parts
            ):
                continue

            package_files.append(path)


        if package_files:

            package_json = package_files[0]

            try:
                data = json.loads(
                    package_json.read_text(
                        encoding="utf-8",
                        errors="ignore",
                    )
                )

            except Exception:
                data = {}


            dependencies = {
                **data.get("dependencies", {}),
                **data.get("devDependencies", {}),
            }


            # Package manager

            if (root / "package-lock.json").exists():
                technology["package_manager"] = "npm"

            elif (root / "yarn.lock").exists():
                technology["package_manager"] = "yarn"

            elif (root / "pnpm-lock.yaml").exists():
                technology["package_manager"] = "pnpm"

            elif (root / "bun.lockb").exists():
                technology["package_manager"] = "bun"

            else:
                technology["package_manager"] = "npm"



            # Languages

            if "typescript" in dependencies:
                technology["languages"].append(
                    "TypeScript"
                )



            # Frontend frameworks

            if "react" in dependencies:
                technology["frameworks"].append(
                    "React"
                )

            if "next" in dependencies:
                technology["frameworks"].append(
                    "Next.js"
                )


            # Backend frameworks

            if "express" in dependencies:
                technology["frameworks"].append(
                    "Express"
                )

            if "fastify" in dependencies:
                technology["frameworks"].append(
                    "Fastify"
                )

            if "@nestjs/core" in dependencies:
                technology["frameworks"].append(
                    "NestJS"
                )

            if "koa" in dependencies:
                technology["frameworks"].append(
                    "Koa"
                )



            # ORMs

            if "@prisma/client" in dependencies or "prisma" in dependencies:
                technology["orms"].append(
                    "Prisma"
                )

            if "mongoose" in dependencies:
                technology["orms"].append(
                    "Mongoose"
                )

            if "sequelize" in dependencies:
                technology["orms"].append(
                    "Sequelize"
                )

            if "typeorm" in dependencies:
                technology["orms"].append(
                    "TypeORM"
                )
            


            # Build tools

            if "vite" in dependencies:
                technology["build_tools"].append(
                    "Vite"
                )

            if "webpack" in dependencies:
                technology["build_tools"].append(
                    "Webpack"
                )



            # Styling

            if "tailwindcss" in dependencies:
                technology["styling_tools"].append(
                    "Tailwind CSS"
                )



            # Testing

            if "jest" in dependencies:
                technology["testing_tools"].append(
                    "Jest"
                )

            if "vitest" in dependencies:
                technology["testing_tools"].append(
                    "Vitest"
                )



        # Detect JavaScript files

        javascript_files = []

        for extension in ["*.js", "*.jsx"]:

            for path in root.rglob(extension):

                if any(
                    part in IGNORED_DIRECTORIES
                    for part in path.parts
                ):
                    continue

                javascript_files.append(path)


        if javascript_files:
            technology["languages"].append(
                "JavaScript"
            )


        for key in [
            "languages",
            "frameworks",
            "orms",
            "migration_tools",
            "build_tools",
            "testing_tools",
            "styling_tools",
        ]:
            technology[key] = list(set(technology[key]))

            
        return {
            "technology": technology
        }