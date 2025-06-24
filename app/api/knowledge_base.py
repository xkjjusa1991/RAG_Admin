'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-06-24 16:07:35
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-06-24 16:17:30
FilePath: \RAG_Admin\app\api\knowledge_base.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.knowledge_base import KnowledgeBaseSchema, KnowledgeBaseCreateSchema, KnowledgeBaseUpdateSchema
from app.crud.crud_knowledge_base import crud_knowledge_base
from app.schemas.response import ResponseBase, PageResponse, PageInfo
from typing import List
import math

router = APIRouter()

@router.get("/", response_model=PageResponse[List[KnowledgeBaseSchema]])
async def list_knowledge_bases(page: int = 1, limit: int = 100, db: AsyncSession = Depends(get_db)):
    offset = (page - 1) * limit
    items = await crud_knowledge_base.get_multi(db, skip=offset, limit=limit)
    total = await crud_knowledge_base.count(db) if hasattr(crud_knowledge_base, 'count') else len(items)
    data = [KnowledgeBaseSchema.model_validate(item) for item in items]
    total_pages = math.ceil(total / limit) if limit else 1
    count = len(items)
    page_info = PageInfo(total_pages=total_pages, page=page, size=limit, count=count)
    return PageResponse[List[KnowledgeBaseSchema]](data=data, page_info=page_info)

@router.get("/{kb_id}", response_model=ResponseBase[KnowledgeBaseSchema])
async def get_knowledge_base(kb_id: str, db: AsyncSession = Depends(get_db)):
    obj = await crud_knowledge_base.get(db, kb_id)
    if not obj:
        raise HTTPException(status_code=404, detail="KnowledgeBase not found")
    return ResponseBase[KnowledgeBaseSchema](data=KnowledgeBaseSchema.model_validate(obj))

@router.post("/", response_model=ResponseBase[KnowledgeBaseSchema])
async def create_knowledge_base(data: KnowledgeBaseCreateSchema, db: AsyncSession = Depends(get_db)):
    obj = await crud_knowledge_base.create(db, data)
    return ResponseBase[KnowledgeBaseSchema](data=KnowledgeBaseSchema.model_validate(obj))

@router.put("/{kb_id}", response_model=ResponseBase[KnowledgeBaseSchema])
async def update_knowledge_base(kb_id: str, data: KnowledgeBaseUpdateSchema, db: AsyncSession = Depends(get_db)):
    obj = await crud_knowledge_base.update(db, kb_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="KnowledgeBase not found")
    return ResponseBase[KnowledgeBaseSchema](data=KnowledgeBaseSchema.model_validate(obj))

@router.delete("/{kb_id}", response_model=ResponseBase[KnowledgeBaseSchema])
async def delete_knowledge_base(kb_id: str, db: AsyncSession = Depends(get_db)):
    obj = await crud_knowledge_base.remove(db, kb_id)
    if not obj:
        raise HTTPException(status_code=404, detail="KnowledgeBase not found")
    return ResponseBase[KnowledgeBaseSchema](data=KnowledgeBaseSchema.model_validate(obj)) 