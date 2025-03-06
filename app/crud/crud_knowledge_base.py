from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.knowledge_base import KnowledgeBase
from app.schemas.knowledge_base import KnowledgeBaseSchema, KnowledgeBaseCreateSchema

class CRUDKnowledgeBase:
    async def create(self, db: AsyncSession, knowledge_base: KnowledgeBaseCreateSchema) -> KnowledgeBase:
        # 将 Pydantic 模型转换为 ORM 模型
        db_kb = KnowledgeBase(
            filename=knowledge_base.filename,
            slice_number=knowledge_base.slice_number,
            slice_content=knowledge_base.slice_content,
            embedding=knowledge_base.embedding,
            upload_user=knowledge_base.upload_user,
            upload_time=knowledge_base.upload_time,
            text_head_hash=knowledge_base.text_head_hash,
            text_end_hash=knowledge_base.text_end_hash,
            scope=knowledge_base.scope,
            file_id=knowledge_base.file_id,
            file_summary=knowledge_base.file_summary,
            file_info=knowledge_base.file_info,
            source_type=knowledge_base.source_type,
            file_content=knowledge_base.file_content
        )
        
        db.add(db_kb)
        await db.commit()
        await db.refresh(db_kb)
        return db_kb

    async def get(self, db: AsyncSession, knowledge_base_id: int) -> Optional[KnowledgeBaseSchema]:
        result = await db.execute(select(KnowledgeBase).filter(KnowledgeBase.id == knowledge_base_id))
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession) -> List[KnowledgeBaseSchema]:
        result = await db.execute(select(KnowledgeBase))
        return [KnowledgeBaseSchema.from_orm(kb) for kb in result.scalars().all()]

    async def update(self, db: AsyncSession, knowledge_base_id: int, knowledge_base_data: KnowledgeBase) -> Optional[KnowledgeBaseSchema]:
        result = await self.get(db, knowledge_base_id)
        if result:
            for key, value in knowledge_base_data.dict(exclude_unset=True).items():
                setattr(result, key, value)
            await db.commit()
            await db.refresh(result)
            return KnowledgeBaseSchema.from_orm(result)
        return None

    async def delete(self, db: AsyncSession, knowledge_base_id: int) -> None:
        result = await self.get(db, knowledge_base_id)
        if result:
            await db.delete(result)
            await db.commit()

    async def get_all_by_file_id(self, db: AsyncSession, file_id: int) -> List[KnowledgeBaseSchema]:
        result = await db.execute(select(KnowledgeBase).filter(KnowledgeBase.file_id == file_id).order_by(KnowledgeBase.file_info.asc()))
        return [KnowledgeBaseSchema.from_orm(kb) for kb in result.scalars().all()]

knowledge_base_crud = CRUDKnowledgeBase() 