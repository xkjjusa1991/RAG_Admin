from sqlalchemy import Column, BigInteger, String, Text, JSON, DECIMAL, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserLogs(Base):
    __tablename__ = 'user_logs'

    question_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='问题id')
    session_id = Column(String(36), nullable=False, comment='会话id')
    user_id = Column(String(40), nullable=False, comment='用户id')
    query = Column(Text, comment='问题内容')
    answer = Column(Text, comment='回答')
    response_segment = Column(JSON, comment='响应片段')
    score = Column(DECIMAL(40, 0), default=None, comment='分数')
    prompt = Column(Text, comment='回答片段及得分')
    like = Column(Integer, default=None, comment='点赞：1、点踩：2、无操作：0')
    question_time = Column(DateTime, default=None, comment='提问时间')
    dislike_suggestion = Column(String(255), default=None, comment='点踩建议') 