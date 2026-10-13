from pathlib import Path
import ast

from app.analysis.base import BaseAnalyzer
from app.analysis.constants import IGNORED_DIRECTORIES


class MetricsAnalyzer(BaseAnalyzer):

    name = "MetricsAnalyzer"


    def analyze(self, project_directory):

        root = Path(project_directory)

        result = {
            "files_analyzed": 0,
            "total_lines": 0,
            "code_lines": 0,
            "comment_lines": 0,
            "blank_lines": 0,
            "total_functions": 0,
            "total_classes": 0,
            "total_imports": 0,
            "files": []
        }


        for file in root.rglob("*"):

            if self.should_ignore(file):
                continue


            if not file.is_file():
                continue


            if file.suffix == ".py":

                metrics = self.analyze_python_file(file)

                result["files_analyzed"] += 1

                result["total_lines"] += metrics["lines"]
                result["code_lines"] += metrics["code_lines"]
                result["comment_lines"] += metrics["comments"]
                result["blank_lines"] += metrics["blank_lines"]

                result["total_functions"] += metrics["functions"]
                result["total_classes"] += metrics["classes"]
                result["total_imports"] += metrics["imports"]


                result["files"].append(
                    {
                        "file": str(file),
                        **metrics
                    }
                )


        return {
            "metrics": result
        }



    def analyze_python_file(self, file):

        metrics = {
            "lines": 0,
            "code_lines": 0,
            "comments": 0,
            "blank_lines": 0,
            "functions": 0,
            "classes": 0,
            "imports": 0
        }


        try:

            content = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            lines = content.splitlines()

            metrics["lines"] = len(lines)


            for line in lines:

                stripped = line.strip()

                if not stripped:
                    metrics["blank_lines"] += 1

                elif stripped.startswith("#"):
                    metrics["comments"] += 1

                else:
                    metrics["code_lines"] += 1



            tree = ast.parse(content)


            for node in ast.walk(tree):

                if isinstance(
                    node,
                    ast.FunctionDef
                ):
                    metrics["functions"] += 1


                elif isinstance(
                    node,
                    ast.ClassDef
                ):
                    metrics["classes"] += 1


                elif isinstance(
                    node,
                    (
                        ast.Import,
                        ast.ImportFrom
                    )
                ):
                    metrics["imports"] += 1


        except Exception:
            pass


        return metrics



    def should_ignore(self, path):

        return any(
            part in IGNORED_DIRECTORIES
            for part in path.parts
        )