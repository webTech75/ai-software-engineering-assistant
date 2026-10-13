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
from fastapi import APIRouter, Depends, Response, status, UploadFile, File, Query, HTTPException
from sqlalchemy.orm import Session

from app.utils.file_storage import save_uploaded_file, extract_zip
from app.db.database import get_db
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.schemas.project_scan import ProjectScanResponse
from app.api.dependencies import get_current_user
from app.services.project_service import ProjectService
from app.services.symbol_index_service import SymbolIndexService
from app.services.file_index_service import FileIndexService
from app.agent.tools.list_files import ListFilesTool
from app.agent.tools.read_file import ReadFileTool
from app.agent.tools.search_text import SearchTextTool
from app.models.project import Project
from app.services.project_index_service import ProjectIndexService
from app.api.dependencies import get_project_index_service


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
    index_service: ProjectIndexService = Depends(get_project_index_service),
):
    # Verify project exists and belongs to the user
    project = service.get_project(project_id, current_user)

    file_path = save_uploaded_file(project.id, file)

    if file.filename.lower().endswith(".zip"):
        extracted_path = extract_zip(project.id, file_path)

        project.project_directory = extracted_path
        service.save(project)

        result = index_service.reindex_project(
            project_id=project.id,
            project_directory=extracted_path,
        )

        return {
            "message": "ZIP uploaded and indexed successfully.",
            "project_directory": extracted_path,
            **result,
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


# @router.post("/{project_id}/index-symbols")
# def index_project_symbols(
#     project_id: int,
#     db: Session = Depends(get_db),
# ):

#     project = (
#         db.query(Project)
#         .filter(Project.id == project_id)
#         .first()
#     )

#     if not project:
#         raise HTTPException(
#             status_code=404,
#             detail="Project not found"
#         )


#     service = SymbolIndexService(db)

#     symbols = service.index_project(
#         project_id=project.id,
#         project_directory=project.project_directory,
#     )


#     return {
#         "message": "Project symbols indexed successfully",
#         "symbols_indexed": len(symbols),
#     }

# @router.post("/{project_id}/index-files")
# def index_project_files(
#     project_id: int,
#     db: Session = Depends(get_db),
# ):
#     project = db.query(Project).filter(
#         Project.id == project_id
#     ).first()

#     if not project:
#         raise HTTPException(
#             status_code=404,
#             detail="Project not found"
#         )

#     service = FileIndexService(db)

#     files = service.index_project(
#         project.id,
#         project.project_directory
#     )

#     return {
#         "message": "Project files indexed successfully",
#         "files_indexed": len(files)
#     }

@router.delete("/{project_id}/cleanup-index")
def cleanup_project_index(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    service = ProjectIndexService(db)

    service.cleanup(project_id)

    return {
        "message": "Project index cleaned successfully",
        "project_id": project_id,
    }

@router.post("/{project_id}/reindex")
def reindex_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    service = ProjectIndexService(db)

    result = service.reindex_project(
        project_id=project.id,
        project_directory=project.project_directory,
    )

    return {
        "message": "Project reindexed successfully",
        **result,
    }

@router.get("/{project_id}/index-status")
def get_project_index_status(
    project_id: int,
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
    index_service: ProjectIndexService = Depends(get_project_index_service),
):
    project_service.get_project(
        project_id,
        current_user,
    )

    return index_service.get_index_status(project_id)