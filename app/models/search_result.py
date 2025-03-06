from sqlalchemy import Column, BigInteger, String, Float, JSON
from app.core.database import Base
from typing import Optional

class SearchResult(Base):
    __tablename__ = "search_results"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键, 自增')
    request_id = Column(BigInteger, nullable=False, comment='关联 search_requests 表的 id')
    efile_id = Column(BigInteger, nullable=True, comment='关联 v_ai_arichive_efile 表的 EFILE_ID')
    nd = Column(String(50), nullable=True, comment='年度')
    ztm = Column(String(2000), nullable=True, comment='题名')
    table_cname1 = Column(String(50), nullable=True, comment='档案分类名（一级）')
    table_cname2 = Column(String(50), nullable=True, comment='档案分类名（二级）')
    label = Column(String(500), nullable=False, comment='文件名称')
    relevance_score = Column(Float, default=0, comment='相关性评分')
    clicks = Column(BigInteger, default=0, comment='点击次数')
    relevant_chunks = Column(JSON, nullable=True, comment='相关切块详情')
    temp_id = Column(String(100), nullable=True, comment='redis同步id')

    class Config:
        orm_mode = True  # 允许从 ORM 模型转换 