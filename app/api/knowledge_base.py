from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.crud.crud_knowledge_base import knowledge_base_crud
from app.schemas.knowledge_base import KnowledgeBaseSchema, KnowledgeBaseAISchema, KnowledgeBaseCreateSchema  # 导入新的模式
from app.schemas.response import ResponseBase  # 导入基础返回格式
from typing import List

router = APIRouter()

# 根据 file_id 查询知识库数据
@router.get("/knowledge/{file_id}", response_model=ResponseBase[List[KnowledgeBaseSchema]])  # 使用基础返回格式
async def get_knowledge_bases_by_file_id(file_id: int, db: AsyncSession = Depends(get_db)):
    knowledge_bases = await knowledge_base_crud.get_all_by_file_id(db=db, file_id=file_id)
    return ResponseBase(data=knowledge_bases)

# 添加知识库条目
@router.post("/knowledge", response_model=ResponseBase[KnowledgeBaseAISchema])  # 使用基础返回格式
async def create_knowledge_base(knowledge_base: KnowledgeBaseCreateSchema, db: AsyncSession = Depends(get_db)):
    try:
        new_kb = await knowledge_base_crud.create(db=db, knowledge_base=knowledge_base)
        return ResponseBase(data=KnowledgeBaseAISchema(id=new_kb.id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

