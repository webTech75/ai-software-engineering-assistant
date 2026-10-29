"""
Analyzer for measuring code complexity and function metrics.

Author: Amr Elhabbal | Powered by Meta AI Muse
"""

import ast
from pathlib import Path

from app.analysis.base import BaseAnalyzer
from app.utils.should_ignore import should_ignore


class ComplexityAnalyzer(BaseAnalyzer):

    name = "ComplexityAnalyzer"

    def analyze(self, project_directory):

        root = Path(project_directory)

        result = {
            "files_analyzed": 0,
            "total_functions": 0,
            "total_complexity": 0,
            "average_complexity": 0,
            "functions": [],
            "highest_complexity": [],
        }

        for file in root.rglob("*"):

            if should_ignore(file):
                continue

            if not file.is_file():
                continue

            if file.suffix == ".py":

                data = self.analyze_python_file(file, root)

                result["files_analyzed"] += 1

                result["total_functions"] += len(data)

                for function in data:

                    result["total_complexity"] += function["complexity"]

                    result["functions"].append(function)

        if result["total_functions"]:

            result["average_complexity"] = round(
                result["total_complexity"] / result["total_functions"], 2
            )

        result["highest_complexity"] = sorted(
            result["functions"], key=lambda x: x["complexity"], reverse=True
        )[:10]

        return {"complexity": result}

    def analyze_python_file(self, file, root):

        results = []

        try:

            content = file.read_text(encoding="utf-8", errors="ignore")

            tree = ast.parse(content)

            for node in ast.walk(tree):

                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                    complexity = 1 + self.calculate_complexity(node)

                    results.append(
                        {
                            "file": str(file.relative_to(root)),
                            "function": node.name,
                            "complexity": complexity,
                        }
                    )

        except Exception:

            pass

        return results

    def calculate_complexity(self, node):

        complexity = 0

        for child in ast.walk(node):

            if isinstance(
                child, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.With)
            ):
                complexity += 1

            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1

        return complexity
