'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-06-18 14:24:22
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-06-24 16:37:27
FilePath: \RAG_Admin\app\services\file.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os
import shutil
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.file import File as FileModel
from sqlalchemy import select, func
from app.core.config import settings
from app.crud.crud_file import crud_file
from app.schemas.file import FileCreateSchema


async def get_file_list(db, skip: int = 0, limit: int = 20):
    stmt = select(FileModel).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_file_detail(db, file_id: int):
    stmt = select(FileModel).where(FileModel.id == file_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def delete_file(db, file_id: int):
    file_obj = await get_file_detail(db, file_id)
    if file_obj:
        await db.delete(file_obj)
        await db.commit()
    return file_obj

async def save_upload_file(file, user_id: str, db: AsyncSession):
    os.makedirs(settings.FILE_ROOT_PATH, exist_ok=True)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(settings.FILE_ROOT_PATH, file_id + "_" + file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_info = {
        "file_name": file.filename,
        "upload_time": datetime.now(),
        "file_size": os.path.getsize(file_path),
        "content_type": file.content_type,
        "user_id": user_id,
        "file_metadata": None,
        "file_path": file_path,
        "ocr_text": None,
        "ocr_status": "pending",
        "ocr_time": None,
        "ocr_engine": None,
        "ocr_language": None,
    }

    file_to_create = FileCreateSchema(**file_info)
    db_file = await crud_file.create(db, obj_in=file_to_create)
    return db_file
