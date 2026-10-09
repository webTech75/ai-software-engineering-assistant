"""
===============================================================================
File: main.py
Path: app/main.py

Description:
    Application entry point for the AI Software Engineering Assistant.

Responsibilities:
    - Create the FastAPI application.
    - Configure middleware.
    - Register API routers.
    - Configure application startup.
    - Expose API documentation.

Notes:
    - This module is executed when the application starts.
    - Uvicorn uses the `app` instance defined here.
    - All API routes are registered through this file.

Author:
    Amr Elhabbal
===============================================================================
"""
from fastapi import FastAPI

from app.api.v1.users import router as users_router
from app.core.config import settings
# import the User model to ensure it is registered with SQLAlchemy
from app.models.user import User
from app.api.v1.projects import router as projects_router
from app.api.v1.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.models.project import Project
from app.models.chat_message import ChatMessage

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.app_name}"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }