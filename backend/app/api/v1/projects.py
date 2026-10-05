from fastapi import APIRouter, Depends, Response, status, UploadFile, File
from sqlalchemy.orm import Session

from app.utils.file_storage import save_uploaded_file, extract_zip
from app.db.database import get_db
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.schemas.project_scan import ProjectScanResponse
from app.api.dependencies import get_current_user
from app.services.project_service import ProjectService

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


@router.post(
    "/{project_id}/upload",
)
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