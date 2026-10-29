"""
===============================================================================
File:
    app/services/chat_service.py

Description:
    Chat operations service layer.

Author:
    Amr Elhabbal
===============================================================================
"""

from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage
from app.repositories.chat_repository import ChatRepository

MAX_CHAT_LENGTH = 10000


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
        # MAX_MESSAGE_LENGTH = 20000

        if len(content) > MAX_CHAT_LENGTH:
            content = content[:MAX_CHAT_LENGTH] + "\n\n[Message truncated]"

        message = ChatMessage(
            project_id=project_id,
            role=role,
            content=content,
        )

        return self.repository.create(message)

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

        return self.repository.get_messages(project_id)
