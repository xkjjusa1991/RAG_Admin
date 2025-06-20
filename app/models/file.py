'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-06-18 14:23:00
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-06-18 15:32:39
FilePath: \RAG_Admin\app\models\file.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, JSON, Text, Enum
from app.models.base import Base

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_name = Column(String(255), nullable=False)
    upload_time = Column(DateTime, nullable=False)
    file_size = Column(BigInteger, nullable=False)
    content_type = Column(String(100), nullable=False)
    user_id = Column(String(36), nullable=False)
    file_metadata = Column("metadata", JSON)
    file_path = Column(String(255), nullable=False)
    ocr_text = Column(Text)
    ocr_status = Column(Enum("pending", "processing", "completed", "failed", name="ocr_status_enum"), default="pending")
    ocr_time = Column(DateTime)
    ocr_engine = Column(String(50))
    ocr_language = Column(String(10)) 