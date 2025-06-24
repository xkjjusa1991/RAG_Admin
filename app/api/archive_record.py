'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-06-20 13:37:20
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-06-24 13:01:41
FilePath: \\RAG_Admin\\app\\api\\archive_record.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.archive_record import ArchiveRecord
from app.schemas.archive_file import ArchiveFileSchema
from app.crud.crud_archive_record import crud_archive_record
from app.core.database import get_db
from app.schemas.response import ResponseBase, PageResponse, PageInfo
from typing import List

router = APIRouter()

@router.get("/", response_model=PageResponse[List[ArchiveRecord]], summary="获取归档记录列表")
async def list_records(
    page: int = Query(1, ge=1, description="页码，从1开始"),
    limit: int = Query(20, ge=1, description="每页数量"),
    db: AsyncSession = Depends(get_db)
):
    """分页获取归档记录列表"""
    skip = (page - 1) * limit
    orm_records = await crud_archive_record.get_multi(db, skip=skip, limit=limit)
    records = [ArchiveRecord.model_validate(item) for item in orm_records]
    total = await crud_archive_record.count(db) if hasattr(crud_archive_record, 'count') else len(records)
    page_info = PageInfo(total=total, page=page, size=limit)
    return PageResponse[List[ArchiveRecord]](data=records, page_info=page_info)

@router.get("/{record_id}", response_model=ResponseBase[ArchiveRecord], summary="获取归档记录详情")
async def get_record(record_id: int, db: AsyncSession = Depends(get_db)):
    """根据record_id获取归档记录详情"""
    rec = await crud_archive_record.get(db, record_id)
    if not rec:
        return ResponseBase(code=404, msg="Record not found")
    return ResponseBase(data=rec)

@router.get("/{record_id}/files", response_model=ResponseBase[List[ArchiveFileSchema]], summary="获取归档记录下所有文件")
async def get_files_by_record_id(record_id: int, db: AsyncSession = Depends(get_db)):
    """根据record_id获取该记录下所有归档文件"""
    files = await crud_archive_record.get_files_by_record_id(db, record_id)
    return ResponseBase(data=files) 