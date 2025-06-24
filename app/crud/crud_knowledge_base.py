from app.models.knowledge_base import KnowledgeBase
from app.schemas.knowledge_base import KnowledgeBaseCreateSchema, KnowledgeBaseUpdateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

class CRUDKnowledgeBase:
    async def get(self, db: AsyncSession, kb_id: str):
        result = await db.execute(select(KnowledgeBase).where(KnowledgeBase.kb_id == kb_id))
        return result.scalar_one_or_none()

    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(KnowledgeBase).offset(skip).limit(limit))
        return result.scalars().all()

    async def count(self, db: AsyncSession):
        result = await db.execute(select(func.count()).select_from(KnowledgeBase))
        return result.scalar_one()

    async def create(self, db: AsyncSession, obj_in: KnowledgeBaseCreateSchema):
        db_obj = KnowledgeBase(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, kb_id: str, obj_in: KnowledgeBaseUpdateSchema):
        db_obj = await self.get(db, kb_id)
        if not db_obj:
            return None
        for field, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, kb_id: str):
        db_obj = await self.get(db, kb_id)
        if not db_obj:
            return None
        await db.delete(db_obj)
        await db.commit()
        return db_obj

crud_knowledge_base = CRUDKnowledgeBase() 