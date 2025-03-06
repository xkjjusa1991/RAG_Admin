from sqlalchemy import Column, String, Text, DateTime, BigInteger, Float, JSON
from app.core.database import Base
from datetime import datetime

class SearchRequest(Base):
    __tablename__ = "search_requests"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='自增主键')
    user_id = Column(String(36), nullable=False, comment='用户id')
    query_text = Column(Text, nullable=False, comment='搜索内容')
    search_time = Column(DateTime, default=datetime.now, comment='搜索时间')
    result_count = Column(BigInteger, default=0, comment='结果数量')
    is_satisfied = Column(BigInteger, default=0, comment='用户是否对搜索结果满意（0: 不满意, 1: 满意）')
    query_duration = Column(Float, default=0, comment='查询的耗时（秒）')
    ip_address = Column(String(45), nullable=True, comment='用户的IP地址，用于分析地理位置信息。')
    user_agent = Column(Text, nullable=True, comment='用户的浏览器和操作系统信息。')
    source = Column(String(255), default='web', comment='搜索来源，例如"网页"、"API"等。')
    search_conditions = Column(JSON, nullable=True, comment='存储搜索条件的JSON格式数据。') 