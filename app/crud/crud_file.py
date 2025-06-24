from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.file import File
from app.schemas.file import FileCreateSchema

class CRUDFile:
    async def get(self, db: AsyncSession, file_id: int):
        result = await db.execute(select(File).where(File.id == file_id))
        return result.scalar_one_or_none()

    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 20):
        result = await db.execute(select(File).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: FileCreateSchema):
        db_obj = File(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, file_id: int):
        obj = await self.get(db, file_id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

    async def count(self, db: AsyncSession):
        result = await db.execute(select(func.count()).select_from(File))
        return result.scalar_one()

crud_file = CRUDFile() 