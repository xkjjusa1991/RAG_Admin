'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-06-20 12:09:43
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-06-24 20:44:06
FilePath: \RAG_Admin\app\api\document.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
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
import math

router = APIRouter()

@router.get("/", response_model=PageResponse[List[Document]], summary="获取文档列表（分页）", description="分页获取所有文档的信息。")
async def list_documents(page: int = 1, limit: int = 20, db: AsyncSession = Depends(get_db)):
    offset = (page - 1) * limit
    orm_items = await crud_document.get_multi(db, skip=offset, limit=limit)
    items = [Document.model_validate(item) for item in orm_items]
    total = await crud_document.count(db) if hasattr(crud_document, 'count') else len(items)
    total_pages = math.ceil(total / limit) if limit else 1
    count = len(items)
    page_info = PageInfo(total_pages=total_pages, page=page, size=limit, count=count)
    return PageResponse[List[Document]](data=items, page_info=page_info)

@router.get("/{id}", response_model=Document, summary="获取文档详情", description="根据文档ID获取单个文档的详细信息。")
async def get_document(id: int, db: AsyncSession = Depends(get_db)):
    doc = await crud_document.get(db, id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.post("/", response_model=Document, summary="创建新文档", description="创建一个新的文档。")
async def create_document(document: DocumentCreate, db: AsyncSession = Depends(get_db)):
    return await crud_document.create(db, document)

@router.put("/{id}", response_model=Document, summary="更新文档", description="根据文档ID更新指定文档的信息。")
async def update_document(id: int, document: DocumentUpdate, db: AsyncSession = Depends(get_db)):
    db_obj = await crud_document.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Document not found")
    return await crud_document.update(db, db_obj, document)

@router.delete("/{id}", response_model=Document, summary="删除文档", description="根据文档ID删除指定文档。")
async def delete_document(id: int, db: AsyncSession = Depends(get_db)):
    doc = await crud_document.remove(db, id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc 