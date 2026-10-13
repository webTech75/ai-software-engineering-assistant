"""
===============================================================================
File: code_parser.py
Path: app/agent/intelligence/code_parser.py

Description:
    Parses source code files and extracts code structure.

Responsibilities:
    - Read source files.
    - Extract classes.
    - Extract functions.
    - Extract imports.
    - Return structured metadata.

Notes:
    - Uses Python AST parser.
    - Additional languages can be added later.

Author:
    Amr Elhabbal
===============================================================================
"""

import ast
from pathlib import Path


class CodeParser:
    """
    Extracts code structure from project files.
    """


    def parse(
        self,
        file_path: str,
    ) -> dict:

        file = Path(file_path)

        if not file.exists():
            return {}


        if file.suffix.lower() != ".py":
            return {
                "language": "Unknown",
                "classes": [],
                "functions": [],
                "imports": [],
            }


        try:
            content = file.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            tree = ast.parse(content)

        except Exception:
            return {
                "language": "Python",
                "classes": [],
                "functions": [],
                "imports": [],
            }


        return {
            "language": "Python",
            "classes": self.extract_classes(tree),
            "functions": self.extract_functions(tree),
            "imports": self.extract_imports(tree),
        }



    def extract_classes(
        self,
        tree,
    ) -> list[str]:

        classes = []

        for node in ast.walk(tree):

            if isinstance(
                node,
                ast.ClassDef,
            ):
                classes.append(
                    node.name
                )

        return classes



    def extract_functions(
        self,
        tree,
    ) -> list[str]:

        functions = []

        for node in ast.walk(tree):

            if isinstance(
                node,
                ast.FunctionDef,
            ):
                functions.append(
                    node.name
                )

        return functions



    def extract_imports(
        self,
        tree,
    ) -> list[str]:

        imports = []

        for node in ast.walk(tree):

            if isinstance(
                node,
                ast.Import,
            ):
                for item in node.names:
                    imports.append(
                        item.name
                    )


            if isinstance(
                node,
                ast.ImportFrom,
            ):
                if node.module:
                    imports.append(
                        node.module
                    )

        return imports