'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-06-20 12:09:43
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-06-24 12:49:43
FilePath: \RAG_Admin\app\api\document.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.document import Document, DocumentCreate, DocumentUpdate, DocumentList
from app.crud.crud_document import crud_document
from app.core.database import get_db
from typing import List
from app.schemas.response import PageResponse, PageInfo

router = APIRouter()

@router.get("/", response_model=PageResponse[List[Document]])
async def list_documents(page: int = 1, limit: int = 20, db: AsyncSession = Depends(get_db)):
    offset = (page - 1) * limit
    orm_items = await crud_document.get_multi(db, skip=offset, limit=limit)
    items = [Document.model_validate(item) for item in orm_items]
    total = await crud_document.count(db) if hasattr(crud_document, 'count') else len(items)
    page_info = PageInfo(total=total, page=page, size=limit)
    return PageResponse[List[Document]](data=items, page_info=page_info)

@router.get("/{id}", response_model=Document)
async def get_document(id: int, db: AsyncSession = Depends(get_db)):
    doc = await crud_document.get(db, id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.post("/", response_model=Document)
async def create_document(document: DocumentCreate, db: AsyncSession = Depends(get_db)):
    return await crud_document.create(db, document)

@router.put("/{id}", response_model=Document)
async def update_document(id: int, document: DocumentUpdate, db: AsyncSession = Depends(get_db)):
    db_obj = await crud_document.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Document not found")
    return await crud_document.update(db, db_obj, document)

@router.delete("/{id}", response_model=Document)
async def delete_document(id: int, db: AsyncSession = Depends(get_db)):
    doc = await crud_document.remove(db, id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc 