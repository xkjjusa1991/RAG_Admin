'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-06-18 14:23:06
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-06-24 20:40:44
FilePath: \RAG_Admin\app\api\file.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import APIRouter, File as FastAPIFile, UploadFile, Depends, Query, Path
from fastapi.responses import JSONResponse
from datetime import datetime
import os
import shutil
from app.core.database import get_db
from sqlalchemy.orm import Session
import uuid
from app.models.file import File as FileModel
from app.services.file import save_upload_file, get_file_list, get_file_detail, delete_file
from fastapi.encoders import jsonable_encoder
from app.schemas.response import ResponseBase, PageResponse, PageInfo
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.file import FileSchema, ImportToDocumentsRequest
from app.services.file_service import import_to_documents_service
import math
from typing import List
from app.crud.crud_file import crud_file

router = APIRouter()


@router.post("/upload", response_model=ResponseBase, summary="上传文件", description="上传单个文件到服务器，并保存文件信息到数据库。")
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_file = await save_upload_file(file, current_user.user_id, db)
    return ResponseBase(msg="上传成功", data=FileSchema.model_validate(db_file))

@router.get("/list", response_model=PageResponse[List[FileSchema]], summary="获取文件列表（分页）", description="分页获取所有文件的信息。")
async def file_list(
    page: int = Query(1, ge=1, description="页码，从1开始"),
    limit: int = Query(20, ge=1, description="每页数量"),
    db: Session = Depends(get_db)
):
    skip = limit * (page - 1)
    files = await crud_file.get_multi(db, skip=skip, limit=limit)
    total = await crud_file.count(db)
    total_pages = math.ceil(total / limit) if limit else 1
    count = len(files)
    page_info = PageInfo(total_pages=total_pages, page=page, size=limit, count=count)
    return PageResponse[List[FileSchema]](data=[FileSchema.model_validate(f) for f in files], page_info=page_info)

@router.get("/detail/{file_id}", response_model=ResponseBase, summary="获取文件详情", description="根据文件ID获取单个文件的详细信息，仅限文件所有者访问。")
async def file_detail(file_id: int = Path(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    file = await crud_file.get(db, file_id)
    if not file or file.user_id != current_user.user_id:
        return ResponseBase(code=404, msg="文件不存在")
    return ResponseBase(data=FileSchema.model_validate(file))

@router.delete("/delete/{file_id}", response_model=ResponseBase, summary="删除文件", description="根据文件ID删除指定文件，仅限文件所有者操作。")
async def file_delete(file_id: int = Path(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    file = await get_file_detail(db, file_id)
    if not file or file.user_id != current_user.user_id:
        return ResponseBase(code=404, msg="文件不存在")
    await delete_file(db, file_id)
    return ResponseBase(msg="删除成功")

@router.post("/import_to_documents", response_model=ResponseBase, summary="批量导入文件到documents表", description="将指定的文件批量导入到documents表中。")
async def import_to_documents(
    body: ImportToDocumentsRequest,
    db: Session = Depends(get_db)
):
    result = await import_to_documents_service(db, kb_id=body.kb_id, last_update_time=body.last_update_time, file_ids=body.file_ids)
    return ResponseBase(msg="导入完成", data=result) 