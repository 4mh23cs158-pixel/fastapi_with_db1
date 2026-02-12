from pydantic import BaseModel

from datetime import datetime
from typing import List, Optional

class AIRequest(BaseModel):
    message: str
    system_prompt: str = "You are a helpful assistant."
    session_id: Optional[str] = None

class AIResponse(BaseModel):
    response: str
    session_id: Optional[str] = None

class ChatMessageSchema(BaseModel):
    role: str
    content: str
    timestamp: datetime
    session_id: str

    class Config:
        from_attributes = True

class SessionSchema(BaseModel):
    session_id: str
    title: str
    last_message_at: datetime

class ChatHistoryResponse(BaseModel):
    history: List[ChatMessageSchema]

class SessionListResponse(BaseModel):
    sessions: List[SessionSchema]