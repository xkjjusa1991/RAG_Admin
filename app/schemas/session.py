from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.base import BaseSchema

class SessionBase(BaseSchema):
    session_name: str
    session_type: Optional[int] = 0
    context: Optional[str] = None

class SessionCreate(SessionBase):
    pass

class SessionUpdate(BaseSchema):
    session_name: Optional[str] = None
    context: Optional[str] = None
    session_type: Optional[int] = None
    session_status: Optional[int] = None
    end_time: Optional[datetime] = None

class SessionResponse(SessionBase):
    session_id: str
    user_id: str
    start_time: datetime
    last_update_time: datetime
    end_time: Optional[datetime] = None
    session_status: int

class SessionRename(BaseSchema):
    """仅用于重命名会话的 Schema"""
    session_name: str 