"""
===============================================================================
File:
    app/models/project_file.py

Description:
    Defines the database model for project source files.

Responsibilities:
    - Store project file metadata.
    - Track file path, language, extension, and size.
    - Connect files with projects and extracted symbols.

Notes:
    - Each file belongs to a project.
    - File records are removed when the parent project is deleted.

Author:
    Amr Elhabbal
===============================================================================
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.database import Base


class ProjectFile(Base):
    __tablename__ = "project_files"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    path = Column(String(500), nullable=False)

    language = Column(String(50), nullable=True)

    extension = Column(String(20), nullable=True)

    size = Column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    project = relationship("Project", back_populates="files")

    symbols = relationship(
        "ProjectSymbol", back_populates="project_file", cascade="all, delete-orphan"
    )
