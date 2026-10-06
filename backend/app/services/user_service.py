"""
===============================================================================
File: user_service.py
Path: app/services/user_service.py

Description:
    Contains the business logic for user management.

Responsibilities:
    - Register new users.
    - Authenticate users.
    - Retrieve user information.
    - Coordinate repository operations.

Notes:
    - Business rules belong in this layer.
    - Database access is delegated to the repository layer.
    - Password hashing and verification should be handled through the
      application's security utilities.

Author:
    Amr Elhabbal
===============================================================================
"""
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.core.security import create_access_token, verify_password
from app.schemas.auth import LoginRequest, TokenResponse

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class UserService:

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, data: UserCreate) -> User:

        if self.repository.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists."
            )

        if self.repository.get_by_username(data.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists."
            )

        password_hash = hash_password(data.password)

        user = User(
            username=data.username,
            email=data.email,
            password_hash=password_hash,
        )

        return self.repository.create(user)

    def login(self, username: str, password: str) -> TokenResponse:

        user = self.repository.get_by_username(username)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        token = create_access_token(str(user.id))

        return TokenResponse(
            access_token=token
        )