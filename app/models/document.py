'''
Author: 自动生成
Description: Document表ORM模型  
'''
from sqlalchemy import Column, BigInteger, String, Enum, Text, JSON, DateTime, Integer
from app.models.base import Base
import enum

class SourceEnum(enum.Enum):
    archive = 'archive'
    upload = 'upload'

class StatusEnum(enum.Enum):
    # 这里可根据实际业务补充状态
    pending = 'pending'
    processed = 'processed'


class Document(Base):
    __tablename__ = 'documents'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='自增主键')
    document_id = Column(String(255), nullable=False, comment='文档唯一标识')
    file_id = Column(BigInteger, comment='关联文件ID')
    source = Column(Enum(SourceEnum), comment='来源类型 (archive: 转案车, upload: 直接上传)')
    status = Column(Enum(StatusEnum), default=StatusEnum.pending, comment='向量状态')
    summary = Column(Text, comment='文档摘要')
    tags = Column(JSON, comment='标签列表 (JSON数组)')
    upload_user = Column(String(40), comment='上传用户')
    upload_time = Column(DateTime, comment='上传时间')
    process_time = Column(DateTime, comment='最后一次处理时间')
    kb_id = Column(String(255), comment='知识库ID')
    version = Column(Integer, default=1, comment='版本号') 