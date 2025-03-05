'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-03-04 16:25:30
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-05 01:19:07
FilePath: \\RAG_Admin\\app\\crud\\user_logs.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user_logs import UserLogs
from app.schemas.user_logs import UserLogsCreate
import json

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

    async def get_user_logs_by_session_id(self, db_conn: AsyncSession, session_id: str):
        async with db_conn.begin():
            query = """
                SELECT *
                FROM user_logs
                WHERE session_id = :session_id
                ORDER BY question_time;
            """
            result = await db_conn.execute(query, {"session_id": session_id})
            rows = result.fetchall()

            # 将查询结果转换为字典列表
            dict_list = [
                {
                    "question_id": row[0],
                    "session_id": row[1],
                    "user_id": row[2],
                    "query": row[3],
                    "answer": row[4],
                    "response_segment": json.loads(row[5]),
                    "score": row[6],
                    "prompt": row[7],
                    "like": row[8],
                    "question_time": row[9],
                    "dislike_suggestion": row[10],
                } for row in rows
            ]

            return [UserLogs(**data) for data in dict_list]  # 返回 UserLogs 对象的列表

user_logs_crud = CRUDUserLogs() 