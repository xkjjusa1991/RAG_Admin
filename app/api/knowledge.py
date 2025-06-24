'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-06-24 13:29:59
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-06-24 20:46:44
FilePath: \RAG_Admin\app\api\knowledge.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.knowledge import KnowledgeSchema, KnowledgeCreateSchema
from app.crud.crud_knowledge import crud_knowledge
from app.schemas.response import ResponseBase
from typing import List

router = APIRouter()

@router.get("/by_file/{file_id}", response_model=ResponseBase[List[KnowledgeSchema]], summary="根据文件ID获取知识列表", description="根据 file_id 获取该文件下所有知识分片，并按分段序号升序排序。")
async def get_by_file_id(file_id: int, db: AsyncSession = Depends(get_db)):
    items = await crud_knowledge.get_by_file_id(db, file_id)
    data = [KnowledgeSchema.model_validate(item) for item in items]
    # 按 file_info['id'] 的分段序号升序排序
    def get_sort_key(x):
        try:
            id_str = x.file_info.get('id', '')
            return int(id_str.split('_')[1]) if '_' in id_str else 0
        except Exception:
            return 0
    data.sort(key=get_sort_key)
    return ResponseBase[List[KnowledgeSchema]](data=data)

@router.post("/", response_model=ResponseBase[KnowledgeSchema], summary="创建知识分片", description="新增一条知识分片数据。")
async def create_knowledge(data: KnowledgeCreateSchema, db: AsyncSession = Depends(get_db)):
    obj = await crud_knowledge.create(db, data)
    return ResponseBase[KnowledgeSchema](data=KnowledgeSchema.model_validate(obj)) 