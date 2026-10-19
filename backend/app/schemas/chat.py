from datetime import datetime

from pydantic import BaseModel



class ChatRequest(BaseModel):
    """
    Incoming chat request.

    project_id is optional.

    None:
        General Neura conversation.

    Value:
        Project-aware conversation.
    """

    message: str
    project_id: int | None = None



class ChatResponse(BaseModel):
    answer: str



class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime


    class Config:
        from_attributes = True