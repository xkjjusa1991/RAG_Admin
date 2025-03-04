from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

class ChatBase(BaseModel):
    question: str
    answer: str

class ChatCreate(ChatBase):
    session_id: str

class ChatResponse(ChatBase):
    chat_id: str
    user_id: str
    created_at: datetime

class ChatRequest(BaseModel):
    query: str
    question_id: Optional[str] = Field(None, description="The ID of the question.")
    session_id: Optional[str] = Field(None, description="The ID of the session.")
    stream: Optional[bool] = False
    history: Optional[List] = []
    temperature: Optional[float] = 0.7
    max_new_tokens: Optional[int] = 1200 