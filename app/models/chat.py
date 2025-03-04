'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-03-04 12:23:59
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-04 12:25:38
FilePath: \RAG_Admin\app\models\chat.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from app.core.database import Base

class Chat(Base):
    """聊天记录数据模型"""
    __tablename__ = "chats"

    chat_id = Column(String(36), primary_key=True, comment="聊天记录ID")
    user_id = Column(String(36), comment="用户ID")
    session_id = Column(String(36), comment="会话ID")
    question = Column(Text, comment="用户提问")
    answer = Column(Text, comment="算法端返回的答案")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间") 