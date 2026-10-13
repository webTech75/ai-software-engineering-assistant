"""
===============================================================================
File: context_builder.py
Path: app/agent/context_builder.py

Description:
    Builds context information for AI agent reasoning.

Responsibilities:
    - Load project information.
    - Load indexed files.
    - Load indexed symbols.
    - Prepare structured context.

Notes:
    - Does not execute tools.
    - Does not create plans.
    - Provides information to the agent.

Author:
    Amr Elhabbal
===============================================================================
"""

from sqlalchemy.orm import Session

from app.models.project_file import ProjectFile
from app.models.project_symbol import ProjectSymbol


class ContextBuilder:
    """
    Builds project context for the AI agent.
    """


    def __init__(
        self,
        db: Session,
    ):
        self.db = db


    def build(
        self,
        project,
    ) -> dict:
        """
        Build project context.
        """

        files = (
            self.db.query(ProjectFile)
            .filter(
                ProjectFile.project_id == project.id
            )
            .all()
        )


        symbols = (
            self.db.query(ProjectSymbol)
            .join(ProjectFile)
            .filter(
                ProjectFile.project_id == project.id
            )
            .all()
        )


        return {
            "project": {
                "id": project.id,
                "name": project.name,
                "description": project.description,
            },

            "index": {
                "files_count": len(files),
                "symbols_count": len(symbols),
            },

            "files": [
                {
                    "path": file.path,
                    "language": file.language,
                    "extension": file.extension,
                }
                for file in files
            ],

            "symbols": [
                {
                    "name": symbol.name,
                    "type": symbol.type,
                }
                for symbol in symbols
            ],
        }