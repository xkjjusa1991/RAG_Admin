from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey
from app.core.database import Base

class Session(Base):
    """会话数据模型"""
    __tablename__ = "sessions"

    session_id = Column(String(36), primary_key=True, comment="会话ID")
    user_id = Column(String(36), ForeignKey("users.user_id"), nullable=False, comment="用户ID")
    session_name = Column(String(255), nullable=False, comment="会话名称")
    start_time = Column(DateTime, nullable=False, default=datetime.now, comment="会话开始时间")
    last_update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="最后更新时间")
    end_time = Column(DateTime, nullable=True, comment="会话结束时间")
    context = Column(Text, nullable=True, comment="会话上下文")
    session_type = Column(Integer, default=0, comment="会话类型(档案：1、个人：2、其他：0)")
    session_status = Column(Integer, default=1, comment="会话状态（活跃：1、非活跃：2、其他：0）") 