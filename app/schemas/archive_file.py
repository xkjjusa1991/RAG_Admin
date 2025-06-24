'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-06-20 13:36:12
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-06-20 13:55:38
FilePath: \RAG_Admin\app\schemas\archive_file.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ArchiveFileBaseSchema(BaseModel):
    record_id: Optional[int]
    label: Optional[str]
    file_type: Optional[str]
    order_num: Optional[int]
    content: Optional[str]
    last_update_time: Optional[datetime]

    model_config = {"from_attributes": True}

class ArchiveFileCreateSchema(ArchiveFileBaseSchema):
    pass

class ArchiveFileUpdateSchema(ArchiveFileBaseSchema):
    pass

class ArchiveFileInDBBaseSchema(ArchiveFileBaseSchema):
    efile_id: int

class ArchiveFileSchema(ArchiveFileInDBBaseSchema):
    pass

class ImportToDocumentsRequest(BaseModel):
    last_update_time: Optional[datetime] = None
    efile_ids: Optional[List[int]] = None 