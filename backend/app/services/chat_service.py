"""
===============================================================================
File:
    app/services/chat_service.py

Description:
    Service layer for chat operations.

Responsibilities:
    - Create chat messages.
    - Load conversation history.
    - Support general and project conversations.

===============================================================================
"""

from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage
from app.repositories.chat_repository import ChatRepository



class ChatService:
    """
    Service layer for chat operations.

    Supports:

        General AI chat:
            project_id=None

        Project chat:
            project_id=<project id>
    """



    def __init__(
        self,
        db: Session,
    ):
        self.repository = ChatRepository(db)



    def create_message(
        self,
        project_id: int | None,
        role: str,
        content: str,
    ) -> ChatMessage:
        """
        Save a chat message.

        project_id can be None for general conversations.
        """


        message = ChatMessage(
            project_id=project_id,
            role=role,
            content=content,
        )


        return self.repository.create(
            message
        )



    def get_messages(
        self,
        project_id: int | None = None,
    ):
        """
        Get recent conversation history.

        None:
            General conversation history.

        ID:
            Project conversation history.
        """


        return self.repository.get_messages(
            project_id
        )