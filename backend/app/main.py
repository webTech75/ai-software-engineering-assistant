from fastapi import FastAPI

from app.api.v1.users import router as users_router
from app.core.config import settings
# import the User model to ensure it is registered with SQLAlchemy
from app.models.user import User
from app.api.v1.projects import router as projects_router

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)

app.include_router(users_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1")

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