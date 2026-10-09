from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage
from app.repositories.chat_repository import ChatRepository


class ChatService:

    def __init__(self, db: Session):
        self.repository = ChatRepository(db)

    def create_message(
        self,
        project_id: int,
        role: str,
        content: str,
    ) -> ChatMessage:

        message = ChatMessage(
            project_id=project_id,
            role=role,
            content=content,
        )

        return self.repository.create(message)

    def get_messages(self, project_id: int):
        return self.repository.get_by_project(project_id)