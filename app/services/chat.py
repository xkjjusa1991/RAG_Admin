'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-03-04 12:24:08
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-05 01:23:12
FilePath: \RAG_Admin\app\services\chat.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.chat import chat_crud
from app.schemas.chat import ChatCreate, ChatResponse
from app.core.logger import logger
import aiohttp
import json
from app.core.config import settings
import time
from app.schemas.conversation import Conversation
from app.services.redis_service import redis_service  # 导入 RedisService
from typing import List

class ChatService:
    async def create_chat(self, db: AsyncSession, obj_in: ChatCreate) -> ChatResponse:
        """创建聊天记录并与算法端交互"""
        logger.info(f"Creating chat record for question: {obj_in.question}")

        # 调用算法端的接口
        model_input = {
            "query": obj_in.question,
            "session_id": obj_in.session_id,
            # 其他必要的参数
        }

        # 获取完整的聊天响应
        response_data = await self.get_chat_response(model_input)
        answer = response_data.get("response", "未返回答案")

        # 创建聊天记录
        chat = await chat_crud.create(db=db, obj_in=obj_in)
        return ChatResponse(
            chat_id=chat.chat_id,
            user_id=chat.user_id,
            question=chat.question,
            answer=answer,
            created_at=chat.created_at
        )

    async def stream_chat(self, model_input: dict):
        """流式获取聊天记录"""
        async with aiohttp.ClientSession() as session:
            async with session.post(settings.CHAT_URL, json=model_input, params={'stream': 'true'}) as resp:
                buffer = bytearray()
                async for chunk in resp.content.iter_any():
                    buffer.extend(chunk)
                    while b'\n' in buffer:
                        part, rest = buffer.split(b'\n', 1)
                        buffer = rest

                        if part:
                            try:
                                data = json.loads(part.decode('utf-8'))
                                answer = data.get("response", "未返回答案")
                                yield f"data: {json.dumps({'answer': answer}, ensure_ascii=False)}\n\n"
                            except json.JSONDecodeError:
                                logger.error(f"Failed to decode JSON from: {part.decode('utf-8')}")
                                break

    async def get_chat_response(self, model_input: dict):
        """获取完整的聊天响应"""
        async with aiohttp.ClientSession() as session:
            async with session.post(settings.CHAT_URL, json=model_input) as resp:
                return await resp.json()
            
    async def fetch_streaming_data_from_model(self, model_input: dict):
        start_time = time.time() * 1000
        data_delimiter = b"\0"  # 使用给定的分隔符
        model_url = settings.CHAT_URL
        async with aiohttp.ClientSession() as session:
            async with session.post(model_url, json=model_input, params={'stream': 'true'}) as resp:
                buffer = bytearray()
                async for chunk in resp.content.iter_any():  # 迭代所有数据块
                    buffer.extend(chunk)
                    while data_delimiter in buffer:
                        # 分割数据包并移除分隔符
                        part, rest = buffer.split(data_delimiter, 1)
                        buffer = rest  # 更新缓冲区，去除已处理的部分

                        # 解析并返回数据
                        if part:
                            try:
                                data = json.loads(part.decode('utf-8'))
                                yield data

                                # 如果数据包中有 "stop" 且其值为 True，则存储会话数据
                                if data.get("stop", True):
                                    # 创建 user_conversation 和 assistant_conversation
                                    user_conversation = Conversation(
                                        question_id=model_input['session_id'],
                                        role="user",
                                        content=model_input['query'],
                                        timestamp=int(start_time)  # 获取当前时间戳
                                    )

                                    assistant_conversation = Conversation(
                                        question_id=model_input['session_id'],
                                        role="assistant",
                                        content=data.get("response", ""),  # 假设算法返回的内容在 "response" 字段
                                        timestamp=int(time.time() * 1000)  # 获取当前时间戳
                                    )

                                    # 将两个对话放入数组中
                                    conversations = [user_conversation, assistant_conversation]

                                    # 调用 redis_service 的 append_to_session_data 方法
                                    await redis_service.append_to_session_data(
                                        session_id=model_input['session_id'],
                                        user_id=model_input.get('user_id', 'default_user_id'),  # 根据需要提供 user_id
                                        conversations=conversations
                                    )
                                    return  # 结束生成器
                            except json.JSONDecodeError:
                                print(f"Failed to decode JSON from: {part.decode('utf-8')}")
                                break  # 如果解析失败，跳出循环并等待下一个数据包

chat_service = ChatService() 