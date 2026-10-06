"""
===============================================================================
File: database.py
Path: app/db/database.py

Description:
    Configures the application's database connection and session factory.

Responsibilities:
    - Create the SQLAlchemy engine.
    - Configure session management.
    - Provide database sessions.
    - Initialize the declarative base.

Notes:
    - A new database session should be created per request.
    - Sessions should always be closed after use.
    - This module is the central entry point for database access.

Author:
    Amr Elhabbal
===============================================================================
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from collections.abc import Generator
from sqlalchemy.orm import Session

from app.core.config import settings

# SQLAlchemy engine used to communicate with the database.
engine = create_engine(
    settings.database_url,
    echo=True
)

# Factory used to create independent database sessions.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass

# Dependency to get the database session
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()