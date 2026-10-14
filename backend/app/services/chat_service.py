from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage
from app.repositories.chat_repository import ChatRepository


class ChatService:
    """
    Service layer for chat operations.

    Responsibilities:
        - Create chat messages.
        - Load limited conversation history.
    """

    def __init__(
        self,
        db: Session
    ):
        self.repository = ChatRepository(db)


    def create_message(
        self,
        project_id: int,
        role: str,
        content: str,
    ) -> ChatMessage:
        """
        Save a chat message.
        """

        message = ChatMessage(
            project_id=project_id,
            role=role,
            content=content,
        )

        return self.repository.create(message)


    def get_messages(
        self,
        project_id: int,
        limit: int = 12,
    ):
        """
        Get recent conversation history.

        Only returns the latest messages
        to prevent sending huge context
        to the LLM.
        """

        messages = self.repository.get_by_project(
            project_id
        )

        return messages[-limit:]