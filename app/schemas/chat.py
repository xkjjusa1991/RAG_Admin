'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-03-04 12:24:00
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-05 15:40:19
FilePath: \RAG_Admin\app\schemas\chat.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
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