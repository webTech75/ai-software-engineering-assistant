"""
===============================================================================
File:
    app/api/v1/chat.py

Description:
    Chat API endpoint.

Responsibilities:
    - Receive user messages.
    - Load project information.
    - Load limited conversation history.
    - Send request to Agent.
    - Save messages.
    - Return agent response.

Notes:
    - The Agent does not receive database models.
    - Only project filesystem information is passed
      when tools require file access.

===============================================================================
"""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.project import Project
from app.schemas.chat import ChatRequest, ChatResponse

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
    Create Agent instance with dependencies.
    """

    return Agent(
        planner=Planner(),
        executor=Executor(),
        response_builder=ResponseBuilder(),
        llm=LLMClient(),
    )


@router.post(
    "/{project_id}",
    response_model=ChatResponse,
)
def chat(
    project_id: int,
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    Send a message to the AI software engineering agent.
    """

    chat_service = ChatService(db)

    # -------------------------------------------------
    # Load project
    # -------------------------------------------------

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


    # -------------------------------------------------
    # Load previous conversation history
    # -------------------------------------------------

    history_messages = chat_service.get_messages(
        project_id
    )

    # Keep only recent messages
    history_messages = history_messages[-10:]


    history = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in history_messages
    ]


    logger.info(
        "Conversation history loaded: %s messages",
        len(history),
    )


    # -------------------------------------------------
    # Run AI agent
    # -------------------------------------------------

    agent = get_agent()

    response = agent.run(
        project_directory=project.project_directory,
        message=request.message,
        history=history,
    )


    # -------------------------------------------------
    # Save conversation
    # -------------------------------------------------

    chat_service.create_message(
        project_id=project.id,
        role="user",
        content=request.message,
    )

    chat_service.create_message(
        project_id=project.id,
        role="assistant",
        content=response,
    )


    # -------------------------------------------------
    # Return response
    # -------------------------------------------------

    return ChatResponse(
        answer=response
    )

@router.get(
    "/{project_id}/history",
)
def get_chat_history(
    project_id: int,
    db: Session = Depends(get_db),
):
    """
    Get previous chat messages for a project.
    """

    chat_service = ChatService(db)

    # -------------------------------------------------
    # Verify project exists
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Load messages
    # -------------------------------------------------

    messages = chat_service.get_messages(
        project_id
    )

    # -------------------------------------------------
    # Return clean response
    # -------------------------------------------------

    return [
        {
            "id": message.id,
            "role": message.role,
            "content": message.content,
            "created_at": message.created_at,
        }
        for message in messages
    ]