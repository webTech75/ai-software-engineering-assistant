# Validates incoming/outgoing data - contracts
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=30
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=64
    )