from app.models.knowledge import Knowledge
from app.schemas.knowledge import KnowledgeCreateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class CRUDKnowledge:
    async def get_by_file_id(self, db: AsyncSession, file_id: int):
        result = await db.execute(select(Knowledge).where(Knowledge.file_id == file_id))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: KnowledgeCreateSchema):
        db_obj = Knowledge(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

crud_knowledge = CRUDKnowledge() 