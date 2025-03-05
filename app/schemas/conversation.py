'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-03-04 22:30:00
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-04 22:30:00
FilePath: \\RAG_Admin\\app\\schemas\\conversation.py
Description: 对话内容模型
'''
from pydantic import BaseModel

class Conversation(BaseModel):
    question_id: str
    role: str  # 使用 role 来代替 from_
    content: str
    timestamp: int 