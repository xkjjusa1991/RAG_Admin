'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-02-18 11:22:04
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-05 01:24:42
FilePath: \RAG_Admin\app\schemas\session.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.base import BaseSchema
from app.schemas.conversation import Conversation
from typing import List
from pydantic import Field

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

class SessionData(BaseModel):
    session_id: str
    user_id: str

    scope: List[str]
    data: List[Conversation]
    status_code: int = Field(200, ge=200, le=599)    