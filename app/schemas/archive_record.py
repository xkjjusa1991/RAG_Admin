'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-06-20 13:36:28
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-06-24 13:00:04
FilePath: \RAG_Admin\app\schemas\archive_record.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
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

    model_config = {"from_attributes": True}

class ArchiveRecordCreate(ArchiveRecordBase):
    pass

class ArchiveRecordUpdate(ArchiveRecordBase):
    pass

class ArchiveRecordInDBBase(ArchiveRecordBase):
    record_id: int

class ArchiveRecord(ArchiveRecordInDBBase):
    pass 