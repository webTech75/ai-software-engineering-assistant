"""
Analyzer for detecting database models and relationships in projects.

Author: Amr Elhabbal | Powered by Meta AI Muse
"""

import ast
from pathlib import Path

from app.analysis.base import BaseAnalyzer
from app.utils.should_ignore import should_ignore


class ModelAnalyzer(BaseAnalyzer):

    name = "ModelAnalyzer"

    def analyze(self, project_directory):

        models = []

        root = Path(project_directory)

        for file in root.rglob("*.py"):

            if should_ignore(file):
                continue

            # Only scan model files
            if "models" not in file.parts:
                continue

            try:
                tree = ast.parse(file.read_text(encoding="utf-8"))

            except Exception:
                continue

            for node in ast.walk(tree):

                if isinstance(node, ast.ClassDef):

                    model = self.extract_model(node, file)

                    if model:
                        models.append(model)

        return {"total_models": len(models), "models": models}

    def extract_model(self, node, file):

        fields = []
        relationships = []
        table_name = None

        for item in node.body:

            if isinstance(item, ast.Assign):

                for target in item.targets:

                    if not isinstance(target, ast.Name):
                        continue

                    name = target.id

                    # Detect table name
                    if name == "__tablename__":

                        if isinstance(item.value, ast.Constant):
                            table_name = item.value.value

                        continue

                    value = ""

                    try:
                        value = ast.unparse(item.value)

                    except Exception:
                        pass

                    # Detect SQLAlchemy columns
                    if "Column(" in value or "mapped_column(" in value:

                        fields.append(name)

                    # Detect SQLAlchemy relationships
                    elif "relationship(" in value:

                        relationships.append(
                            {
                                "name": name,
                                "target": self.extract_relationship_target(item),
                            }
                        )

            # Support SQLAlchemy 2.x annotations
            if isinstance(item, ast.AnnAssign):

                if isinstance(item.target, ast.Name):

                    name = item.target.id

                    value = ""

                    try:
                        value = ast.unparse(item.value)

                    except Exception:
                        pass

                    if "Mapped[" in value or "mapped_column(" in value:

                        fields.append(name)

        # Only return real models
        if table_name or fields or relationships:

            return {
                "name": node.name,
                "file": str(file),
                "table": table_name,
                "fields": fields,
                "relationships": relationships,
            }

        return None

    def extract_relationship_target(self, node):

        try:

            text = ast.unparse(node.value)

        except Exception:

            return None

        start = text.find("(")
        end = text.find(")")

        if start != -1 and end != -1:

            value = text[start + 1 : end]

            return value.replace('"', "").replace("'", "").split(",")[0].strip()

        return None
