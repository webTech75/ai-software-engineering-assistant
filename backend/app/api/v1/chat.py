"""
===============================================================================
File: chat.py

Path: app/api/v1/chat.py

Description:
    Exposes the AI chat endpoint.

Responsibilities:
    - Authenticate the user.
    - Validate project ownership.
    - Save chat messages.
    - Forward requests to the AI agent.
    - Return the assistant response.

Author:
    Amr Elhabbal
===============================================================================
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.agent.service import AgentService
from app.api.dependencies import get_current_user
from app.api.v1.projects import get_project_service
from app.db.database import get_db
from app.models.user import User
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ChatMessageResponse,
)
from app.services.chat_service import ChatService
from app.services.project_service import ProjectService


router = APIRouter(
    prefix="/projects",
    tags=["AI"],
)


def get_chat_service(
    db: Session = Depends(get_db),
) -> ChatService:
    return ChatService(db)


@router.post(
    "/{project_id}/chat",
    response_model=ChatResponse,
)
def chat(
    project_id: int,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
    chat_service: ChatService = Depends(get_chat_service),
):
    # Verify the project belongs to the current user.
    project = project_service.get_project(
        project_id,
        current_user,
    )

    # Save the user's message.
    chat_service.create_message(
        project.id,
        "user",
        request.message,
    )

    # Ask the AI.
    agent = AgentService()

    answer = agent.ask(
        project,
        request.message,
    )

    # Save the AI response.
    chat_service.create_message(
        project.id,
        "assistant",
        answer,
    )

    return ChatResponse(
        answer=answer,
    )

@router.get(
    "/{project_id}/chat",
    response_model=list[ChatMessageResponse],
)
def get_chat_history(
    project_id: int,
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
    chat_service: ChatService = Depends(get_chat_service),
):
    project = project_service.get_project(
        project_id,
        current_user,
    )

    return chat_service.get_messages(project.id)