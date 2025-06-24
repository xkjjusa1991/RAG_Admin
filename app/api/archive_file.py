'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-06-20 13:37:34
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-06-24 12:51:07
FilePath: \RAG_Admin\app\api\archive_file.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.archive_file import ArchiveFileSchema, ImportToDocumentsRequest
from app.crud.crud_archive_file import crud_archive_file
from app.core.database import get_db
from app.schemas.response import ResponseBase, PageResponse, PageInfo
from typing import List
from app.models.archive_file import ArchiveFile
from app.models.document import Document
from sqlalchemy import select
from app.models.archive_record import ArchiveRecord
from datetime import datetime
import uuid
from app.services.archive_file_service import import_to_documents_service
from pydantic import BaseModel

router = APIRouter()

@router.get("/", response_model=PageResponse[List[ArchiveFileSchema]], summary="获取归档文件列表")
async def list_files(
    page: int = Query(1, ge=1, description="页码，从1开始"),
    limit: int = Query(20, ge=1, description="每页数量"),
    db: AsyncSession = Depends(get_db)
):
    """分页获取归档文件列表"""
    skip = (page - 1) * limit
    orm_files = await crud_archive_file.get_multi(db, skip=skip, limit=limit)
    files = [ArchiveFileSchema.model_validate(item) for item in orm_files]
    total = await crud_archive_file.count(db) if hasattr(crud_archive_file, 'count') else len(files)
    page_info = PageInfo(total=total, page=page, size=limit)
    return PageResponse[List[ArchiveFileSchema]](data=files, page_info=page_info)

@router.get("/{efile_id}", response_model=ResponseBase[ArchiveFileSchema], summary="获取归档文件详情")
async def get_file(efile_id: int, db: AsyncSession = Depends(get_db)):
    """根据efile_id获取归档文件详情"""
    file = await crud_archive_file.get(db, efile_id)
    if not file:
        return ResponseBase(code=404, msg="File not found")
    return ResponseBase(data=file)

@router.post("/import_to_documents", summary="批量导入未同步的归档文件到documents表")
async def import_to_documents(
    body: ImportToDocumentsRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await import_to_documents_service(db, last_update_time=body.last_update_time, efile_ids=body.efile_ids)
    return ResponseBase(msg="导入完成", data=result) 