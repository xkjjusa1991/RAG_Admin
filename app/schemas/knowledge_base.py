from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class KnowledgeBaseSchema(BaseModel):
    kb_id: str
    kb_name: str
    name: str
    description: Optional[str]
    user_id: str
    status: int
    is_public: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}

class KnowledgeBaseCreateSchema(BaseModel):
    kb_id: str
    kb_name: str
    name: str
    description: Optional[str] = None
    user_id: str
    status: int = 1
    is_public: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class KnowledgeBaseUpdateSchema(BaseModel):
    kb_name: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None
    is_public: Optional[int] = None
    updated_at: Optional[datetime] = None 