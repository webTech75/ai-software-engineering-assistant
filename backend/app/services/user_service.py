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
from sqlalchemy.orm import Session
import secrets
from datetime import datetime, timedelta, timezone

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.core.security import create_access_token, verify_password
from app.schemas.auth import TokenResponse
from app.models.password_reset_token import PasswordResetToken
from app.repositories.password_reset_token_repository import (
    PasswordResetTokenRepository,
)


class UserService:

    def __init__(self, db: Session):
        self.repository = UserRepository(db)
        self.password_reset_repository = PasswordResetTokenRepository(db)
    def create_user(self, data: UserCreate) -> User:

        username = data.username.strip().lower()
        email = data.email.strip().lower()

        if self.repository.get_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists."
            )

        if self.repository.get_by_username(username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists."
            )

        password_hash = hash_password(data.password)

        user = User(
            username=username,
            email=email,
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

    def forgot_password(self, email: str):

        email = email.strip().lower()

        user = self.repository.get_by_email(email)

        if not user:
            return

        token = secrets.token_urlsafe(32)

        expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)

        password_reset = PasswordResetToken(
            user_id=user.id,
            token=token,
            expires_at=expires_at,
        )

        self.password_reset_repository.create(password_reset)

        print("\n==============================")
        print("PASSWORD RESET LINK")
        print(f"http://localhost:5173/reset-password?token={token}")
        print("==============================\n")

    def reset_password(self, token: str, password: str):

        password_reset = self.password_reset_repository.get_by_token(token)

        if not password_reset:
            raise ValueError("Invalid or expired reset link.")

        if password_reset.used:
            raise ValueError("This reset link has already been used.")

        if password_reset.expires_at < datetime.now():
            raise ValueError("This reset link has expired.")

        user = password_reset.user

        user.password_hash = hash_password(password)

        password_reset.used = True

        self.password_reset_repository.update()