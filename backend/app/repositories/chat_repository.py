"""
===============================================================================
File:
    app/repositories/chat_repository.py

Description:
    Repository layer for chat storage.

Responsibilities:
    - Save chat messages.
    - Load general conversations.
    - Load project conversations.

===============================================================================
"""

from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage



class ChatRepository:
    """
    Repository layer for chat storage.

    Supports:

        project_id=None
            General Neura conversation

        project_id=<id>
            Project conversation
    """



    def __init__(
        self,
        db: Session,
    ):
        self.db = db



    def create(
        self,
        message: ChatMessage,
    ) -> ChatMessage:
        """
        Save chat message.
        """


        self.db.add(message)

        self.db.commit()

        self.db.refresh(message)


        return message



    def get_messages(
        self,
        project_id: int | None = None,
    ) -> list[ChatMessage]:
        """
        Get conversation history.

        None:
            General Neura conversation.

        ID:
            Project conversation.
        """


        query = (
            self.db.query(ChatMessage)
        )


        if project_id is None:

            query = query.filter(
                ChatMessage.project_id.is_(None)
            )

        else:

            query = query.filter(
                ChatMessage.project_id == project_id
            )


        messages = (
            query
            .order_by(
                ChatMessage.created_at.desc(),
                ChatMessage.id.desc(),
            )
            .limit(12)
            .all()
        )


        messages.reverse()


        return messages