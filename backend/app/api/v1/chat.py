"""
===============================================================================
File:
    app/api/v1/chat.py

Description:
    Chat API endpoint.

Responsibilities:
    - Receive user messages.
    - Support general AI conversations.
    - Support optional project context.
    - Load conversation history.
    - Execute AI agent.
    - Save messages.
    - Return response.

Architecture:

    User
      |
      v
    Chat API
      |
      +----------------+
      |                |
 General Chat     Project Chat
      |                |
      v                v
    LLM          Project Tools

===============================================================================
"""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.project import Project

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)

from app.ai.llm.client import LLMClient

from app.agent.agent import Agent
from app.agent.planner import Planner
from app.agent.executor import Executor
from app.agent.response_builder import ResponseBuilder

from app.services.chat_service import ChatService


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


def get_agent() -> Agent:
    """
    Create AI agent.
    """

    return Agent(
        planner=Planner(),
        executor=Executor(),
        response_builder=ResponseBuilder(),
        llm=LLMClient(),
    )


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    Send message to Neura.

    Supports:

    General:

        {
            "message": "Explain FastAPI"
        }


    Project:

        {
            "message": "Review main.py",
            "project_id": 1
        }

    """

    chat_service = ChatService(db)

    project_directory = None


    # -------------------------------------------------
    # Load project only when provided
    # -------------------------------------------------

    if request.project_id is not None:

        project = (
            db.query(Project)
            .filter(
                Project.id == request.project_id
            )
            .first()
        )


        if not project:

            raise HTTPException(
                status_code=404,
                detail="Project not found",
            )


        project_directory = (
            project.project_directory
        )


    # -------------------------------------------------
    # Load conversation history
    # -------------------------------------------------

    history_messages = chat_service.get_messages(
        project_id=request.project_id
    )


    history = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in history_messages
    ]


    logger.info(
        "History loaded: %s messages",
        len(history),
    )


    # -------------------------------------------------
    # Run Agent
    # -------------------------------------------------

    agent = get_agent()


    response = agent.run(
        message=request.message,
        project_directory=project_directory,
        history=history,
    )


    if not response:

        response = (
            "I was unable to generate a response. "
            "Please try again."
        )


    # -------------------------------------------------
    # Save conversation
    # -------------------------------------------------

    chat_service.create_message(
        project_id=request.project_id,
        role="user",
        content=request.message,
    )


    chat_service.create_message(
        project_id=request.project_id,
        role="assistant",
        content=response,
    )


    return ChatResponse(
        answer=response
    )



@router.get(
    "/history",
)
def get_chat_history(
    project_id: int | None = None,
    db: Session = Depends(get_db),
):
    """
    Get chat history.

    Without project_id:
        Returns general chat.

    With project_id:
        Returns project conversation.
    """

    chat_service = ChatService(db)


    # -------------------------------------------------
    # Validate project
    # -------------------------------------------------

    if project_id is not None:

        project = (
            db.query(Project)
            .filter(
                Project.id == project_id
            )
            .first()
        )


        if not project:

            raise HTTPException(
                status_code=404,
                detail="Project not found",
            )


    # -------------------------------------------------
    # Load messages
    # -------------------------------------------------

    messages = chat_service.get_messages(
        project_id=project_id
    )


    return [
        {
            "id": message.id,
            "role": message.role,
            "content": message.content,
            "created_at": message.created_at,
        }
        for message in messages
    ]