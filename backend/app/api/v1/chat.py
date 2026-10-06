"""
===============================================================================
File: chat.py
Path: app/api/v1/chat.py

Description:
    Exposes the AI chat endpoint.

Responsibilities:
    - Authenticate the user.
    - Validate project ownership.
    - Forward user messages to the AI agent.
    - Return the assistant's response.

Notes:
    - Requires a valid JWT.
    - Users can only access their own projects.
    - Delegates all AI orchestration to AgentService.

Author:
    Amr Elhabbal
===============================================================================
"""

from fastapi import APIRouter, Depends

from app.agent.service import AgentService
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.project_service import ProjectService 
from app.api.dependencies import get_current_user
from app.api.v1.projects import get_project_service
from app.models.user import User

router = APIRouter(
    prefix="/projects",
    tags=["AI"],
)


@router.post(
    "/{project_id}/chat",
    response_model=ChatResponse,
)
def chat(
    project_id: int,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
):
    project = service.get_project(
        project_id,
        current_user,
    )

    agent = AgentService()

    answer = agent.ask(
        project,
        request.message,
    )

    return ChatResponse(
        answer=answer,
    )