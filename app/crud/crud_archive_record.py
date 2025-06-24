from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.archive_record import ArchiveRecord
from app.models.archive_file import ArchiveFile
from app.schemas.archive_record import ArchiveRecordCreate, ArchiveRecordUpdate

class CRUDArchiveRecord:
    async def get(self, db: AsyncSession, record_id: int):
        result = await db.execute(select(ArchiveRecord).where(ArchiveRecord.record_id == record_id))
        return result.scalar_one_or_none()

    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 20):
        result = await db.execute(select(ArchiveRecord).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: ArchiveRecordCreate):
        db_obj = ArchiveRecord(**obj_in.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: ArchiveRecord, obj_in: ArchiveRecordUpdate):
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, record_id: int):
        obj = await self.get(db, record_id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

    async def get_files_by_record_id(self, db: AsyncSession, record_id: int):
        result = await db.execute(select(ArchiveFile).where(ArchiveFile.record_id == record_id))
        return result.scalars().all()

    async def count(self, db: AsyncSession):
        result = await db.execute(select(func.count()).select_from(ArchiveRecord))
        return result.scalar_one()

crud_archive_record = CRUDArchiveRecord() 