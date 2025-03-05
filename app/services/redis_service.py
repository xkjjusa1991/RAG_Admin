'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-03-05 00:45:00
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-05 01:17:47
FilePath: \\RAG_Admin\\app\\services\\redis_service.py
Description: Redis 服务模块，用于存储和检索会话数据
'''
from app.core.cache import RedisCache  # 导入 RedisCache 类
from app.schemas.session import SessionData
from typing import List
from app.models.user_logs import UserLogs  # 确保导入 UserLogs 模型
from app.crud.user_logs import CRUDUserLogs  # 确保导入获取用户日志的函数
from app.schemas.conversation import Conversation  # 确保导入 Conversation 模型
from sqlalchemy.ext.asyncio import AsyncSession  # 导入 AsyncSession

class RedisService:
    async def store_session_data(self, session_data: SessionData):
        key = f"session:{session_data.session_id}"
        await RedisCache.set(key, session_data.json())  # 直接调用静态方法

    async def retrieve_session_data(self, session_id: str, db_conn: AsyncSession) -> SessionData:
        key = f"session:{session_id}"
        data = await RedisCache.get(key)  # 使用 cache 中的 get 方法
        if data is not None:
            return SessionData.parse_raw(data)

        # 如果 Redis 中没有数据，从数据库中获取
        db_data = await CRUDUserLogs.get_user_logs_by_session_id(db_conn, session_id)  # 使用 AsyncSession
        conversations = []
        user_id = ""

        if len(db_data) > 0:
            for item in db_data:
                user_id = item.user_id
                if item.answer is None or item.query is None:
                    break
                user_conversation = Conversation(
                    question_id=item.question_id,
                    role="user",
                    content=str(item.query),
                    timestamp=int(item.question_time.timestamp())  # 假设 question_time 是 datetime 对象
                )

                assistant_conversation = Conversation(
                    question_id=item.question_id,
                    role="assistant",
                    content=str(item.answer),
                    timestamp=int(item.question_time.timestamp())  # 假设 question_time 是 datetime 对象
                )
                conversations.extend([user_conversation, assistant_conversation])

            await self.append_to_session_data(session_id, user_id, conversations)  # 存储到 Redis
            result = await RedisCache.get(key)  # 再次从 Redis 获取数据
            return SessionData.parse_raw(result)

        # 如果没有找到任何数据，返回一个空的 SessionData
        blank_session_data = SessionData(
            session_id=session_id,
            user_id="123",  # 提供一个默认值
            scope=["1"],  # 提供一个默认值
            data=[]
        )

        return blank_session_data

    async def append_to_session_data(self, session_id: str, user_id: str, conversations: List[Conversation]):
        key = f"session:{session_id}"
        data = await RedisCache.get(key)  # 直接调用静态方法

        if data:
            # 如果键已存在，追加新的对话列表
            existing_data = SessionData.parse_raw(data)
            existing_data.data.extend(conversations)
            await self.store_session_data(existing_data)  # 直接调用静态方法
        else:
            # 如果键不存在，创建新的 SessionData 实例并存储
            new_session_data = SessionData(
                session_id=session_id,
                user_id=user_id,  # 请设置默认值或从其他地方获取
                scope=["1"],  # 请设置默认值或从其他地方获取
                data=list(conversations)  # 直接使用传入的对话列表
            )
            await self.store_session_data(new_session_data)  # 直接调用静态方法

# 实例化 RedisService
redis_service = RedisService() 