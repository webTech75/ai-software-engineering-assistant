"""
===============================================================================
File:
    app/api/v1/chat.py

Description:
    Chat API endpoint for interacting with the Neura AI agent.

Responsibilities:
    - Receive user messages.
    - Load project context and conversation history.
    - Execute the AI agent.
    - Save and return responses.

Does NOT:
    - Execute tools directly.
    - Analyze projects.
    - Communicate with the LLM directly.

Author:
    Amr Elhabbal
===============================================================================
"""

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
    UploadFile,
    File,
    Query,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.utils.file_storage import save_uploaded_file, extract_zip
from app.db.database import get_db
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.schemas.project_scan import ProjectScanResponse
from app.api.dependencies import get_current_user
from app.services.project_service import ProjectService
from app.agent.tools.read_file import ReadFileTool
from app.agent.tools.search_text import SearchTextTool
from app.agent.agent import Agent
from app.ai.llm.client import LLMClient
from app.analysis.scanner import ProjectScanner
from app.analysis.storage import AnalysisStorage
from app.analysis.context_builder import ProjectContextBuilder
from app.utils.file_storage import get_project_directory

llm_client = LLMClient()


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


def get_agent() -> Agent:
    return Agent(llm=llm_client)


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
        from pathlib import Path

        print("EXTRACTED PATH:", extracted_path)

        print("FILES AFTER EXTRACT:", list(Path(extracted_path).rglob("*"))[:20])

        project.project_directory = extracted_path
        service.save(project)
        print("FILES BEFORE SCAN:", list(Path(extracted_path).rglob("*"))[:20])
        scanner = ProjectScanner()

        analysis = scanner.scan(extracted_path)

        # Build AI context once
        context = ProjectContextBuilder.build(
            project.name,
            analysis,
        )

        # Store analysis + context
        analysis_data = {
            "report": analysis,
            "context": context,
        }

        AnalysisStorage.save(
            str(get_project_directory(project.id)),
            analysis_data,
        )

        agent = get_agent()

        welcome = agent.get_project_welcome(
            project.name,
            context,
        )

        return {
            "message": "ZIP uploaded successfully.",
            "project_id": project.id,
            "project_directory": extracted_path,
            "welcome": welcome,
        }

    return {
        "message": "File uploaded successfully.",
        "filename": file.filename,
        "path": file_path,
    }


@router.get(
    "/{project_id}/scan",
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
