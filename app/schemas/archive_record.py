from pydantic import BaseModel
from typing import Optional
from datetime import date

class ArchiveRecordBase(BaseModel):
    nd: Optional[str]
    dh: Optional[str]
    ztm: Optional[str]
    wh: Optional[str]
    zrz: Optional[str]
    bgqx: Optional[str]
    mj: Optional[str]
    gddw: Optional[str]
    gdsj: Optional[date]
    lrsj: Optional[date]
    sry: Optional[str]
    table_cname1: Optional[str]
    table_cname2: Optional[str]
    kb_id: Optional[str]

class ArchiveRecordCreate(ArchiveRecordBase):
    pass

class ArchiveRecordUpdate(ArchiveRecordBase):
    pass

class ArchiveRecordInDBBase(ArchiveRecordBase):
    record_id: int
    class Config:
        orm_mode = True

class ArchiveRecord(ArchiveRecordInDBBase):
    pass 