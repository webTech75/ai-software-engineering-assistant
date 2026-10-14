from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage


class ChatRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, message: ChatMessage) -> ChatMessage:
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_by_project(self, project_id: int) -> list[ChatMessage]:
        messages = (
            self.db.query(ChatMessage)
            .filter(ChatMessage.project_id == project_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(12)
            .all()
        )

        messages = list(reversed(messages))

        while messages and messages[0].role != "user":
            messages.pop(0)

        return messages[-12:]