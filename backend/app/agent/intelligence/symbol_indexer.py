"""
===============================================================================
File: symbol_indexer.py
Path: app/agent/intelligence/symbol_indexer.py

Description:
    Extracts and stores code symbols from project files.

Responsibilities:
    - Read indexed project files.
    - Parse source code.
    - Extract classes, functions, and imports.
    - Store symbols in the database.

Author:
    Amr Elhabbal
===============================================================================
"""

from sqlalchemy.orm import Session

from app.agent.intelligence.code_parser import CodeParser
from app.models.project_file import ProjectFile
from app.models.project_symbol import ProjectSymbol


class SymbolIndexer:
    """
    Builds a searchable symbol index for a project.
    """


    def __init__(
    self,
    db: Session,
    project_directory: str,
    ):
        self.db = db
        self.project_directory = project_directory
        self.parser = CodeParser()



    def index_project(
        self,
        project_id: int,
    ):

        files = (
            self.db.query(ProjectFile)
            .filter(
                ProjectFile.project_id == project_id
            )
            .all()
        )

        print("FILES FOUND:", len(files))
        indexed_symbols = []


        for project_file in files:

            result = self.parser.parse(
                f"{self.project_directory}/{project_file.path}"
            )

            print(
                f"Indexing file: {project_file.path}"
            )
            symbols = []


            for class_name in result.get(
                "classes",
                []
            ):
                symbols.append(
                    {
                        "name": class_name,
                        "type": "class",
                    }
                )


            for function_name in result.get(
                "functions",
                []
            ):
                symbols.append(
                    {
                        "name": function_name,
                        "type": "function",
                    }
                )


            for import_name in result.get(
                "imports",
                []
            ):
                symbols.append(
                    {
                        "name": import_name,
                        "type": "import",
                    }
                )



            for symbol in symbols:

                existing = (
                    self.db.query(ProjectSymbol)
                    .filter(
                        ProjectSymbol.project_file_id
                        == project_file.id,

                        ProjectSymbol.name
                        == symbol["name"],

                        ProjectSymbol.type
                        == symbol["type"],
                    )
                    .first()
                )


                if existing:
                    continue



                project_symbol = ProjectSymbol(
                    project_file_id=project_file.id,
                    name=symbol["name"],
                    type=symbol["type"],
                )


                self.db.add(
                    project_symbol
                )

                indexed_symbols.append(
                    project_symbol
                )


        self.db.commit()


        return indexed_symbols