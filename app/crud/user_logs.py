'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-03-04 16:25:30
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-04 16:40:43
FilePath: \\RAG_Admin\\app\\crud\\user_logs.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user_logs import UserLogs
from app.schemas.user_logs import UserLogsCreate

class CRUDUserLogs:
    async def create(self, db: AsyncSession, obj_in: UserLogsCreate):
        db_obj = UserLogs(**obj_in.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, question_id: int):
        result = await db.execute(select(UserLogs).where(UserLogs.question_id == question_id))
        return result.scalars().first()

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(UserLogs))
        return result.scalars().all()

    async def delete(self, db: AsyncSession, question_id: int):
        obj = await self.get(db, question_id)
        if obj:
            await db.delete(obj)
            await db.commit()
            return obj
        return None

user_logs_crud = CRUDUserLogs() 