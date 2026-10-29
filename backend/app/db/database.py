"""
Database configuration and session management.

Provides SQLAlchemy engine setup,
database sessions, and declarative base.


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

connect_args = {}

if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
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
