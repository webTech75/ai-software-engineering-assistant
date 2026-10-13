from sqlalchemy.orm import Session
from datetime import datetime, timezone
from fastapi import HTTPException, status
from app.models.project import Project
from app.models.project_file import ProjectFile
from app.models.project_symbol import ProjectSymbol

from app.services.file_index_service import FileIndexService
from app.services.symbol_index_service import SymbolIndexService


class ProjectIndexService:
    """
    Handles the complete project indexing workflow.
    """

    def __init__(self, db: Session):
        self.db = db

        self.file_service = FileIndexService(db)
        self.symbol_service = SymbolIndexService(db)


    def cleanup(self, project_id: int):
        """
        Remove existing indexed data for a project.
        """

        file_ids = (
            self.db.query(ProjectFile.id)
            .filter(
                ProjectFile.project_id == project_id
            )
            .all()
        )

        file_ids = [
            file_id[0]
            for file_id in file_ids
        ]


        if file_ids:
            self.db.query(ProjectSymbol).filter(
                ProjectSymbol.project_file_id.in_(file_ids)
            ).delete(
                synchronize_session=False
            )


        self.db.query(ProjectFile).filter(
            ProjectFile.project_id == project_id
        ).delete(
            synchronize_session=False
        )

        project = (
            self.db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

        if project:
            project.index_status = "pending"
            project.files_count = 0
            project.symbols_count = 0
            project.last_indexed_at = None

        self.db.commit()


    def reindex_project(
        self,
        project_id: int,
        project_directory: str,
    ):
        """
        Completely rebuild project index.
        """

        project = (
            self.db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        try:
            # 1. Mark indexing started
            project.index_status = "indexing"

            self.db.commit()

            # 2. Remove old index
            self.cleanup(project_id)


            # 3. Index files
            files = self.file_service.index_project(
                project_id=project_id,
                project_directory=project_directory,
            )

            if not files:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail= "No project files found during indexing."
                )

            # 4. Index symbols
            symbols = self.symbol_service.index_project(
                project_id=project_id,
                project_directory=project_directory,
            )

            # 5. Update project metadata
            project.index_status = "completed"
    
            project.files_count = len(files)
    
            project.symbols_count = len(symbols)
    
            project.last_indexed_at = datetime.now(timezone.utc)
    
    
            self.db.commit()
    
            self.db.refresh(project)

            return {
                "files_indexed": len(files),
                "symbols_indexed": len(symbols),
                "status": project.index_status,
                "last_indexed_at": project.last_indexed_at,
            }

        except Exception:

            project.index_status = "failed from Amr"

            self.db.commit()

            raise

    def get_index_status(
        self,
        project_id: int,
    ):
        project = (
            self.db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        return {
            "project_id": project.id,
            "status": project.index_status,
            "files_indexed": project.files_count,
            "symbols_indexed": project.symbols_count,
            "last_indexed_at": project.last_indexed_at,
        }