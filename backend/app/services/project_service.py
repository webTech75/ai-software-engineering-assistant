from json import scanner

from fastapi import HTTPException, status

from app.models.project import Project
from app.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate
from sqlalchemy.orm import Session
from app.analysis.scanner import ProjectScanner
from app.utils.file_storage import get_project_directory

class ProjectService:

    def __init__(self, db: Session):
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

        return self.repository.get_all_by_owner(
            current_user.id
        )

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

        return self.repository.update(project, data)

    def scan_project(
        self,
        project_id: int,
        current_user,
    ):
        project = self.get_project(project_id, current_user)

        project_dir = get_project_directory(project.id)

        scanner = ProjectScanner()

        return scanner.scan(str(project_dir))