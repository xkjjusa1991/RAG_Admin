'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-06-20 13:36:44
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-06-20 14:31:01
FilePath: \RAG_Admin\app\crud\crud_archive_file.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.archive_file import ArchiveFile
from app.schemas.archive_file import ArchiveFileCreateSchema, ArchiveFileUpdateSchema

class CRUDArchiveFile:
    async def get(self, db: AsyncSession, efile_id: int):
        result = await db.execute(select(ArchiveFile).where(ArchiveFile.efile_id == efile_id))
        return result.scalar_one_or_none()

    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 20):
        result = await db.execute(select(ArchiveFile).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: ArchiveFileCreateSchema):
        db_obj = ArchiveFile(**obj_in.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: ArchiveFile, obj_in: ArchiveFileUpdateSchema):
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, efile_id: int):
        obj = await self.get(db, efile_id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

crud_archive_file = CRUDArchiveFile() 