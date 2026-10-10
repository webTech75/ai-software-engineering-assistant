"""
===============================================================================
File: users.py
Path: app/api/v1/users.py

Description:
    Provides user authentication and account management endpoints.

Responsibilities:
    - Register new users.
    - Authenticate existing users.
    - Return JWT access tokens.
    - Retrieve authenticated user information.

Notes:
    - Passwords are never stored in plain text.
    - JWT authentication secures protected endpoints.

Author:
    Amr Elhabbal
===============================================================================
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db.database import get_db
from app.schemas.user import UserCreate, ForgotPasswordRequest, ResetPasswordRequest
from app.services.user_service import UserService
from app.schemas.auth import LoginRequest, TokenResponse
from app.api.dependencies import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register")

def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    service = UserService(db)

    created_user = service.create_user(user)

    return {
        "id": created_user.id,
        "username": created_user.username,
        "email": created_user.email,
    }

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    service = UserService(db)

    return service.login(
        username=form_data.username,
        password=form_data.password,
    )

@router.post("/forgot-password")

def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    service = UserService(db)
    service.forgot_password(request.email)
    return {
        "message": "If an account exists, a password reset email should be sent shortly."
    }

@router.post("/reset-password")

def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    try: 
        service.reset_password(
            token=request.token,
            password=request.password,
        )
        return {
            "message": "Your password has been reset successfully."
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("/me")

def get_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
    }