from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from app.models.base import Base

class Knowledge(Base):
    __tablename__ = 'knowledge'

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255))
    slice_number = Column(String(255))
    slice_content = Column(Text)
    embedding = Column(JSON)
    upload_user = Column(String(40))
    upload_time = Column(DateTime)
    text_head_hash = Column(Text)
    text_end_hash = Column(Text)
    scope = Column(JSON)
    file_id = Column(Integer)
    file_summary = Column(Text)
    file_info = Column(JSON)
    source_type = Column(String(15))
    file_content = Column(Text)
    kb_id = Column(String(255)) 