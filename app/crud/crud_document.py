from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentUpdate

class CRUDDocument:
    async def get(self, db: AsyncSession, id: int):
        result = await db.execute(select(Document).where(Document.id == id))
        return result.scalar_one_or_none()

    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 20):
        result = await db.execute(select(Document).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: DocumentCreate):
        db_obj = Document(**obj_in.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: Document, obj_in: DocumentUpdate):
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, id: int):
        obj = await self.get(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

    async def count(self, db: AsyncSession):
        result = await db.execute(select(func.count()).select_from(Document))
        return result.scalar_one()

crud_document = CRUDDocument() 