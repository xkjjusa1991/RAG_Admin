from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class KnowledgeSchema(BaseModel):
    id: Optional[int]
    filename: Optional[str]
    slice_number: Optional[str]
    slice_content: Optional[str]
    embedding: Optional[Any]
    upload_user: Optional[str]
    upload_time: Optional[datetime]
    text_head_hash: Optional[str]
    text_end_hash: Optional[str]
    scope: Optional[Any]
    file_id: Optional[int]
    file_summary: Optional[str]
    file_info: Optional[Any]
    source_type: Optional[str]
    file_content: Optional[str]
    kb_id: Optional[str]

    model_config = {"from_attributes": True}

class KnowledgeCreateSchema(BaseModel):
    filename: Optional[str]
    slice_number: Optional[str]
    slice_content: Optional[str]
    embedding: Optional[Any]
    upload_user: Optional[str]
    upload_time: Optional[datetime]
    text_head_hash: Optional[str]
    text_end_hash: Optional[str]
    scope: Optional[Any]
    file_id: Optional[int]
    file_summary: Optional[str]
    file_info: Optional[Any]
    source_type: Optional[str]
    file_content: Optional[str]
    kb_id: Optional[str] 