"""
===============================================================================
File: projects.py
Path: app/api/v1/projects.py

Description:
    Provides endpoints for managing software projects.

Responsibilities:
    - Create projects.
    - Retrieve projects.
    - Update project information.
    - Delete projects.
    - Ensure users can only access their own projects.

Notes:
    - All endpoints require authentication.
    - Project ownership is verified before any operation.

Author:
    Amr Elhabbal
===============================================================================
"""
from fastapi import APIRouter, Depends, Response, status, UploadFile, File, Query
from sqlalchemy.orm import Session

from app.utils.file_storage import save_uploaded_file, extract_zip
from app.db.database import get_db
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.schemas.project_scan import ProjectScanResponse
from app.api.dependencies import get_current_user
from app.services.project_service import ProjectService
from app.agent.tools.list_files import ListFilesTool
from app.agent.tools.read_file import ReadFileTool
from app.agent.tools.search_text import SearchTextTool

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    return ProjectService(db)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
):
    return service.create_project(data, current_user)


@router.get(
    "",
    response_model=list[ProjectResponse],
)
def get_projects(
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
):
    return service.get_projects(current_user)


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
):
    return service.get_project(project_id, current_user)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
):
    service.delete_project(project_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
):
    return service.update_project(
        project_id=project_id,
        data=data,
        current_user=current_user,
    )


@router.post("/{project_id}/upload")
def upload_project_file(
    project_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
):
    # Verify project exists and belongs to the user
    project = service.get_project(project_id, current_user)

    file_path = save_uploaded_file(project.id, file)

    if file.filename.lower().endswith(".zip"):
        extracted_path = extract_zip(project.id, file_path)

        # Save project directory
        project.project_directory = extracted_path
        service.save(project)

        return {
            "message": "ZIP uploaded and extracted successfully.",
            "project_directory": extracted_path,
        }

    return {
        "message": "File uploaded successfully.",
        "filename": file.filename,
        "path": file_path,
    }


@router.get(
    "/{project_id}/scan",
    response_model=ProjectScanResponse,
)
def scan_project_endpoint(
    project_id: int,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
):
    return service.scan_project(
        project_id,
        current_user,
    )


@router.get("/{project_id}/files")
def list_project_files(
    project_id: int,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
):
    project = service.get_project(project_id, current_user)

    tool = ListFilesTool()

    return tool.execute(project)


@router.get("/{project_id}/file")
def read_project_file(
    project_id: int,
    path: str,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
):
    # Verify the project exists and belongs to the user
    project = service.get_project(project_id, current_user)

    tool = ReadFileTool()

    content = tool.execute(project, path)

    return {
        "path": path,
        "content": content,
    }


@router.get("/{project_id}/search")
def search_project(
    project_id: int,
    query: str = Query(...),
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
):
    project = service.get_project(project_id, current_user)

    tool = SearchTextTool()

    return tool.execute(project, query)