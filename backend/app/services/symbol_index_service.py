"""
===============================================================================
File: symbol_index_service.py
Path: app/services/symbol_index_service.py

Description:
    Service layer for building project symbol indexes.

Responsibilities:
    - Coordinate symbol indexing.
    - Provide project directory information.
    - Handle database operations through SymbolIndexer.

Author:
    Amr Elhabbal
===============================================================================
"""

from sqlalchemy.orm import Session

from app.agent.intelligence.symbol_indexer import SymbolIndexer


class SymbolIndexService:
    """
    Handles project code symbol indexing.
    """


    def __init__(
        self,
        db: Session,
    ):
        self.db = db



    def index_project(
        self,
        project_id: int,
        project_directory: str,
    ):

        indexer = SymbolIndexer(
            db=self.db,
            project_directory=project_directory,
        )


        return indexer.index_project(
            project_id=project_id
        )