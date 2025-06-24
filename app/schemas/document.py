from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime

class DocumentBase(BaseModel):
    document_id: str
    file_id: Optional[int] = None
    source: Optional[str] = None
    status: Optional[str] = None
    summary: Optional[str] = None
    tags: Optional[Any] = None
    upload_user: Optional[str] = None
    upload_time: Optional[datetime] = None
    process_time: Optional[datetime] = None
    kb_id: Optional[str] = None
    version: Optional[int] = 1

    model_config = {"from_attributes": True}

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(DocumentBase):
    pass

class DocumentInDBBase(DocumentBase):
    id: int

class Document(DocumentInDBBase):
    pass

class DocumentList(BaseModel):
    total: int
    items: List[Document] 