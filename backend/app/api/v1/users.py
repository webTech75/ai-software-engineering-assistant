# Defines HTTP endpoints.
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db.database import get_db
from app.schemas.user import UserCreate
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

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
    }