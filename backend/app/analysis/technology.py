"""
Analyzer for detecting project technology stack.

Identifies languages, frameworks, databases, tools, and dependencies.

Author:
    Amr Elhabbal
    Powered by Meta AI Muse
"""

import json
from pathlib import Path

from app.analysis.base import BaseAnalyzer
from app.utils.should_ignore import should_ignore


class TechnologyAnalyzer(BaseAnalyzer):
    """
    Analyze project technology stack.
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

        self.detect_python(root, technology)
        self.detect_requirements(root, technology)
        self.detect_env_database(root, technology)
        self.detect_prisma(root, technology)
        self.detect_javascript(root, technology)

        self.cleanup(technology)

        return {"technology": technology}

    def detect_python(self, root, technology):

        python_files = [path for path in root.rglob("*.py") if not should_ignore(path)]

        if python_files:
            technology["languages"].append("Python")

    def detect_env_database(self, root, technology):

        env_files = [path for path in root.rglob(".env*") if not should_ignore(path)]

        for env_file in env_files:

            try:
                content = env_file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                ).lower()

            except Exception:
                continue

            databases = [
                ("postgresql", "PostgreSQL"),
                ("postgres", "PostgreSQL"),
                ("mysql", "MySQL"),
                ("mongodb", "MongoDB"),
                ("sqlite", "SQLite"),
            ]

            for keyword, database in databases:

                if keyword in content:
                    technology["database"] = database
                    return

    def detect_requirements(self, root, technology):

        requirements = next(
            (
                path
                for path in root.rglob("requirements.txt")
                if not should_ignore(path)
            ),
            None,
        )

        if not requirements:
            return

        try:
            content = requirements.read_text(
                encoding="utf-8",
                errors="ignore",
            ).lower()

        except Exception:
            return

        technology["package_manager"] = "pip"

        checks = {
            "FastAPI": ("frameworks", "fastapi"),
            "SQLAlchemy": ("orms", "sqlalchemy"),
            "Alembic": ("migration_tools", "alembic"),
        }

        for name, (category, keyword) in checks.items():

            if keyword in content:
                technology[category].append(name)

        self.detect_python_database(content, technology)

    def detect_python_database(self, content, technology):

        databases = [
            ("postgresql", "PostgreSQL"),
            ("psycopg", "PostgreSQL"),
            ("psycopg2", "PostgreSQL"),
            ("asyncpg", "PostgreSQL"),
            ("mysql", "MySQL"),
            ("pymysql", "MySQL"),
            ("pymongo", "MongoDB"),
            ("sqlite", "SQLite"),
        ]

        for keyword, database in databases:

            if keyword in content:
                technology["database"] = database
                return

    def detect_prisma(self, root, technology):

        prisma_file = next(
            (path for path in root.rglob("schema.prisma") if not should_ignore(path)),
            None,
        )

        if not prisma_file:
            return

        try:
            content = prisma_file.read_text(
                encoding="utf-8",
                errors="ignore",
            ).lower()

        except Exception:
            return

        if "postgresql" in content:
            technology["database"] = "PostgreSQL"

        elif "mysql" in content:
            technology["database"] = "MySQL"

        elif "sqlite" in content:
            technology["database"] = "SQLite"

        elif "mongodb" in content:
            technology["database"] = "MongoDB"

    def detect_javascript(self, root, technology):

        package_file = next(
            (path for path in root.rglob("package.json") if not should_ignore(path)),
            None,
        )

        if not package_file:
            return

        try:
            data = json.loads(
                package_file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
            )

        except Exception:
            return

        dependencies = {
            **data.get("dependencies", {}),
            **data.get("devDependencies", {}),
        }

        self.detect_js_language(root, technology)
        self.detect_package_manager(root, technology)
        self.detect_frameworks(dependencies, technology)
        self.detect_orms(dependencies, technology)
        self.detect_tools(dependencies, technology)

    def detect_js_language(self, root, technology):

        ts_files = [x for x in root.rglob("*.ts") if not should_ignore(x)]

        js_files = [x for x in root.rglob("*.js") if not should_ignore(x)]

        if ts_files:
            technology["languages"].append("TypeScript")

        if js_files:
            technology["languages"].append("JavaScript")

    def detect_package_manager(self, root, technology):

        if (root / "package-lock.json").exists():
            technology["package_manager"] = "npm"

        elif (root / "yarn.lock").exists():
            technology["package_manager"] = "yarn"

        elif (root / "pnpm-lock.yaml").exists():
            technology["package_manager"] = "pnpm"

        else:
            technology["package_manager"] = "npm"

    def detect_frameworks(self, dependencies, technology):

        frameworks = {
            "react": "React",
            "next": "Next.js",
            "express": "Express",
            "fastify": "Fastify",
            "@nestjs/core": "NestJS",
            "koa": "Koa",
        }

        for package, name in frameworks.items():

            if package in dependencies:
                technology["frameworks"].append(name)

    def detect_orms(self, dependencies, technology):

        orms = {
            "@prisma/client": "Prisma",
            "prisma": "Prisma",
            "mongoose": "Mongoose",
            "sequelize": "Sequelize",
            "typeorm": "TypeORM",
        }

        for package, name in orms.items():

            if package in dependencies:
                technology["orms"].append(name)

    def detect_tools(self, dependencies, technology):

        tools = {
            "vite": ("build_tools", "Vite"),
            "webpack": ("build_tools", "Webpack"),
            "tailwindcss": ("styling_tools", "Tailwind CSS"),
            "jest": ("testing_tools", "Jest"),
            "vitest": ("testing_tools", "Vitest"),
        }

        for package, (category, name) in tools.items():

            if package in dependencies:
                technology[category].append(name)

    def cleanup(self, technology):

        list_fields = [
            "languages",
            "frameworks",
            "orms",
            "migration_tools",
            "build_tools",
            "testing_tools",
            "styling_tools",
        ]

        for key in list_fields:
            technology[key] = sorted(set(technology[key]))
