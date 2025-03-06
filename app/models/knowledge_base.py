from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class KnowledgeBase(Base):
    __tablename__ = 'knowledge_base'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增id')
    filename = Column(String(255), comment='文件名')
    slice_number = Column(String(255), comment='切片编号')
    slice_content = Column(Text, comment='切片内容')
    embedding = Column(JSON, comment='向量化数组')
    upload_user = Column(String(40), comment='上传用户')
    upload_time = Column(DateTime, comment='上传时间')
    text_head_hash = Column(Text, comment='文本头部哈希')
    text_end_hash = Column(Text, comment='文本尾部哈希')
    scope = Column(JSON, comment='权限（list）')
    file_id = Column(Integer, comment='文档id')
    file_summary = Column(Text, comment='摘要')
    file_info = Column(JSON, comment='文档元数据')
    source_type = Column(String(15), comment='文档来源类型（files, news）')
    file_content = Column(Text, comment='文档内容') 