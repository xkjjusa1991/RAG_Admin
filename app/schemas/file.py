from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FileBaseSchema(BaseModel):
    file_name: str
    upload_time: datetime
    file_size: int
    content_type: str
    user_id: str
    file_metadata: Optional[dict]
    file_path: str
    ocr_text: Optional[str]
    ocr_status: Optional[str]
    ocr_time: Optional[datetime]
    ocr_engine: Optional[str]
    ocr_language: Optional[str]

class FileCreateSchema(FileBaseSchema):
    pass

class FileSchema(FileBaseSchema):
    id: int
    class Config:
        from_attributes = True

class ImportToDocumentsRequest(BaseModel):
    kb_id: str
    last_update_time: Optional[datetime] = None
    file_ids: Optional[List[int]] = None 