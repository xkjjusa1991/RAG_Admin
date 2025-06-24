from sqlalchemy import Column, String, Text, DateTime, SmallInteger
from app.models.base import Base

class KnowledgeBase(Base):
    __tablename__ = 'knowledge_base'

    kb_id = Column(String(36), primary_key=True, comment='UUID主键')
    kb_name = Column(String(255), nullable=False, comment='知识库名称')
    name = Column(String(255), nullable=False, comment='知识库标识符')
    description = Column(Text, comment='知识库描述')
    user_id = Column(String(36), nullable=False, comment='创建者ID')
    status = Column(SmallInteger, default=1, comment='状态：1-正常，0-禁用')
    is_public = Column(SmallInteger, default=0, comment='是否公开：1-公开，0-私有')
    created_at = Column(DateTime, comment='创建时间')
    updated_at = Column(DateTime, comment='更新时间') 