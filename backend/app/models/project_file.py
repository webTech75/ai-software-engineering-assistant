from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship,  Mapped, mapped_column

from app.db.database import Base


class ProjectFile(Base):
    __tablename__ = "project_files"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    path = Column(
        String(500),
        nullable=False
    )

    language = Column(
        String(50),
        nullable=True
    )

    extension = Column(
        String(20),
        nullable=True
    )

    size = Column(
        Integer,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    project = relationship(
        "Project",
        back_populates="files"
    )
    
    symbols = relationship(
        "ProjectSymbol",
        back_populates="project_file",
        cascade="all, delete-orphan"
    )