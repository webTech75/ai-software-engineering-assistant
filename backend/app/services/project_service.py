"""
===============================================================================
File: project_service.py
Path: app/services/project_service.py

Description:
    Handles project management business logic.

Responsibilities:
    - Create, retrieve, update, and delete projects.
    - Validate project ownership.
    - Manage project analysis and file storage.

Notes:
    - Uses repository layer for database operations.

Author:
    Amr Elhabbal
===============================================================================
"""

from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.analysis.storage import AnalysisStorage
from app.utils.file_storage import (
    get_project_directory,
    get_existing_project_directory,
)


class ProjectService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = ProjectRepository(db)

    def create_project(
        self,
        data: ProjectCreate,
        current_user: User,
    ) -> Project:

        project = Project(
            name=data.name,
            description=data.description,
            owner_id=current_user.id,
        )

        return self.repository.create(project)

    def get_projects(
        self,
        current_user: User,
    ) -> list[Project]:

        return self.repository.get_all_by_owner(current_user.id)

    def get_project(
        self,
        project_id: int,
        current_user: User,
    ) -> Project:

        project = self.repository.get_by_id(project_id)

        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found.",
            )

        if project.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied.",
            )

        return project

    def delete_project(
        self,
        project_id: int,
        current_user: User,
    ) -> None:

        project = self.get_project(
            project_id,
            current_user,
        )

        self.remove_project_files(project)
        self.repository.delete(project)

    def update_project(
        self,
        project_id: int,
        data: ProjectUpdate,
        current_user: User,
    ) -> Project:

        project = self.repository.get_by_id(project_id)

        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found.",
            )

        if project.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to update this project.",
            )

        return self.repository.update(
            project,
            data,
        )

    def scan_project(
        self,
        project_id: int,
        current_user,
    ):
        """
        Return existing project analysis.

        Analysis is generated during upload.
        This endpoint only retrieves stored results.
        """

        project = self.get_project(
            project_id,
            current_user,
        )

        project_dir = get_project_directory(project.id)

        analysis_data = AnalysisStorage.load(str(project_dir))

        if not analysis_data:
            return {
                "status": "not_analyzed",
                "message": "Upload a project to generate analysis.",
            }

        report = analysis_data.get("report")

        if not report:
            raise ValueError("Project analysis report is missing.")

        return report

    def update_project_directory(
        self,
        project: Project,
        directory: str,
    ):
        project.project_directory = directory
        self.repository.commit()

    def save(
        self,
        project: Project,
    ) -> Project:

        return self.repository.save(project)

    def remove_project_files(
        self,
        project: Project,
    ) -> None:

        project_dir = get_existing_project_directory(project.id)

        if project_dir.exists():
            import shutil

            shutil.rmtree(project_dir)
