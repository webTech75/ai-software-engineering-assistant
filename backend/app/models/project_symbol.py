"""
===============================================================================
File: project_symbol.py
Path: app/models/project_symbol.py

Description:
    Stores extracted code symbols for AI code intelligence.

Responsibilities:
    - Store classes.
    - Store functions.
    - Store imports and other code symbols.
    - Link symbols to project files.

Author:
    Amr Elhabbal
===============================================================================
"""

from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)

from app.db.database import Base


class ProjectSymbol(Base):
    """
    Represents a code symbol extracted from a project file.
    """

    __tablename__ = "project_symbols"


    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )


    project_file_id = Column(
        Integer,
        ForeignKey("project_files.id"),
        nullable=False,
    )


    name = Column(
        String(255),
        nullable=False,
    )


    type = Column(
        String(50),
        nullable=False,
    )


    line_number = Column(
        Integer,
        nullable=True,
    )


    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )