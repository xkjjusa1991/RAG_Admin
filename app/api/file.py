'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-06-18 14:23:06
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-06-20 16:32:43
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
from app.schemas.response import ResponseBase
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.file import FileSchema, ImportToDocumentsRequest
from app.services.file_service import import_to_documents_service

router = APIRouter()


@router.post("/upload", response_model=ResponseBase)
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_file = await save_upload_file(file, current_user.user_id, db)
    return ResponseBase(msg="上传成功", data=FileSchema.model_validate(db_file))

@router.get("/list", response_model=ResponseBase)
async def file_list(
    page: int = Query(1, ge=1, description="页码，从1开始"),
    limit: int = Query(20, ge=1, description="每页数量"),
    db: Session = Depends(get_db)
):
    skip = limit * (page - 1)
    files = await get_file_list(db, skip=skip, limit=limit)
    return ResponseBase(data=[FileSchema.model_validate(f) for f in files])

@router.get("/detail/{file_id}", response_model=ResponseBase)
async def file_detail(file_id: int = Path(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    file = await get_file_detail(db, file_id)
    if not file or file.user_id != current_user.user_id:
        return ResponseBase(code=404, msg="文件不存在")
    return ResponseBase(data=FileSchema.model_validate(file))

@router.delete("/delete/{file_id}", response_model=ResponseBase)
async def file_delete(file_id: int = Path(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    file = await get_file_detail(db, file_id)
    if not file or file.user_id != current_user.user_id:
        return ResponseBase(code=404, msg="文件不存在")
    await delete_file(db, file_id)
    return ResponseBase(msg="删除成功")

@router.post("/import_to_documents", response_model=ResponseBase, summary="批量导入file到documents表")
async def import_to_documents(
    body: ImportToDocumentsRequest,
    db: Session = Depends(get_db)
):
    result = await import_to_documents_service(db, kb_id=body.kb_id, last_update_time=body.last_update_time, file_ids=body.file_ids)
    return ResponseBase(msg="导入完成", data=result) 