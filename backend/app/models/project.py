from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

from app.models.chat_message import ChatMessage

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    project_directory: Mapped[str] = mapped_column(
        String(500),
        nullable=True,
    )

    index_status = mapped_column(
        String(50),
        nullable=False,
        default="pending",
    )

    files_count = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    symbols_count = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    last_indexed_at = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    owner = relationship(
        "User",
        back_populates="projects",
    )
    files = relationship(
        "ProjectFile",
        back_populates="project",
        cascade="all, delete-orphan"
    )
    messages = relationship(
        "ChatMessage",
        back_populates="project",
        cascade="all, delete-orphan",
    )