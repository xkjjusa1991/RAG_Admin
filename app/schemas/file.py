from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FileSchema(BaseModel):
    id: Optional[int]
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

    class Config:
        from_attributes = True 