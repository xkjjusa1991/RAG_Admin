'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-03-04 16:25:24
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-04 22:24:00
FilePath: \\RAG_Admin\\app\\schemas\\user_logs.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from pydantic import BaseModel
from typing import Optional, Dict, Any, Union, List
from datetime import datetime

class UserLogsCreate(BaseModel):
    session_id: str
    user_id: str
    query: Optional[str] = None
    answer: Optional[str] = None
    response_segment: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None
    score: Optional[float] = None
    prompt: Optional[str] = None
    like: Optional[int] = None
    question_time: Optional[datetime] = None
    dislike_suggestion: Optional[str] = None

class UserLogs(BaseModel):
    question_id: int
    session_id: str
    user_id: str
    query: Optional[str] = None
    answer: Optional[str] = None
    response_segment: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None
    score: Optional[float] = None
    prompt: Optional[str] = None
    like: Optional[int] = None
    question_time: Optional[datetime] = None
    dislike_suggestion: Optional[str] = None

    class Config:
        orm_mode = True 