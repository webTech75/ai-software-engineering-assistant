"""
===============================================================================
File:
    app/api/v1/chat.py

Description:
    Chat API endpoint.

Responsibilities:
    - Receive user messages.
    - Load optional project context.
    - Load conversation history.
    - Execute AI agent.
    - Save messages.
    - Return response.

Does NOT:
    - Execute tools.
    - Manage planning.
    - Manage LLM communication.

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

from app.services.chat_service import ChatService


logger = logging.getLogger(__name__)



router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)



# -------------------------------------------------
# Shared dependencies
# -------------------------------------------------

llm_client = LLMClient()



def get_agent() -> Agent:
    """
    Create AI agent.

    Agent owns:
        - Router
        - Planner
        - Executor

    API only provides LLM dependency.
    """

    return Agent(
        llm=llm_client,
    )



def get_project(
    db: Session,
    project_id: int,
) -> Project:
    """
    Load project by id.
    """

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


    return project



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
    """

    chat_service = ChatService(db)


    project_directory = None



    # -------------------------------------------------
    # Load project context
    # -------------------------------------------------

    if request.project_id is not None:

        project = get_project(
            db,
            request.project_id,
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
        "Loaded chat history: %s messages",
        len(history),
    )



    # -------------------------------------------------
    # Execute Agent
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


    logger.info(
        "AI response generated successfully"
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
    Get conversation history.
    """


    chat_service = ChatService(db)



    if project_id is not None:

        get_project(
            db,
            project_id,
        )



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