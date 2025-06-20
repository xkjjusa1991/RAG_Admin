from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class DocumentBase(BaseModel):
    document_id: str
    file_id: Optional[int]
    source: Optional[str]
    status: Optional[str]
    summary: Optional[str]
    tags: Optional[Any]
    upload_user: Optional[str]
    upload_time: Optional[datetime]
    process_time: Optional[datetime]
    kb_id: Optional[str]
    version: Optional[int]

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(DocumentBase):
    pass

class DocumentInDBBase(DocumentBase):
    id: int
    class Config:
        orm_mode = True

class Document(DocumentInDBBase):
    pass

class DocumentList(BaseModel):
    total: int
    items: List[Document] 