"""
===============================================================================
File: user_repository.py
Path: app/repositories/user_repository.py

Description:
    Provides database access operations for User entities.

Responsibilities:
    - Create users.
    - Retrieve users.
    - Update users.
    - Delete users.

Notes:
    - Contains persistence logic only.
    - Business logic belongs in the service layer.

Author:
    Amr Elhabbal
===============================================================================
"""

from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_by_username(self, username: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.username == username)
            .first()
        )

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_email(self, email: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_by_id(self, user_id: int) -> User | None:
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )