'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-03-06 16:48:51
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-06 17:22:32
FilePath: \RAG_Admin\app\schemas\knowledge_base.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class KnowledgeBaseSchema(BaseModel):
    id: Optional[int]
    filename: Optional[str]
    slice_number: Optional[str]
    slice_content: Optional[str]
    embedding: Optional[List[float]]
    upload_user: Optional[str]
    upload_time: Optional[str]  # 可以根据需要更改为 datetime
    text_head_hash: Optional[str]
    text_end_hash: Optional[str]
    scope: Optional[List[str]]
    file_id: Optional[int]
    file_summary: Optional[str]
    file_info: Optional[dict]
    source_type: Optional[str]
    file_content: Optional[str]

    class Config:
        orm_mode = True  # 确保使用 orm_mode

class KnowledgeBaseCreateSchema(BaseModel):
    filename: str
    slice_number: Optional[str] = None
    slice_content: str
    embedding: Optional[List[float]] = []
    upload_user: Optional[str] = None
    upload_time: Optional[datetime] = datetime.now()  # 使用当前时间
    text_head_hash: Optional[str] = None
    text_end_hash: Optional[str] = None
    scope: Optional[List[str]] = []
    file_id: int
    file_summary: Optional[str] = None
    file_info: Optional[dict] = {}
    source_type: Optional[str] = None
    file_content: Optional[str] = None

    class Config:
        orm_mode = True  # 确保使用 orm_mode

class KnowledgeBaseAISchema(BaseModel):
    id: int  # 主键

    class Config:
        from_attributes = True  # 允许模型直接从ORM对象实例化 